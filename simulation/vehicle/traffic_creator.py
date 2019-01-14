from common.config_reader import ConfigReader
from simulation.vehicle.vehicle import Vehicle
import random


class TrafficCreator(object):
    __percentages = {
        "aggressive": ConfigReader.get_data("driving.traffic.driver_profile_type.aggressive"),
        "moderate": ConfigReader.get_data("driving.traffic.driver_profile_type.moderate"),
        "defensive": ConfigReader.get_data("driving.traffic.driver_profile_type.defensive")
    }
    __traffic = []
    __instance = None

    def __init__(self, map1):

        if TrafficCreator.__instance is None:
            TrafficCreator.__traffic = TrafficCreator.__create_traffic(map1)
        else:
            raise Exception("Object already exists")

    @staticmethod
    def get_instance(map1):

        if TrafficCreator.__instance is None:
            __instance = TrafficCreator(map1)
        return __instance

    @staticmethod
    def __create_traffic(map1):

        taken = []

        for i in range(len(ConfigReader.__percentages)):
            v = TrafficCreator.__vehicle_creator(list(TrafficCreator.__percentages.values())[i], list(TrafficCreator.__percentages.keys())[i])
            v = TrafficCreator.__set_position(v, map1, taken)
            TrafficCreator.__traffic.append(v)

        return TrafficCreator.__traffic

    @staticmethod
    def __set_position(v, map1, taken):

        """
        :param v: Vehicle not assigned a position
        :param map1: full map
        :param taken: already allotted points
        :return: vehicle with assigned initial position
        """

        # choose a point where a car is not already present
        while tup in taken:
            road_idx = random.randint(len(map1.roads))
            lane_idx = random.randint(len(map1.roads[road_idx].lanes))

            # pick random points from list of possible lane points
            xy_id = random.randint((v.car_length/2.0), len(map1.roads[road_idx].lanes[lane_idx].lane_points) - (v.car_length/2.0))
            tup = (map1.roads[road_idx].name, map1.roads[road_idx].lanes[lane_idx].id, map1.roads[road_idx].lanes[lane_idx].lane_points[xy_id[1]])

        lower_limit = map1.roads[road_idx].lanes[lane_idx].lane_points[xy_id[1]] - (v.car_length/2.0)
        upper_limit = map1.roads[road_idx].lanes[lane_idx].lane_points[xy_id[1]] + (v.car_length/2.0)

        # taken points by this car
        points = map1.points_in_yrange(map1.roads[road_idx].name, map1.roads[road_idx].lanes[lane_idx].id, (lower_limit, upper_limit))

        # remove taken points by this car
        for p in points:
            tup = (map1.roads[road_idx].name, map1.roads[road_idx].lanes[lane_idx].id, p[1])
            taken.append(tup)

        # set car attributes
        v.road(map1.roads[road_idx].name)
        v.lane(map1.roads[road_idx].lanes[lane_idx].id)
        v.x(map1.roads[road_idx].lanes[lane_idx].lane_points[xy_id][0])
        v.y(map1.roads[road_idx].lanes[lane_idx].lane_points[xy_id][1])

        return v

    @staticmethod
    def __vehicle_creator(percentage, type1):
        for i in range(ConfigReader.get_data("driving.traffic.traffic_amount") * percentage):
            v = Vehicle(ConfigReader.get_data("driving." + type1 + ".perception_size"),
                                ConfigReader.get_data("driving." + type1 + ".speed_limit"),
                                ConfigReader.get_data("driving." + type1 + ".acceleration"),
                                ConfigReader.get_data("driving." + type1 + ".de_acceleration"),
                                ConfigReader.get_data("driving." + type1 + ".length"), type1)

        return v

    @property
    def traffic(self):
        return TrafficCreator.__traffic

    @traffic.setter
    def traffic(self, traffic):
        TrafficCreator.__traffic = traffic
