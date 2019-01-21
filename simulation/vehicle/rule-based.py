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
            self.__speed = (self.de_acceleration * 1.0/ConfigReader.get_data("fps")) + self.__speed
            self.__x = self.__x + self.__speed*np.cos(bearing)
            self.__y = self.__y + self.__speed * np.sin(bearing)

        elif Decisions[decision].value == Decisions.Move_right.value:
            distance = point_to_line(RoadType[road_type].value, (self.__x, self.__y), bearing, intercept)
            self.__x = self.__x + distance
