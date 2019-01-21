from simulation.vehicle.vehicle import Vehicle
from common.config_reader import ConfigReader
from common.decisions import Decisions
from common.utility import *


class RuleBased(Vehicle):

    def __init__(self, perception_size, speed_limit, acceleration, de_acceleration, length, type1):
        super(RuleBased, self).__init__(perception_size, speed_limit, acceleration, de_acceleration, length, type1)

    def move(self, road_type, bearing, intercept, decision):
        bearing = deg2rad(bearing)
        if Decisions[decision].value == Decisions.Accelerate.value:
            self._Vehicle__speed = (self._Vehicle__acceleration * (1.0/ConfigReader.get_data("fps")[0])) + self._Vehicle__speed
            self._Vehicle__x = self._Vehicle__x + self._Vehicle__speed * np.cos(bearing)
            self._Vehicle__y = self._Vehicle__y + self._Vehicle__speed * np.sin(bearing)

        elif Decisions[decision].value == Decisions.Constant_speed.value:
            self._Vehicle__x = self._Vehicle__x + self._Vehicle__speed*np.cos(bearing)
            self._Vehicle__y = self._Vehicle__y + self._Vehicle__speed * np.sin(bearing)

        elif Decisions[decision].value == Decisions.De_accelerate.value:
            self._Vehicle__speed = (self._Vehicle__de_acceleration * (1.0/ConfigReader.get_data("fps")[0])) + self._Vehicle__speed
            self._Vehicle__x = self._Vehicle__x + self._Vehicle__speed*np.cos(bearing)
            self._Vehicle__y = self._Vehicle__y + self.__speed * np.sin(bearing)

        elif Decisions[decision].value == Decisions.Move_right.value:
            distance = point_to_line(road_type, (self._Vehicle__x, self._Vehicle__y), bearing, intercept)
            self._Vehicle__x = self._Vehicle__x + distance

        self._Vehicle__front_point = (self._Vehicle__x, self._Vehicle__y + (self._Vehicle__car_length / 2.0))
        self._Vehicle__back_point = (self._Vehicle__x, self._Vehicle__y - (self._Vehicle__car_length / 2.0))
