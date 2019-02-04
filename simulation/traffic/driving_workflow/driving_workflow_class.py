
from abc import ABC, abstractmethod

class DrivingWorkFlow:
    def __init__(self):
        self.__car = None

    @property
    def car(self):
        return self.__car

    @car.setter
    def car(self, self_car):
        self.__car = self_car

    @abstractmethod
    def make_decision(self):
        """
        An abstract method for making decisions
        :return:
        """