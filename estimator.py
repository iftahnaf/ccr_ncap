import carla


class RangeEstimator():

    @staticmethod
    def naive_range_estimator(vehicle, stationary_vehicle):
        ego_location = vehicle.get_location()
        stationary_location = stationary_vehicle.get_location()
        range = ego_location.distance(stationary_location)
        return range