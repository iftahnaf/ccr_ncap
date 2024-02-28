import carla
import numpy as np
class Dynamics():

    """
    Provides functionality to calculate vehicle dynamics and related information.

    This class encapsulates methods for computing various vehicle dynamics properties,
    such as position, velocity, acceleration, jerk, and relative distance.

    Attributes:
        vehicle (carla.Vehicle): The vehicle object for which dynamics are calculated.
        dt (float): Time interval for calculating jerk.

    Methods:
        __init__: Initializes a new Dynamics object.
        get_position: Retrieves the position (location) of a given vehicle.
        get_velocity: Retrieves the velocity of a given vehicle.
        get_acceleration: Retrieves the acceleration of a given vehicle.
        get_ground_truth_relative_distance: Computes the ground truth relative distance between two vehicles.
        get_jerk: Calculates the jerk (rate of change of acceleration) of a vehicle.

    Example:
        vehicle = get_some_vehicle()  # Get a vehicle instance from somewhere
        dynamics = Dynamics(vehicle)  # Create a Dynamics object for the vehicle
        position = dynamics.get_position()  # Get the position of the vehicle
        velocity = dynamics.get_velocity()  # Get the velocity of the vehicle
        acceleration = dynamics.get_acceleration()  # Get the acceleration of the vehicle
        jerk = dynamics.get_jerk()  # Get the jerk of the vehicle
        relative_distance = dynamics.get_ground_truth_relative_distance(another_vehicle)  # Get the relative distance to another vehicle
    """

    def __init__(self, vehicle, dt=0.05):
        self.vehicle = vehicle
        self.acceleration = self.get_acceleration(self.vehicle)
        self.dt = dt
        self.previous_acceleration = None
        self.filter_window_size = 5  
        self.acceleration_history = {"x": [], "y": [], "z": []}
    
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

        This method calculates the jerk (the rate of change of acceleration) of a vehicle
        using a moving average filter to smooth out noisy acceleration data.

        The function appends the current acceleration to a history buffer and then computes
        the moving average acceleration over a specified window size. The jerk is then
        calculated as the difference between the current filtered acceleration and the
        previous filtered acceleration, divided by the time step.

        The calculated jerk values are bounded within the range [-10, 10] to prevent
        excessively large or small values.

        Example:
            ego_vehicle = get_some_vehicle()
            jerk = get_jerk(ego_vehicle)
            print(jerk)  # Output: [0.5, 0.2, -0.1] (example values)
        """
        current_acceleration = self.get_acceleration(vehicle)

        # Append current acceleration to the history
        self.acceleration_history["x"].append(current_acceleration.x)
        self.acceleration_history["y"].append(current_acceleration.y)
        self.acceleration_history["z"].append(current_acceleration.z)

        # Apply the moving average filter to each axis
        filtered_acceleration = current_acceleration
        if all(len(self.acceleration_history[axis]) >= self.filter_window_size for axis in ["x", "y", "z"]):
            filtered_acceleration = carla.Vector3D(
                x=np.mean(self.acceleration_history["x"][-self.filter_window_size:]),
                y=np.mean(self.acceleration_history["y"][-self.filter_window_size:]),
                z=np.mean(self.acceleration_history["z"][-self.filter_window_size:])
            )

        # Calculate jerk
        jerk = [0, 0, 0]
        if self.previous_acceleration is not None:
            jerk = [(getattr(filtered_acceleration, axis) - getattr(self.previous_acceleration, axis)) / self.dt for axis in ["x", "y", "z"]]

        # Update previous acceleration
        self.previous_acceleration = filtered_acceleration

        saturated_jerk = [min(max(j, -10), 10) for j in jerk]

        return saturated_jerk

        