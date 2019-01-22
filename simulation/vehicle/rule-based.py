from simulation.vehicle.vehicle import Vehicle
import numpy as np
from common.config_reader import ConfigReader
from common.decisions import Decisions
from common.utility import *


class RuleBased(Vehicle):

    def __init__(self, perception_size, speed_limit, acceleration, de_acceleration, length, type1):
        super(RuleBased, self).__init__(perception_size, speed_limit, acceleration, de_acceleration, length, type1)

    def move(self, road_type, bearing, intercept, decision):

        if Decisions[decision].value == Decisions.Accelerate.value:
            self.__speed = (self.__acceleration * 1.0/ConfigReader.get_data("fps")) + self.__speed
            self.__x = self.__x + self.__speed*np.cos(bearing)
            self.__y = self.__y + self.__speed * np.sin(bearing)

        elif Decisions[decision].value == Decisions.Constant_speed.value:
            # self.__speed = (self.__acceleration * 1.0/ConfigReader.get_data("fps")) + self.__speed
            self.__x = self.__x + self.__speed*np.cos(bearing)
            self.__y = self.__y + self.__speed * np.sin(bearing)

        elif Decisions[decision].value == Decisions.De_accelerate.value:
            self.__speed = (-1*self.de_acceleration * 1.0/ConfigReader.get_data("fps")) + self.__speed
            self.__x = self.__x + self.__speed*np.cos(bearing)
            self.__y = self.__y + self.__speed * np.sin(bearing)

        elif Decisions[decision].value == Decisions.Move_right.value:
            distance = point_to_line(RoadType[road_type].value, (self.__x, self.__y), bearing, intercept)
            self.__x = self.__x + distance
        elif Decisions[decision].value == Decisions.Move_left.value:
            distance = point_to_line(RoadType[road_type].value, (self.__x, self.__y), bearing, intercept)
            self.__x = self.__x - distance

    def __two_sec_rule(self, bearing, car_list, _map):
        # ASSUMING BEARING -> map.get_bearing
        # # v^2 = u^2 +2as
        # # 2as = u^2
        # # s = u^2/2a deg2r

        c = []
        dis = []
        for car in car_list:
            _angle = (_map.get_bearing(self.__x, self.__y) - _map.get_bearing(car.x, car.y)) % 360
            if _angle >= 0 or _angle <= 90 or _angle >= 270 or _angle <= 360:
                c.append(car)
                dis.append(np.linalg.norm([car.x, car.y] - [self.__x, self.__y]))

        immediate_car = c[np.argmin(dis)]
        s = (np.sqrt(self.__speed)) / (2 * self.__de_acceleration)
        x = self.__x + s * np.cos(bearing)
        y = self.__y + s * np.sin(bearing)

        _angle = (_map.get_bearing(x, y) - _map.get_bearing(immediate_car.x, immediate_car.y))% 360

        if _angle >= 0 or _angle <= 90 or _angle >= 270 or _angle <= 360:
            # car is ahead of the point
            return False
        # De_accelerate
        return True

    def decision(self, bearing, grid):
        current_road = grid[self.__road_id][self.__lane_id]
        if self.__speed > self.__speed_limit or (self.__two_sec_rule(self, bearing, current_road)):
            return "De_accelerate"
        elif self.__speed == self.__speed_limit:
            return "Constant_speed"
        elif self.__speed < self.__speed_limit:
            return "Accelerate"
            



