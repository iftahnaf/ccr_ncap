import carla
class Dynamics():

    def __init__(self, vehicle, dt=0.05):
        self.vehicle = vehicle
        self.acceleration = self.get_acceleration(self.vehicle)
        self.dt = dt
    
    @staticmethod
    def get_positon(vehicle: carla.Vehicle) -> carla.Location:
        """
        Get the position (location) of a given vehicle.

        Args:
            vehicle (carla.Vehicle): The vehicle whose position is to be retrieved.

        Returns:
            carla.Location: The location of the vehicle.

        Example:
            vehicle = get_some_vehicle()  # Get a vehicle instance from somewhere
            position = get_position(vehicle)
            print(position)  # Output: carla.Location(x=100.0, y=200.0, z=0.0)
        """
        transfrom = vehicle.get_transform()
        location = transfrom.location
        return location

    @staticmethod
    def get_velocity(vehicle: carla.Vehicle) -> carla.Vector3D:
        """
        Get the velocity of a given vehicle.

        Args:
            vehicle (carla.Vehicle): The vehicle whose velocity is to be retrieved.

        Returns:
            carla.Vector3D: The velocity vector of the vehicle in meters per second (m/s).

        Example:
            vehicle = get_some_vehicle()  # Get a vehicle instance from somewhere
            velocity = get_velocity(vehicle)
            print(velocity)  # Output: carla.Vector3D(x=5.0, y=0.0, z=0.0)
        """
        velocity = vehicle.get_velocity() # m/s
        return velocity

    @staticmethod
    def get_acceleration(vehicle: carla.Vehicle) -> carla.Vector3D:
        """
        Get the acceleration of a given vehicle.

        Args:
            vehicle (carla.Vehicle): The vehicle whose acceleration is to be retrieved.

        Returns:
            carla.Vector3D: The acceleration vector of the vehicle in meters per second squared (m/s^2).

        Example:
            vehicle = get_some_vehicle()  # Get a vehicle instance from somewhere
            acceleration = get_acceleration(vehicle)
            print(acceleration)  # Output: carla.Vector3D(x=1.0, y=0.0, z=0.0)
        """
        acceleration = vehicle.get_acceleration() # m/s^2
        return acceleration
    
    @staticmethod
    def get_ground_truth_relative_distance(ego_vehicle: carla.Vehicle, stationary_vehicle: carla.Vehicle, ego_vehicle_dimensions: list, stationary_vehicle_dimensions: list) -> float:
        """
        Get the ground truth relative distance between an ego vehicle and a stationary vehicle.

        Args:
            ego_vehicle (carla.Vehicle): The ego vehicle.
            stationary_vehicle (carla.Vehicle): The stationary vehicle.
            ego_vehicle_dimensions (list): The dimensions of the ego vehicle [length, width, height] in meters.
            stationary_vehicle_dimensions (list): The dimensions of the stationary vehicle [length, width, height] in meters.

        Returns:
            float: The relative distance between the ego vehicle and the stationary vehicle in meters.

        Example:
            ego_vehicle = get_ego_vehicle()  # Get the ego vehicle instance
            stationary_vehicle = get_stationary_vehicle()  # Get the stationary vehicle instance
            ego_vehicle_dimensions = [4.5, 2.0, 1.5]  # Ego vehicle dimensions: length, width, height (in meters)
            stationary_vehicle_dimensions = [4.0, 2.5, 1.7]  # Stationary vehicle dimensions: length, width, height (in meters)
            relative_distance = get_ground_truth_relative_distance(ego_vehicle, stationary_vehicle, ego_vehicle_dimensions, stationary_vehicle_dimensions)
            print(relative_distance)  # Output: 10.3
        """
        ego_location = ego_vehicle.get_location()
        stationary_location = stationary_vehicle.get_location()
        raw_distance = ego_location.distance(stationary_location)

        distance = raw_distance - (ego_vehicle_dimensions[0] / 2) - (stationary_vehicle_dimensions[0] / 2)

        return distance
    
    def get_jerk(self, vehicle: carla.Vehicle) -> list[float]:
        """
        Calculate the jerk (rate of change of acceleration) of a vehicle.

        Args:
            vehicle (carla.Vehicle): The vehicle for which jerk is to be calculated.

        Returns:
            list[float]: List containing the jerk components [jerk_x, jerk_y, jerk_z].

        Example:
            ego_vehicle = get_some_vehicle()
            jerk = get_jerk(ego_vehicle)
            print(jerk)  # Output: [0.5, 0.2, -0.1] (example values)
        """
        current_acceleration = self.get_acceleration(vehicle)
        previous_acceleration = self.acceleration

        jerk_x = (current_acceleration.x - previous_acceleration.x) / self.dt
        jerk_y = (current_acceleration.y - previous_acceleration.y) / self.dt
        jerk_z = (current_acceleration.z - previous_acceleration.z) / self.dt

        self.acceleration = current_acceleration

        jerk = [jerk_x, jerk_y, jerk_z]
        return jerk

        