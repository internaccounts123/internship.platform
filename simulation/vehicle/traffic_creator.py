from common.config_reader import ConfigReader
from simulation.vehicle.vehicle import Vehicle
import random
from common.utility import deg2rad
from common.road_types import RoadType
import numpy as np


class TrafficCreator(object):

    __traffic = []

    @staticmethod
    def create_traffic(map1, world_id):
        __percentages = {
            "aggressive": ConfigReader.get_data("driving.traffic.driver_profile_type.aggressive")[0],
            "moderate": ConfigReader.get_data("driving.traffic.driver_profile_type.moderate")[0],
            "defensive": ConfigReader.get_data("driving.traffic.driver_profile_type.defensive")[0]
        }

        taken = []
        ind_x = 1
        for i in range(len(__percentages)):
            vehicle = TrafficCreator.vehicle_creator(list(__percentages.values())[i], list(__percentages.keys())[i])
            for v in vehicle:
                v.id = (1000*world_id) + ind_x
                v = TrafficCreator.set_position(v, map1, taken)
                TrafficCreator.__traffic.append(v)
                ind_x += 1
        return TrafficCreator.__traffic

    @staticmethod
    def set_position(v, map1, taken):

        """
        :param v: vehicle not assigned a position
        :param map1: full map
        :param taken: already allotted points
        :return: vehicle with assigned initial position
        """

        tup = None
        _do = True
        road_idx = None
        lane_idx = None
        xy_id = None
        lane_points = []

        # choose a point where a car is not already present
        while (tup in taken) or (_do is True):
            _do = False
            road_idx = random.randint(0, len(map1.roads)-1)
            lane_idx = random.randint(0, len(map1.roads[road_idx].lanes)-1)

        # pick random points from list of possible lane points
            __road = map1.roads[road_idx]

            lane_points = TrafficCreator.generate_lane_points(__road.starting_pos, __road.length, __road.road_type,
                                                              __road.bearing, __road.lanes[lane_idx].width,
                                                              __road.lanes[lane_idx].id)

            xy_id = random.randint((v.car_length/2.0), (len(lane_points) - (v.car_length/2.0))-1)
            tup = (map1.roads[road_idx].road_id, map1.roads[road_idx].lanes[lane_idx].id, lane_points[xy_id][1])

        lower_limit = lane_points[xy_id][1] - (v.car_length/2.0)
        upper_limit = lane_points[xy_id][1] + (v.car_length/2.0)

        # taken points by this car
        points = TrafficCreator.points_in_yrange(map1, road_idx, lane_idx, (lower_limit, upper_limit))

        # remove taken points by this car
        for p in points:
            tup = (map1.roads[road_idx].road_id, map1.roads[road_idx].lanes[lane_idx].id, p[1])
            taken.append(tup)

        # set car attributes
        v.road_id = map1.roads[road_idx].road_id
        v.lane_id = map1.roads[road_idx].lanes[lane_idx].id
        v.x = lane_points[xy_id][0]
        v.y = lane_points[xy_id][1]

        v.front_point = (v.x, upper_limit)
        v.back_point = (v.x, lower_limit)

        return v

    @staticmethod
    def vehicle_creator(percentage, type1):

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

    @staticmethod
    def generate_lane_points(starting_position, length, road_type, bearing, lane_width, lane_id):
        """
        Sample and return lane points based on road type, starting point and length
        : param road_type: type of road/lane
        : param starting_point: starting position of lane/road points
        : param length:
        : return:
        """

        coordinates = np.array([])
        starting_position_x = lane_width*(lane_id-1) + (lane_width / 2)
        starting_position_y = starting_position[1]
        bearing = deg2rad(bearing)

        if RoadType[road_type].value == RoadType.Straight.value:

            final_x = length * np.cos(bearing) + starting_position_x
            final_y = length * np.sin(bearing) + starting_position_y
            x = np.linspace(starting_position_x, final_x, num=length)
            y = np.linspace(starting_position_y, final_y, num=length)
            coordinates = np.array([x, y]).T
            coordinates = coordinates.astype(int)

        return coordinates

    @staticmethod
    def points_in_yrange(map1, road_idx, lane_idx, _range):
        possible_points = np.array(map1.roads[road_idx].lanes[lane_idx].lane_points)
        return possible_points[(possible_points[:, 1] >= _range[0]) * (possible_points[:, 1] <= _range[1])]
