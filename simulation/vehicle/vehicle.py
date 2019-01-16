import numpy as np


class Vehicle(object):

    def __init__(self, perception_size, speed_limit, acceleration, de_acceleration, length, type1):

        self.__perception_size = perception_size
        self.__speed_limit = speed_limit
        self.__acceleration = acceleration
        self.__de_acceleration = de_acceleration
        self.__car_length = length
        self.__type = type1
        self.__x = None
        self.__y = None
        self.__lane = None
        self.__road = None
        self.__perception = None
        self.__id = None

    @property
    def car_length(self):
        return self.__car_length

    @car_length.setter
    def car_length(self, car_length):
        self.__car_length = car_length

    @property
    def road(self):
        return self.__road

    @road.setter
    def road(self, road):
        self.__road = road

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, _id):
        self.__id = _id

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def de_acceleration(self):
        return self.__de_acceleration

    @de_acceleration.setter
    def de_acceleration(self, de_acceleration):
        self.__de_acceleration = de_acceleration

    @property
    def acceleration(self):
        return self.__acceleration

    @acceleration.setter
    def acceleration(self, acceleration):
        self.__acceleration = acceleration

    @property
    def perception_size(self):
        return self.__perception_size

    @perception_size.setter
    def perception_size(self, ps):
        self.__perception_size = ps

    @property
    def speed_limit(self):
        return self.__speed_limit

    @speed_limit.setter
    def speed_limit(self, sl):
        self.__speed_limit = sl

    @property
    def type1(self):
        return self.__type

    @type1.setter
    def type1(self, t):
        self.__type = t

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def lane(self):
        return self.__lane

    @lane.setter
    def lane(self, lane):
        self.__lane = lane

    @property
    def perception(self):
        return self.__perception

    @perception.setter
    def perception(self, perception):
        self.__perception = perception
