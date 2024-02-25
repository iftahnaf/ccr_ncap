import numpy as np

class Dynamics():

    def __init__(self):
        pass

    @staticmethod
    def get_positon(vehicle):
        transfrom = vehicle.get_transform()
        location = transfrom.location
        x = location.x
        y = location.y
        z = location.z
        return x, y, z

    @staticmethod
    def get_speed_norm(vehicle):
        velocity = vehicle.get_velocity() # m/s
        speed = np.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2) # m/s
        return speed

    @classmethod
    def get_acceleration_norm(cls, vehicle):
        cls.acceleration = vehicle.get_acceleration() # m/s^2
        magnitude = np.sqrt(cls.acceleration.x**2 + cls.acceleration.y**2 + cls.acceleration.z**2) # m/s^2
        return magnitude
    
    @classmethod
    def get_jerk(cls, vehicle):
        # this one needs to be implemented. because carla doesn't have a method to get jerk, we need to calculate it by derivate the acceleration.
        pass