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
    def get_next_lane_point_by_name(self, current_point, lane_id, road_name):
        road = self.__roads[[x.roadname for x in self.__roads].index(road_name)]
        lane = road.__lanes[[x.__id for x in self.__lanes].index(lane_id)]
        current_point_index = lane.__lane_points.index(current_point)
        return lane.__lane_points[current_point_index + 1]

    # Returns Next Lane Point using the road name, LaneId and Current Position of the Car

    def get_lateral_lanes (self, lane_id, road_name):

        lateral_lanes = []

        road_idx = [x.roadname for x in self.__roads].index(road_name)
        lane_idx = [x.__id for x in self.__lanes].index(lane_id)
        if lane_idx < 3:
            lateral_lanes. append (self.__roads[road_idx].__lanes[lane_idx + 1])

        if lane_idx > 0:
            lateral_lanes.append(self.__roads[road_idx].__lanes[lane_idx - 1])

        return lateral_lanes

    # Returns Road Name on the basis of a Vehicle's current position
    def get_road_info (self, current_position):
        for r in self.__roads:
            for l in r.__lanes:
                for lp in l.__lanepoints:
                    if lp == current_position:
                        return r.__name
                        break
