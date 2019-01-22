# import random
# import numpy as np
import logging
from simulation.vehicle.traffic_creator import TrafficCreator
import common.utility
from common.logger import Logger
from time import gmtime, strftime
import datetime
import time

class World(object):

    def __init__(self, map1, _id):
        self.__id = _id
        self.__world_map = map1  # Map(map_id, name, version, roads)
        self.__cars = TrafficCreator.create_traffic(map1, self.__id)
        self.__grid = None

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
    def world_map(self, world_map ):
        self.__world_map = world_map

    def update(self, event):
        for i in range(100):
            event.wait()
            for car in self.cars:
                car.y += 1
                car.front_point = (car.front_point[0], car.front_point[1] + 1)
                car.back_point = (car.back_point[0], car.back_point[1] + 1)
            event.clear()
            time.sleep(0.01)


    def log_cars(self):

        for car in self.cars:
            car_id = car.id
            car_speed_limit = car.speed_limit
            car_x = car.x
            car_y = car.y
            x = datetime.datetime.now()
            car_road = car.road_id
            car_lane = car.lane_id
            log = Logger.get_logger()
            log.info('Time : ' + str(x) + 'car_speed limit : ' + str(car_speed_limit) + 'car_id : ' + str(car_id)
                     + 'car_x: '
                     + str(car_x) + 'car_y : ' + str(car_y)
                     + 'car road: ' + str(
                car_road) + 'car lane : ' + str(car_lane))

    """
         A function to log all information about the Map to traffic.log and also to the console
                """


    def log_map(self):
        map1=self.world_map
        x = datetime.datetime.now()
        map_id = map1.id
        map_name = map1.name
        log = Logger.get_logger()
        log.info("Time : " + str(x) + "map_id: " + str(map_id) + "map_id : " + map_name)

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
