
from abc import ABC, abstractmethod

class DecisionWorkFlow:
    def __init__(self):
        self.__car = None

    @property
    def car(self):
        return self.__car

    @car.setter
    def car(self, car):
        self.__car = car


    @abstractmethod
    def make_decision(self):

        """
        An abstract method for making decisions
        :return:
        """
