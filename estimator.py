class RangeEstimator():

    @staticmethod
    def naive_range_estimator(ego_vehicle, stationary_vehicle, ego_vehicle_dimensions, stationary_vehicle_dimensions):
        ego_location = ego_vehicle.get_location()
        stationary_location = stationary_vehicle.get_location()
        raw_distance = ego_location.distance(stationary_location)

        distance = raw_distance - (ego_vehicle_dimensions.x / 2) - (stationary_vehicle_dimensions.x / 2)

        return distance