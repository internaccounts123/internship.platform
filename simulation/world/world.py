import numpy as np
from simulation.vehicle.traffic_creator import TrafficCreator
from collections import defaultdict


class World(object):

    def __init__(self, map1, _id):
        self.__id = _id
        self.__world_map = map1  # Map(map_id, name, version, roads)
        self.__cars = TrafficCreator.create_traffic(map1, self.__id)
        self.__grid = defaultdict(lambda: defaultdict(lambda: []))
        self.__update_init_perception()

    def __update_init_perception(self):
        for car in self.__cars:
            self.__grid[car.road_id][car.lane_id].append(car)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, _id):
        self.__id = _id

    @property
    def cars(self):
        return self.__cars

    @cars.setter
    def cars(self, cars):
        self.__cars = cars

    @property
    def world_map(self):
        return self.__world_map

    @world_map.setter
    def world_map(self, world_map):
        self.__world_map = world_map

    @property
    def grid(self):
        return self.__grid

    @grid.setter
    def grid(self, _grid):
        self.__grid = _grid
