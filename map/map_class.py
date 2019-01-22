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

    @staticmethod
    def get_bearing(x, y):
        return np.arctan2(x, y)

    def get_road_info(self, current_position):
        for r in self.__roads:
            for l in r.lanes:
                    lane_points = l.lane_points
                    if self.check_point_fit(current_position, lane_points):
                        return r.name

    def check_point_fit(self, current_position, lane_points):
        dx = lane_points[1][0] - lane_points[2][0]

        dy = lane_points[1][1] - lane_points[2][1]

        if dx != 0 and dy != 0:
            slope = dy / dx

        else:
            slope = 0
            intercept = lane_points[2][0] - slope * lane_points[2][1]
            return current_position[0]==intercept

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

        # def move(self, road_type, bearing, intercept, decision):
