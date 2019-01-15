import numpy as np


class Map:
    def __init__(self, map_id, name, version, roads):
        self.__id = map_id
        self.__name = name
        self.__version = version
        self.__roads = roads

    def points_in_yrange(self, road_idx, lane_idx, _range):
        possible_points = np.array(self.roads[road_idx].lanes[lane_idx].lane_points)
        return possible_points[(possible_points[:, 1] >= _range[0]) * (possible_points[:, 1] <= _range[1])]


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


    #Returns Next Lane Point using the road name, LaneId and Current Position of the Car
    def GetNextLanePoint_byName(self, currentPoint, laneId, roadname):
        road = self.__roads[[x.roadname for x in self.__roads].index(roadname)]
        lane = road.__lanes[[x.__id for x in self.__lanes].index(laneId)]
        CurrentPointIndex = lane.__lane_points.index(currentPoint)
        return lane.__lane_points[CurrentPointIndex + 1]

    # Returns Next Lane Point using the road name, LaneId and Current Position of the Car

    def GetLateralLanes (self, laneId, roadname):

        Lateral_lanes = []

        roadIdx = [x.roadname for x in self.__roads].index(roadname)
        LaneIdx = [x.__id for x in self.__lanes].index(laneId)
        if (LaneIdx < 3) :
            Lateral_lanes. append (self.__roads[roadIdx].__lanes[LaneIdx + 1])

        if (LaneIdx > 0):
            Lateral_lanes.append(self.__roads[roadIdx].__lanes[LaneIdx - 1])

        return Lateral_lanes

    def GetRoadInfo ( self, currentposition ): #returns Road Name on the basis of a Vehicle's current position

        for r in self.__roads:
            for l in r.__lanes:
                for lp in l.__lanepoints:
                    if (lp == currentposition):
                        return r.__name
                        break








