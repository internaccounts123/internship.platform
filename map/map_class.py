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

    # Returns lateral lanes using lane id and road_name
    def get_lateral_lanes(self, lane_id, road_name):
        lateral_lanes = []
        road_idx = [x.name for x in self.__roads].index(road_name)
        lane_idx = [x.__id for x in self.__roads[road_idx].__lanes].index(lane_id)
        if lane_idx < 3:
            lateral_lanes. append(self.__roads[road_idx].lanes[lane_idx + 1])

        if lane_idx > 0:
            lateral_lanes.append(self.__roads[road_idx].lanes[lane_idx - 1])

        return lateral_lanes

    # Returns road information using the car's current coordinates
    def get_road_info(self, position):
        for r in self.__roads:
            for l in r.lanes:
                    lane_points = l.lane_points
                    if self.check_point_fit(position, lane_points):
                        return r.name

    def check_point_fit(self, position, lane_points):

        dx = lane_points[1][0] - lane_points[2][0]

        dy = lane_points[1][1] - lane_points[2][1]

        if dx != 0 and dy != 0:
            slope = dy / dx

        else:
            slope = 0
            intercept = lane_points[2][0] - slope * lane_points[2][1]
            return position[0] == intercept

        intercept = lane_points[2][0] - slope * lane_points[2][1]

        # checking if point lies on the line:
        return position[1] == slope * position[0] - intercept

    def get_shortest_dist_from_lane(self, position, lane_points, road):

        lane_points = np.array(lane_points)
        starting_position_x = lane_points[0][0]
        starting_position_y = lane_points[0][1]

        final_x = road.length * np.cos(road.bearing) + starting_position_x
        final_y = road.length * np.sin(road.bearing) + starting_position_y

        midpoint_x = starting_position_x + final_x / 2

        midpoint_y = starting_position_y + final_y / 2

        dist_from_point = np.sqrt((position[0] - midpoint_x) ** 2 + (position[1] - midpoint_y) ** 2)

        return dist_from_point

        # A function to track location of points not falling with in the range, the outliers

    def get_closest_road(self, position):
        distances = []
        road_names = []
        for r in self.__roads:
            for l in r.lanes:
                lane_points = l.lane_points
                distances.append(self.get_shortest_dist_from_lane(position, lane_points, r))
                road_names.append(r.name)
        min_index = distances.index(min(distances))
        return road_names[min_index]

