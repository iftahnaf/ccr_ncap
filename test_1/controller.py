import carla

class Controller():
    
    @staticmethod
    def range_controller(relative_distance, current_speed, desired_range=1.0, kt_p=0.1, kt_d = 0.05, kb_p=0.05):

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
