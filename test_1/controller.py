import carla

class Controller():
    
    @staticmethod
    def range_controller(relative_distance: float, current_speed: float, desired_range: float = 1, kt_p: float = 0.1, kt_d: float = 0.05, kb_p:float = 0.05) -> carla.VehicleControl:

        """
        Generates vehicle control commands based on the relative distance to a leading vehicle.

        This function computes throttle and brake commands for the ego vehicle based on its relative distance to a leading vehicle
        and its current speed, aiming to maintain a desired range between the vehicles.

        Args:
            relative_distance (float): The relative distance between the ego vehicle and the leading vehicle in meters.
            current_speed (float): The current speed of the ego vehicle in meters per second (m/s).
            desired_range (float, optional): The desired range between the ego vehicle and the leading vehicle in meters. Defaults to 1.
            kt_p (float, optional): Proportional gain for throttle control. Defaults to 0.1.
            kt_d (float, optional): Derivative gain for throttle control. Defaults to 0.05.
            kb_p (float, optional): Proportional gain for brake control. Defaults to 0.05.

        Returns:
            carla.VehicleControl: The control commands for the ego vehicle.

        Example:
            relative_distance = 10.0  # Relative distance to leading vehicle (in meters)
            current_speed = 20.0  # Current speed of the ego vehicle (in meters per second)
            desired_range = 2.0  # Desired range between vehicles (in meters)
            control = range_controller(relative_distance, current_speed, desired_range)
            ego_vehicle.apply_control(control)
        """

        if relative_distance > 50.0:
            req_throttle = 1.0
            req_brake = 0.0
        else:
            req_throttle =  kt_p * ((relative_distance - desired_range) / 100.0) + kt_d * (current_speed - 0.0)
            req_brake = kb_p * (1 - req_throttle)

        if req_throttle > 1.0:
            req_throttle = 1.0
        elif req_throttle < 0.1:
            req_throttle = 0.0

        control = carla.VehicleControl(throttle=req_throttle, steer=0.0, brake=req_brake, hand_brake=False, reverse=False, manual_gear_shift=False)
        return control
