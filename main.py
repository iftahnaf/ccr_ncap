import pygame
import carla
import numpy as np

from dynamics import Dynamics
from sync_mode_scene import CarlaSyncMode
from controller import Controller
from estimator import RangeEstimator
from visualizer import Visualizer

def main():
    actor_list = []

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

        camera_front = blueprint_library.find('sensor.camera.rgb')
        camera_front.set_attribute('image_size_x', '640')
        camera_front.set_attribute('image_size_y', '480')
        camera_front.set_attribute('fov', '80')

        camera_front = world.spawn_actor(
            camera_front,
            carla.Transform(carla.Location(x=2.5, z=0.7), carla.Rotation(pitch=-15)),
            attach_to=ego_vehicle)
        actor_list.append(camera_front)

        camera_semseg = world.spawn_actor(
            blueprint_library.find('sensor.camera.semantic_segmentation'),
            carla.Transform(carla.Location(x=2.5, z=0.7), carla.Rotation(pitch=-15)),
            attach_to=ego_vehicle)
        actor_list.append(camera_semseg)

        state = Dynamics(ego_vehicle, dt=(1/20))
        visualizer = Visualizer()

        desired_range = 1.0

        # Create a synchronous mode context.
        with CarlaSyncMode(world, camera_front, camera_semseg, fps=30) as sync_mode:
            while True:
                if CarlaSyncMode.should_quit():
                    return
                visualizer.clock.tick()

                # Advance the simulation and wait for the data.
                snapshot, image_front, image_semseg = sync_mode.tick(timeout=2.0)

                # get the range between the two vehicles
                range = RangeEstimator.naive_range_estimator(ego_vehicle, stationary_vehicle)

                # calculate the control signal
                speed = np.linalg.norm([state.get_velocity(ego_vehicle).x, state.get_velocity(ego_vehicle).y, state.get_velocity(ego_vehicle).z])
                control = Controller.range_controller(range, speed, desired_range, kt_p=0.55, kt_d=0.01, kb_p=0.65)

                # Apply the control signal to the ego vehicle
                ego_vehicle.apply_control(control)

                position = state.get_positon(ego_vehicle)
                velocity = state.get_velocity(ego_vehicle)
                acceleration = state.get_acceleration(ego_vehicle)
                jerk = state.get_jerk(ego_vehicle)

                # print(f"Range: {range}, Speed: {speed}, Control: {control.throttle}, Position: {position}, Velocity: {velocity}, Acceleration: {acceleration}, Jerk: {jerk}")
                print(range)

                image_semseg.convert(carla.ColorConverter.CityScapesPalette)

                # Draw the display.
                visualizer.draw_image(image_front)
                visualizer.draw_image(image_semseg, blend=True)

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