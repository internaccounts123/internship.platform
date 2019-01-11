from common.config_reader import ConfigReader
from simulation.vehicle.vehicle import Vehicle
import random


class TrafficCreator(object):
    __percentage_aggressive = ConfigReader.get_data("driving.traffic.driver_profile_type.aggressive")
    __percentage_moderate = ConfigReader.get_data("driving.traffic.driver_profile_type.moderate")
    __percentage_defensive = ConfigReader.get_data("driving.traffic.driver_profile_type.defensive")
    __traffic = []
    __instance = ""

    def __init__(self, map1):

        if TrafficCreator.__instance == "":
            TrafficCreator.__traffic = TrafficCreator.__create_traffic(map1)
        else:
            raise Exception("Object already exists")

    @staticmethod
    def get_instance(map1):

        if TrafficCreator.__instance == "":
            __instance = TrafficCreator(map1)
        return __instance

    @staticmethod
    def __create_traffic(map1):

        taken = []
        for i in range(ConfigReader.get_data("driving.traffic.traffic_amount") * TrafficCreator.__percentage_aggressive):

            v = Vehicle(ConfigReader.get_data("driving.aggressive.perception_size"),
                                ConfigReader.get_data("driving.aggressive.speed_limit"),
                                ConfigReader.get_data("driving.aggressive.acceleration"),
                                ConfigReader.get_data("driving.aggressive.de_acceleration"),
                                ConfigReader.get_data("driving.aggressive.length"), "aggressive")

            v = TrafficCreator.__set_position(v, map1, taken)
            TrafficCreator.__traffic.append(v)

        for i in range(ConfigReader.get_data("driving.traffic.traffic_amount") * TrafficCreator.__percentage_moderate):

            v = Vehicle(ConfigReader.get_data("driving.moderate.perception_size"),
                                ConfigReader.get_data("driving.moderate.speed_limit"),
                                ConfigReader.get_data("driving.moderate.acceleration"),
                                ConfigReader.get_data("driving.moderate.de_acceleration"),
                                ConfigReader.get_data("driving.moderate.length"), "moderate")

            v = TrafficCreator.__set_position(v, map1, taken)
            TrafficCreator.__traffic.append(v)

        for i in range(ConfigReader.get_data("driving.traffic.traffic_amount") * TrafficCreator.__percentage_defensive):
            v = Vehicle(ConfigReader.get_data("driving.defensive.perception_size"),
                                ConfigReader.get_data("driving.defensive.speed_limit"),
                                ConfigReader.get_data("driving.defensive.acceleration"),
                                ConfigReader.get_data("driving.defensive.de_acceleration"),
                                ConfigReader.get_data("driving.defensive.length"), "defensive")

            v = TrafficCreator.__set_position(v, map1, taken)
            TrafficCreator.__traffic.append(v)
        return TrafficCreator.__traffic

    @staticmethod
    def __set_position(v, map1, taken):

        while tup in taken:
            road_id = random.randint(len(map1.roads))
            lane_id = random.randint(len(map1.roads[road_id].lanes))
            xy_id = random.randint(v.car_length, len(map1.roads[road_id].lanes[lane_id].lane_points))
            tup = (road_id, lane_id, xy_id)

        for i in range(v.car_length):
            tup = (road_id, lane_id, xy_id-i)
            taken.append(tup)
        v.road(map1.roads[road_id].name)
        v.lane(map1.roads[road_id].lanes[lane_id].id)
        v.x(map1.roads[road_id].lanes[lane_id].lane_points[xy_id][0])
        v.y(map1.roads[road_id].lanes[lane_id].lane_points[xy_id][1])

        return v

    @property
    def traffic(self):
        return TrafficCreator.__traffic

    @traffic.setter
    def traffic(self, traffic):
        TrafficCreator.__traffic = traffic
