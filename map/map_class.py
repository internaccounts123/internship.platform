import numpy as np


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

    # Returns next lane point using the road name, laneId and current Position of the car

    def get_next_lane_point(self, current_point, lane_id, road_name):
        road = self.__roads[[x.roadname for x in self.__roads].index(road_name)]
        lane = road.__lanes[[x.__id for x in road.__lanes].index(lane_id)]
        current_point_index = lane.__lane_points.index(current_point)
        return lane.__lane_points[current_point_index + 1]

    # Returns Next Lane Point using the road name, LaneId and Current Position of the Car
    def get_lateral_lanes(self, lane_id, road_name):
        lateral_lanes = []
        road_idx = [x.roadname for x in self.__roads].index(road_name)
        lane_idx = [x.__id for x in self.__roads[road_idx].__lanes].index(lane_id)
        if lane_idx < 3:
            lateral_lanes. append(self.__roads[road_idx].__lanes[lane_idx + 1])

        if lane_idx > 0:
            lateral_lanes.append(self.__roads[road_idx].__lanes[lane_idx - 1])

        return lateral_lanes

    def get_road_info(self, current_position):
        for r in self.__roads:
            for l in r.__lanes:
                    if self.check_point_fit(current_position, l.__lanepoints):
                        return r.__name

    @staticmethod
    def check_point_fit(self, current_position, lane_points):

        lane_points = np.array(lane_points)
        dx = lane_points[1][0] - lane_points[2][0]

        dy = lane_points[1][1] - lane_points[2][1]

        if dx != 0 and dy != 0:
            slope = dy / dx

        else:
            slope = 0

        y_intercept = lane_points[1][0] - slope * lane_points[1][1]
        # checking if point lies on the line:
        return current_position[1] == slope * current_position[0] - y_intercept

