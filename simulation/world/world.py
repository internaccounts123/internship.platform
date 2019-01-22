# import random
# import numpy as np
from simulation.vehicle.traffic_creator import TrafficCreator
import common.utility
import time
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
    def world_map (self):
        return self.__world_map

    @world_map.setter
    def world_map (self, world_map ):
        self.__world_map = world_map

    def update(self, event):
        for i in range(100):
            event.wait()
            for car in self.cars:
                # car.y += 1
                # car.front_point = (car.front_point[0], car.front_point[1] + 1)
                # car.back_point = (car.back_point[0], car.back_point[1] + 1)

                # args = road_type, bearing, intercept
                args = self.__world_map.straight_road_info(car.road_id, car.lane_id)
                # bearing, grid
                dec = car.decision(args[1], self.__grid)
                car.move(args[0], args[1], args[2], dec)
            event.clear()
            time.sleep(0.01)

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
