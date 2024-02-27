
class Dynamics():

    def __init__(self, vehicle, dt=0.05):
        self.vehicle = vehicle
        self.acceleration = self.get_acceleration(self.vehicle)
        self.dt = dt
    
    @staticmethod
    def get_positon(vehicle):
        transfrom = vehicle.get_transform()
        location = transfrom.location
        return location

    @staticmethod
    def get_velocity(vehicle):
        velocity = vehicle.get_velocity() # m/s
        return velocity

    @staticmethod
    def get_acceleration(vehicle):
        acceleration = vehicle.get_acceleration() # m/s^2
        return acceleration
    
    def get_jerk(self, vehicle):
        current_acceleration = self.get_acceleration(vehicle)
        previous_acceleration = self.acceleration

        jerk_x = (current_acceleration.x - previous_acceleration.x) / self.dt
        jerk_y = (current_acceleration.y - previous_acceleration.y) / self.dt
        jerk_z = (current_acceleration.z - previous_acceleration.z) / self.dt

        self.acceleration = current_acceleration

        jerk = [jerk_x, jerk_y, jerk_z]
        return jerk

        