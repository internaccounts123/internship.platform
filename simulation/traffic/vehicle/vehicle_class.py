from common.config_reader import ConfigReader
from common.enums.decisions import Decisions
from common.utility.driving.driving_calculations import *
from simulation.traffic.decision_workflow.rule_based_decision_workflow.rule_based_decision_workflow import RuleBasedDecisionWorkFlow
import numpy as np
import datetime


class Vehicle(object):
    def __init__(self, perception_size, speed_limit, acceleration, de_acceleration, length, type1):
        self.__id = None
        self.__perception_size = perception_size
        self.__speed_limit = speed_limit
        self.__acceleration = acceleration
        self.__de_acceleration = de_acceleration
        self.__car_length = length
        self.__type = type1
        self.__x = None
        self.__y = None
        self.__lane_id = None
        self.__road_id = None
        self.__front_point = None
        self.__back_point = None
        self.__speed = 0.5
        self.__decision = "\0"
        self.__extra = "\0"
        self.__current_acc = acceleration
        self.__main_work_flow = None


    @property
    def car_length(self):
        return self.__car_length

    @car_length.setter
    def car_length(self, car_length):
        self.__car_length = car_length

    @property
    def extra(self):
        return self.__extra

    @extra.setter
    def extra(self, extra):
        self.__extra = extra

    @property
    def road_id(self):
        return self.__road_id

    @road_id.setter
    def road_id(self, road_id):
        self.__road_id = road_id

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
    def lane_id(self):
        return self.__lane_id

    @lane_id.setter
    def lane_id(self, lane_id):
        self.__lane_id = lane_id

    @property
    def front_point(self):
        return self.__front_point

    @front_point.setter
    def front_point(self, front_point):
        self.__front_point = front_point

    @property
    def back_point(self):
        return self.__back_point

    @back_point.setter
    def back_point(self, back_point):
        self.__back_point = back_point

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        self.__speed = speed

    @property
    def decision(self):
        return self.__decision

    @decision.setter
    def decision(self, decision):
        self.__decision = decision

    @property
    def current_acc(self):
        return self.__current_acc

    @current_acc.setter
    def current_acc(self, current_acc):
        self.__current_acc = current_acc

    @property
    def main_work_flow(self):
        return self.__main_work_flow

    @main_work_flow.setter
    def main_work_flow(self, main_work_flow):
        self.__main_work_flow = main_work_flow




    def get_info(self):
        current_time = datetime.datetime.now()

        return ('Time : ' + str(current_time)
                + '  Car ID: ' + str(self.id)
                + '  Speed limit: ' + str(self.speed_limit)
                + '  Car x: ' + str(self.x)
                + '  Car y: ' + str(self.y)
                + '  Speed: ' + str(self.speed)
                + '  Acceleration: ' + str(self.acceleration)
                + '  De-acceleration: ' + str(self.de_acceleration)
                + '  Car road: ' + str(self.road_id)
                + '  Car lane: ' + str(self.lane_id)
                + '  Car decision: ' + self.decision
                + '  Car Extra:  ' + str(self.extra))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'perception_size': self.perception_size,
            'speed_limit': self.speed_limit,
            'acceleration': self.acceleration,
            'de_acceleration': self.de_acceleration,
            'car_length': self.car_length,
            'type': self.type1,
            'x': float(self.x),
            'y': float(self.y),
            'lane_id': self.lane_id,
            'road_id': self.road_id,
            # 'front_point': list(self.front_point),
            'front_point': list(map(lambda x:float(x), self.front_point)),
            # 'back_point': list(self.back_point)
            'back_point': list(map(lambda x:float(x), self.back_point))
        }
