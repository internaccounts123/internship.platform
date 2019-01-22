from simulation.vehicle.vehicle import Vehicle
from common.config_reader import ConfigReader
from common.decisions import Decisions
from common.utility import *
from map.map_class import Map


class RuleBased(Vehicle):

    # def __init__(self, perception_size, speed_limit, acceleration, de_acceleration, length, type1):
    #     super(RuleBased, self).__init__(perception_size, speed_limit, acceleration, de_acceleration, length, type1)
    #
    # def move(self, road_type, bearing, intercept, decision):
    #
    #     if Decisions[decision].value == Decisions.Accelerate.value:
    #         self.__speed = (self.__acceleration * 1.0/ConfigReader.get_data("fps")) + self.__speed
    #         self.__x = self.__x + self.__speed*np.cos(bearing)
    #         self.__y = self.__y + self.__speed * np.sin(bearing)
    #
    #     elif Decisions[decision].value == Decisions.Constant_speed.value:
    #         # self.__speed = (self.__acceleration * 1.0/ConfigReader.get_data("fps")) + self.__speed
    #         self.__x = self.__x + self.__speed*np.cos(bearing)
    #         self.__y = self.__y + self.__speed * np.sin(bearing)
    #
    #     elif Decisions[decision].value == Decisions.De_accelerate.value:
    #         self.__speed = (-1*self.de_acceleration * 1.0/ConfigReader.get_data("fps")) + self.__speed
    #         self.__x = self.__x + self.__speed*np.cos(bearing)
    #         self.__y = self.__y + self.__speed * np.sin(bearing)
    #
    #     elif Decisions[decision].value == Decisions.Move_right.value:
    #         distance = point_to_line(RoadType[road_type].value, (self.__x, self.__y), bearing, intercept)
    #         self.__x = self.__x + distance
    #     elif Decisions[decision].value == Decisions.Move_left.value:
    #         distance = point_to_line(RoadType[road_type].value, (self.__x, self.__y), bearing, intercept)
    #         self.__x = self.__x - distance

    def __init__(self, perception_size, speed_limit, acceleration, de_acceleration, length, type1):
        super(RuleBased, self).__init__(perception_size, speed_limit, acceleration, de_acceleration, length, type1)

    def move(self, road_type, bearing, intercept, decision):
        bearing = deg2rad(bearing)
        if Decisions[decision].value == Decisions.Accelerate.value:
            self._Vehicle__speed = (self._Vehicle__acceleration * (1.0/ConfigReader.get_data("fps")[0])) + \
                                   self._Vehicle__speed
            self._Vehicle__x = self._Vehicle__x + self._Vehicle__speed * np.cos(bearing)
            self._Vehicle__y = self._Vehicle__y + self._Vehicle__speed * np.sin(bearing)

        elif Decisions[decision].value == Decisions.Constant_speed.value:
            self._Vehicle__x = self._Vehicle__x + self._Vehicle__speed*np.cos(bearing)
            self._Vehicle__y = self._Vehicle__y + self._Vehicle__speed * np.sin(bearing)

        elif Decisions[decision].value == Decisions.De_accelerate.value:
            self._Vehicle__speed = (self._Vehicle__de_acceleration * (1.0/ConfigReader.get_data("fps")[0])) + \
                                   self._Vehicle__speed
            self._Vehicle__x = self._Vehicle__x + self._Vehicle__speed*np.cos(bearing)
            self._Vehicle__y = self._Vehicle__y + self.__speed * np.sin(bearing)

        elif Decisions[decision].value == Decisions.Move_right.value:
            distance = point_to_line(road_type, (self._Vehicle__x, self._Vehicle__y), bearing, intercept)
            self._Vehicle__x = self._Vehicle__x + distance

        self._Vehicle__front_point = (self._Vehicle__x, self._Vehicle__y + (self._Vehicle__car_length / 2.0))
        self._Vehicle__back_point = (self._Vehicle__x, self._Vehicle__y - (self._Vehicle__car_length / 2.0))

    def __two_sec_rule(self, bearing, car_list):
        # ASSUMING BEARING -> map.get_bearing
        # # v^2 = u^2 +2as
        # # 2as = u^2
        # # s = u^2/2a deg2r
        if len(car_list) == 1:
            return False

        bearing = deg2rad(bearing)
        c = []
        dis = []
        for car in car_list:
            _angle = (Map.get_bearing(self._Vehicle__x, self._Vehicle__y) - Map.get_bearing(car.x, car.y)) % 360
            if _angle >= 0 or _angle <= 90 or _angle >= 270 or _angle <= 360:
                c.append(car)
                dis.append(np.linalg.norm(np.array([car.x, car.y]) - np.array([self._Vehicle__x, self._Vehicle__y])))
        immediate_car = c[np.argmin(dis)]
        s = (np.sqrt(self._Vehicle__speed)) / (2 * self._Vehicle__de_acceleration)
        x = self._Vehicle__x + s * np.cos(bearing)
        y = self._Vehicle__y + s * np.sin(bearing)

        _angle = (Map.get_bearing(x, y) - Map.get_bearing(immediate_car.x, immediate_car.y)) % 360

        if _angle >= 0 or _angle <= 90 or _angle >= 270 or _angle <= 360:
            # car is ahead of the point
            return False
        # De_accelerate
        return True

    def decision(self, bearing, grid):
        current_road = grid[self._Vehicle__road_id][self._Vehicle__lane_id]

        if self._Vehicle__speed > self._Vehicle__speed_limit or (self.__two_sec_rule(bearing, current_road)):
            return "De_accelerate"
        elif self._Vehicle__speed == self._Vehicle__speed_limit:
            return "Constant_speed"
        elif self._Vehicle__speed < self._Vehicle__speed_limit:
            return "Accelerate"
            



