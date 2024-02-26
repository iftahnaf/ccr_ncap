import carla

class Controller():
    
    @staticmethod
    def range_controller(current_range, current_speed, desired_range, kt=0.1, kb=0.05):

        if current_range > 50.0:
            req_throttle = 1.0
            req_brake = 0.0
        else:
            req_throttle =  kt * ((current_range - desired_range) / 100.0)
            req_brake = kb * (1 - req_throttle)

        if req_throttle > 1.0:
            req_throttle = 1.0
        elif req_throttle < 0.1:
            req_throttle = 0.0

        control = carla.VehicleControl(throttle=req_throttle, steer=0.0, brake=req_brake, hand_brake=False, reverse=False, manual_gear_shift=False)
        print(req_throttle, req_brake)
        return control
