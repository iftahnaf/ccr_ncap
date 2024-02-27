import pygame
import carla
import cv2
import numpy as np

from dynamics import Dynamics
from sync_mode_scene import CarlaSyncMode
from controller import Controller
from estimator import RangeEstimator
from visualizer import Visualizer

VIEW_WIDTH = 1920
VIEW_HEIGHT = 1080
VIEW_FOV = 100

def main():
    actor_list = []

    client = carla.Client('localhost', 2000)
    client.set_timeout(5.0)

    world = client.load_world('/Game/Carla/Maps/Town02')
    world = client.get_world()

    try:
        stationary_start_pose = carla.Transform(carla.Location(x=-7.53, y=170.0, z=0.3), carla.Rotation(pitch=0.0, yaw=-90.0, roll=0.0))
        ego_start_pose = carla.Transform(carla.Location(x=-7.53, y=270.0, z=0.3), carla.Rotation(pitch=0.0, yaw=-90.0, roll=0.0))

        blueprint_library = world.get_blueprint_library()

        # Spawn the stationary vehicle
        stationary_vehicle = CarlaSyncMode.spawn_vehicle(world, 'vehicle.tesla.model3', stationary_start_pose)
        stationary_vehicle.set_simulate_physics(False)

        # Spawn the controllable vehicle
        ego_vehicle = CarlaSyncMode.spawn_vehicle(world, 'vehicle.bmw.grandtourer', ego_start_pose)
        ego_vehicle.set_simulate_physics(True)

        # get the dimensions of the ego vehicle
        ego_vehicle_dimensions = CarlaSyncMode.get_vehicle_dimensions(ego_vehicle)

        # Spawn the camera
        sensor_front = blueprint_library.find('sensor.camera.rgb')
        sensor_front.set_attribute('image_size_x', str(VIEW_WIDTH))
        sensor_front.set_attribute('image_size_y', str(VIEW_HEIGHT))
        sensor_front.set_attribute('fov', str(VIEW_FOV))

        camera_x_offset = ego_vehicle_dimensions[0] / 2 
        camera_y_offset = ego_vehicle_dimensions[1] / 2 
        camera_z_offset = ego_vehicle_dimensions[2] / 2 
        
        camera_front = world.spawn_actor(
            sensor_front,
            carla.Transform(carla.Location(x=camera_x_offset, y=camera_y_offset, z=camera_z_offset), carla.Rotation(pitch=0, yaw=0, roll=0)),
            attach_to=ego_vehicle)

        actor_list.append(stationary_vehicle)
        actor_list.append(ego_vehicle)
        actor_list.append(camera_front)

        state = Dynamics(ego_vehicle, dt=(1/20))
        visualizer = Visualizer(camera_front, sensor_front)

        desired_range = 1.0

        # Create a synchronous mode context.
        with CarlaSyncMode(world, camera_front, fps=30) as sync_mode:
            while True:
                if CarlaSyncMode.should_quit():
                    return
                visualizer.clock.tick()

                # Advance the simulation and wait for the data.
                _, image_front = sync_mode.tick(timeout=2.0)

                # get the range between the two vehicles
                dist = RangeEstimator.naive_range_estimator(ego_vehicle, stationary_vehicle)

                # calculate the control signal
                speed = np.linalg.norm([state.get_velocity(ego_vehicle).x, state.get_velocity(ego_vehicle).y, state.get_velocity(ego_vehicle).z])
                control = Controller.range_controller(dist, speed, desired_range, kt_p=0.56, kt_d=0.01, kb_p=0.72)

                # Apply the control signal to the ego vehicle
                ego_vehicle.apply_control(control)

                # Draw the display.
                img = np.reshape(np.copy(image_front.raw_data), (image_front.height, image_front.width, 4))
                visualizer.draw_bbox(img, world, ego_vehicle)

                # log the necessary data
                velocity = state.get_velocity(ego_vehicle)
                acceleration = state.get_acceleration(ego_vehicle)
                verdicts = visualizer.get_bbox_vertices()
                jerk = state.get_jerk(ego_vehicle)
                CarlaSyncMode.save_data_to_csv(velocity, acceleration, jerk, dist, verdicts, 'data.csv')

                pygame.display.flip()

    finally:

        print('destroying actors.')
        for actor in actor_list:
            actor.destroy()

        pygame.quit()
        cv2.destroyAllWindows()
        print('done.')


if __name__ == '__main__':

    try:

        main()

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')