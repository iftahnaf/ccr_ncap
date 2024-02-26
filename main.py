import pygame
import carla
import random
import numpy as np
from dynamics import Dynamics
from sync_mode_scene import CarlaSyncMode
from controller import Controller
from estimator import RangeEstimator

def main():
    actor_list = []
    pygame.init()

    display = pygame.display.set_mode(
        (800, 600),
        pygame.HWSURFACE | pygame.DOUBLEBUF)
    font = CarlaSyncMode.get_font()
    clock = pygame.time.Clock()

    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    world = client.get_world()

    try:

        stationary_start_pose = carla.Transform(carla.Location(x=-50.0, y=0.0, z=0.15), carla.Rotation(pitch=0.000000, yaw=-90.642235, roll=0.000000))
        ego_start_pose = carla.Transform(carla.Location(x=-50.0, y=100.0, z=0.15), carla.Rotation(pitch=0.000000, yaw=-90.0, roll=0.000000))

        blueprint_library = world.get_blueprint_library()

        # Spawn the stationary vehicle
        stationary_vehicle = CarlaSyncMode.spawn_vehicle(world, 'vehicle.tesla.model3', stationary_start_pose)
        stationary_vehicle.set_simulate_physics(False)

        # Spawn the controllable vehicle
        ego_vehicle = CarlaSyncMode.spawn_vehicle(world, 'vehicle.bmw.grandtourer', ego_start_pose)
        ego_vehicle.set_simulate_physics(True)

        actor_list.append(stationary_vehicle)
        actor_list.append(ego_vehicle)

        camera_rgb = world.spawn_actor(
            blueprint_library.find('sensor.camera.rgb'),
            carla.Transform(carla.Location(x=-5.5, z=2.8), carla.Rotation(pitch=-15)),
            attach_to=ego_vehicle)
        actor_list.append(camera_rgb)

        camera_semseg = world.spawn_actor(
            blueprint_library.find('sensor.camera.semantic_segmentation'),
            carla.Transform(carla.Location(x=-5.5, z=2.8), carla.Rotation(pitch=-15)),
            attach_to=ego_vehicle)
        actor_list.append(camera_semseg)

        vd = Dynamics()

        # Create a synchronous mode context.
        with CarlaSyncMode(world, camera_rgb, camera_semseg, fps=30) as sync_mode:
            while True:
                if CarlaSyncMode.should_quit():
                    return
                clock.tick()

                # Advance the simulation and wait for the data.
                snapshot, image_rgb, image_semseg = sync_mode.tick(timeout=2.0)

                # get the range between the two vehicles
                range = RangeEstimator.naive_range_estimator(ego_vehicle, stationary_vehicle)

                # calculate the control signal
                control = Controller.range_controller(range, vd.get_speed_norm(ego_vehicle), 1.0, kt_p=0.5, kt_d=0.01, kb_p=0.7)

                # Apply the control signal to the ego vehicle
                ego_vehicle.apply_control(control)

                
                x,y,z = vd.get_positon(ego_vehicle)
                speed_norm = vd.get_speed_norm(ego_vehicle)
                acceleration_norm = vd.get_acceleration_norm(ego_vehicle)

                # print(f"X: {x}, Y: {y}, Z: {z}, Speed: {speed_norm}, Acceleration: {acceleration_norm}")

                image_semseg.convert(carla.ColorConverter.CityScapesPalette)

                # Draw the display.
                CarlaSyncMode.draw_image(display, image_rgb)
                CarlaSyncMode.draw_image(display, image_semseg, blend=True)
                
                pygame.display.flip()

    finally:

        print('destroying actors.')
        for actor in actor_list:
            actor.destroy()

        pygame.quit()
        print('done.')


if __name__ == '__main__':

    try:

        main()

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')