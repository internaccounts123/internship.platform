# import random
# import numpy as np
# from simulation.Vehicle.rule_based import RuleBased
from simulation.Map.map import Map


class World(object):

    def __init__(self, rb_size, no_of_lanes, road_length, data):
        self.rb_size = 0
        self.data = data
        self.rb_cars = []
        self.map = Map(no_of_lanes, road_length)

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
    # calculate and update perception










