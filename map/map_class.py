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

    def GetNextLanePoint(self, currentPoint, laneId, roadname):
        road = self.__roads[[x.roadname for x in self.__roads].index(roadname)]
        lane = road.__lanes[[x.__id for x in self.__lanes].index(laneId)]
        CurrentPointIndex = lane.__lane_points.index(currentPoint)
        return lane.__lane_points[CurrentPointIndex + 1]





