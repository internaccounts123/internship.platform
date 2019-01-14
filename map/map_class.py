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



