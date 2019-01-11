# import random
# import numpy as np
from simulation.vehicle.traffic_creator import TrafficCreator


class World(object):

    def __init__(self, map):
        self.__world_map = map  # Map(map_id, name, version, roads)
        self.__cars = TrafficCreator(map).traffic
        self.__grid = None

    @property
    def cars(self):
        return self.__cars

    @cars.setter
    def cars(self, cars):
        self.__cars = cars

    @property
    def world_map (self):
        return self.__world_map

    @world_map .setter
    def world_map (self, world_map ):
        self.__world_map = world_map

    # def init_cars(self, type):
    #
    #     for i in range(len(self.data[type])):
    #         arg_list = []
    #
    #         for j in self.data[type][i]:
    #             arg_list.append(self.data[type][i][j])
    #
    #         indx=random.randint(len(map.roads))
    #         arg_list.append(map.roads[indx].name)  #road name
    #
    #
    #         set=0
    #         while (set==0):
    #             id_ = map.roads[indx].lanes[random.randint(len(map.roads[indx].lanes))].id
    #             arg_list.append(id_)  # lane id
    #
    #         width=0
    #         while(map.roads[indx].lanes.id != id_):
    #             width+=map.roads[indx].lanes.width
    #         arg_list.append(width) #x
    #
    #
    #         y= random.randint(map.roads[indx].length)

    # arg_list.append()  # y
    #
    # for j in range(1):
    #     arg_list.append(None)
    #
    # self.rbCars.append(RuleBased(arg_list))
    # self.rbSize += 1

    # function update args[6:] map road grid
