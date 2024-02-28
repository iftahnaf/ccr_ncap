#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import pygame

import carla
try:
    import numpy as np
except ImportError:
    raise RuntimeError('cannot import numpy, make sure numpy package is installed')

try:
    import queue
except ImportError:
    import Queue as queue


class Scene(object):

    """
    Represents a scene in the Carla simulation environment.

    This class provides functionality to manage the simulation scene, including setting up the environment,
    interacting with vehicles and sensors, and handling data collection.

    Attributes:
        world (carla.World): The Carla world object associated with the scene.
        sensors (tuple): A tuple containing sensor objects used in the scene.
        frame: The current frame of the simulation.
        delta_seconds (float): Time interval between simulation frames.
        _queues (list): A list of queues for handling event data from sensors.
        _settings: Carla world settings used to restore the original settings when exiting the scene.

    Methods:
        __init__: Initializes a new Scene object.
        __enter__: Context manager entry method to set up the scene.
        tick: Advances the simulation by one frame and retrieves sensor data.
        __exit__: Context manager exit method to clean up the scene.
        _retrieve_data: Retrieves sensor data from the queue.
        spawn_vehicle: Spawns a vehicle in the simulation.
        remove_all_actors: Removes all actors from the simulation.
        should_quit: Checks if the user wants to quit the simulation.
        save_data_to_csv: Saves vehicle data to a CSV file.
        get_vehicle_dimensions: Retrieves the dimensions of a vehicle.
        spawn_camera: Spawns a camera sensor attached to a vehicle.

    Example:
        with Scene(world, sensor_front, sensor_rear) as scene:
            while not scene.should_quit():
                data = scene.tick(timeout=1)
                process_data(data)
    """

    def __init__(self, world, *sensors, **kwargs):
        self.world = world
        self.sensors = sensors
        self.frame = None
        self.delta_seconds = 1.0 / kwargs.get('fps', 20)
        self._queues = []
        self._settings = None

    def __enter__(self):
        self._settings = self.world.get_settings()
        self.frame = self.world.apply_settings(carla.WorldSettings(
            no_rendering_mode=False,
            synchronous_mode=True,
            fixed_delta_seconds=self.delta_seconds))

        def make_queue(register_event):
            q = queue.Queue()
            register_event(q.put)
            self._queues.append(q)

        make_queue(self.world.on_tick)
        for sensor in self.sensors:
            make_queue(sensor.listen)
        return self

    def tick(self, timeout):
        self.frame = self.world.tick()
        data = [self._retrieve_data(q, timeout) for q in self._queues]
        assert all(x.frame == self.frame for x in data)
        return data

    def __exit__(self, *args, **kwargs):
        self.world.apply_settings(self._settings)

    def _retrieve_data(self, sensor_queue, timeout):
        while True:
            data = sensor_queue.get(timeout=timeout)
            if data.frame == self.frame:
                return data
    
    @staticmethod
    def spawn_vehicle(world, blueprint_name, transform):
        blueprint = world.get_blueprint_library().find(blueprint_name)
        vehicle = world.spawn_actor(blueprint, transform)
        return vehicle
    
    @staticmethod
    def remove_all_actors(world):
        for actor in world.get_actors():
            actor.destroy()

    @staticmethod
    def should_quit():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return True
        return False
    
    @staticmethod
    def save_data_to_csv(velocity: carla.Vector3D, acceleration: carla.Vector3D, jerk: list[float], relative_distance: float, bbox: list[float], filename: str) -> None:
        header = "velocity_x,velocity_y,velocity_z,acceleration_x,acceleration_y,acceleration_z,jerk_x,jerk_y,jerk_z,relative_distance,bbox_top_left_x,bbox_top_left_y,bbox_top_right_x,bbox_top_right_y,bbox_bottom_left_x,bbox_bottom_left_y,bbox_bottom_right_x,bbox_bottom_right_y\n"
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            with open(filename, 'w') as f:
                f.write(header)
        with open(filename, 'a') as f:
            f.write(f"{velocity.x},{velocity.y},{velocity.z},{acceleration.x},{acceleration.y},{acceleration.z},{jerk[0]},{jerk[1]},{jerk[2]},{relative_distance},{bbox[0]},{bbox[3]},{bbox[1]},{bbox[3]},{bbox[0]},{bbox[2]},{bbox[1]},{bbox[2]}\n")

    @staticmethod
    def get_vehicle_dimensions(vehicle: carla.Vehicle) -> list[float]:
        bounding_box = vehicle.bounding_box.extent
        length = 2 * bounding_box.x
        width = 2 * bounding_box.y
        height = 2 * bounding_box.z

        dimensions = [length, width, height]

        return dimensions
    
    @staticmethod
    def spawn_camera(world: carla.World, ego_vehicle: carla.Vehicle, ego_vehicle_dimensions: list[float], view_width: int=1920, view_height: int=1080, view_fov: int=90) -> tuple[carla.Actor, carla.Sensor]:
        sensor_front = world.get_blueprint_library().find('sensor.camera.rgb')
        sensor_front.set_attribute('image_size_x', str(view_width))
        sensor_front.set_attribute('image_size_y', str(view_height))
        sensor_front.set_attribute('fov', str(view_fov))

        camera_offsets = [x/2 for x in ego_vehicle_dimensions]
        
        camera_front = world.spawn_actor(
            sensor_front,
            carla.Transform(carla.Location(x=camera_offsets[0], y=camera_offsets[1], z=camera_offsets[2]), carla.Rotation(pitch=0, yaw=0, roll=0)),
            attach_to=ego_vehicle)
        
        return camera_front, sensor_front