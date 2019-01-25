import numpy as np
from common.enums.road_types import *


class Map:
    def __init__(self, map_id, name, version, roads):
        self.__id = map_id
        self.__name = name
        self.__version = version
        self.__roads = roads

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, map_id):
        self.__id = map_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version):
        self.__id = version

    @property
    def roads(self):
        return self.__roads

    @roads.setter
    def roads(self, roads):
        self.__roads = roads

    # Returns Next Lane Point using the road name, LaneId and Current Position of the Car
    def get_lateral_lanes(self, lane_id, road_name):
        lateral_lanes = []
        road_idx = [x.name for x in self.__roads].index(road_name)
        lane_idx = [x.__id for x in self.__roads[road_idx].__lanes].index(lane_id)
        if lane_idx < 3:
            lateral_lanes. append(self.__roads[road_idx].lanes[lane_idx + 1])

        if lane_idx > 0:
            lateral_lanes.append(self.__roads[road_idx].lanes[lane_idx - 1])

        return lateral_lanes

    def update_lane_info(self, road_id, l_id, dec):
        lane_id = None

        for road in self.__roads:
            if road.road_id == road_id:
                for lane_idx in range(len(road.lanes)):
                    if road.lanes[lane_idx].id == l_id:
                        if dec == "Move_right":
                            lane_id = road.lanes[lane_idx+1].id
                        elif dec == "Move_left":
                            lane_id = road.lanes[lane_idx - 1].id
                        else:
                            lane_id = l_id

        return lane_id

    def get_no_of_road_lanes(self,road_id):
        for road in self.__roads:
            if road.id == road_id:
                return len(road.lanes)

    def is_last_lane_id(self, road_id, lane_id):
        for road in self.__roads:
            if road.road_id == road_id:
                return road.lanes[len(road.lanes) - 1].id == lane_id

    def is_first_lane_id(self, road_id, lane_id):
        for road in self.__roads:
            if road.road_id == road_id:
                return road.lanes[0].id == lane_id


    @staticmethod
    def calculate_bearing(x, y):
        return np.arctan2(y, x)

    def get_road_info(self, current_position):
        for r in self.__roads:
            for l in r.lanes:
                    lane_points = l.lane_points
                    if self.check_point_fit(current_position, lane_points):
                        return r.road_id, l.id

    def check_point_fit(self, current_position, lane_points):
        dx = lane_points[1][0] - lane_points[2][0]

        dy = lane_points[1][1] - lane_points[2][1]

        if dx != 0 and dy != 0:
            slope = dy / dx

        else:
            slope = 0
            intercept = lane_points[2][0] - slope * lane_points[2][1]
            return current_position[0] == intercept

        intercept = lane_points[2][0] - slope * lane_points[2][1]


        # checking if point lies on the line:

        return current_position[1] == slope * current_position[0] - intercept

    def straight_road_info(self, road_id, lane_id):
        arr = []
        for i in range(len(self.__roads)):
            if self.__roads[i].road_id == road_id:
                arr.append(self.__roads[i].road_type)
                arr.append(self.__roads[i].bearing)
                for lane in self.__roads[i].lanes:
                    if lane.id == lane_id:
                        arr.append(lane.intercept)
                        return arr

        # def move(self, road_type, bearing, intercept, make_decision):

    def get_lane_points(self, road_id, lane_id):
        for road in self.__roads:
            if road.road_id == road_id:
                for lane in road.lanes:
                    if lane.id == lane_id:
                        return lane.lane_points, lane.distance_points

    def calculate_initials(self):
        """

        :param _map:
        :return:
        """
        old_max = []
        array_x = []
        array_y = []

        for i in range(len(self.roads)):
            if RoadType[self.roads[i].road_type].value == RoadType.Straight.value:
                array_x.append(self.roads[i].ending_width[0])
                array_y.append(self.roads[i].ending_height[1])

        old_max.append(max(array_x) + 40)
        old_max.append(max(array_y))
        old_min = [-40, 0]

        return old_min, old_max
