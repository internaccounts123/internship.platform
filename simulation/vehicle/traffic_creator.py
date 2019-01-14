from common.config_reader import ConfigReader
from simulation.vehicle.vehicle import Vehicle
import random


class TrafficCreator(object):
    __percentages = {
        "aggressive": ConfigReader.get_data("driving.traffic.driver_profile_type.aggressive")[0],
        "moderate": ConfigReader.get_data("driving.traffic.driver_profile_type.moderate")[0],
        "defensive": ConfigReader.get_data("driving.traffic.driver_profile_type.defensive")[0]
    }
    __traffic = []

    @staticmethod
    def create_traffic(map1):

        taken = []
        for i in range(len(TrafficCreator.__percentages)):
            vehicle = TrafficCreator.__vehicle_creator(list(TrafficCreator.__percentages.values())[i], list(TrafficCreator.__percentages.keys())[i])
            for v in vehicle:
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

        tup = None
        _do = True
        road_idx = None
        lane_idx = None
        xy_id = None

        # choose a point where a car is not already present
        while (tup in taken) or (_do is True):
            _do = False
            road_idx = random.randint(0, len(map1.roads)-1)
            lane_idx = random.randint(0, len(map1.roads[road_idx].lanes)-1)

            # pick random points from list of possible lane points
            xy_id = random.randint((v.car_length/2.0), (len(map1.roads[road_idx].lanes[lane_idx].lane_points) - (v.car_length/2.0))-1)
            tup = (map1.roads[road_idx].name, map1.roads[road_idx].lanes[lane_idx].id, map1.roads[road_idx].lanes[lane_idx].lane_points[xy_id][1])

        lower_limit = map1.roads[road_idx].lanes[lane_idx].lane_points[xy_id][1] - (v.car_length/2.0)
        upper_limit = map1.roads[road_idx].lanes[lane_idx].lane_points[xy_id][1] + (v.car_length/2.0)

        # taken points by this car
        points = map1.points_in_yrange(road_idx, lane_idx, (lower_limit, upper_limit))

        # remove taken points by this car
        for p in points:
            tup = (map1.roads[road_idx].name, map1.roads[road_idx].lanes[lane_idx].id, p[1])
            taken.append(tup)

        # set car attributes
        v.road = map1.roads[road_idx].name
        v.lane = map1.roads[road_idx].lanes[lane_idx].id
        v.x = map1.roads[road_idx].lanes[lane_idx].lane_points[xy_id][0]
        v.y = map1.roads[road_idx].lanes[lane_idx].lane_points[xy_id][1]

        return v

    @staticmethod
    def __vehicle_creator(percentage, type1):

        vehicles = []
        for i in range(int(ConfigReader.get_data("driving.traffic.traffic_amount")[0] * percentage)):
            vehicles.append(Vehicle(ConfigReader.get_data("driving." + type1 + ".perception_size")[0],
                                ConfigReader.get_data("driving." + type1 + ".speed_limit")[0],
                                ConfigReader.get_data("driving." + type1 + ".acceleration")[0],
                                ConfigReader.get_data("driving." + type1 + ".de_acceleration")[0],
                                ConfigReader.get_data("driving." + type1 + ".length")[0], type1,))

        return vehicles

    @property
    def traffic(self):
        return TrafficCreator.__traffic

    @traffic.setter
    def traffic(self, traffic):
        TrafficCreator.__traffic = traffic
