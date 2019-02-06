
import abc as ABC


class DrivingWorkFlow:
    def __init__(self):
        self.__car = None

    @property
    def car(self):
        return self.__car

    @car.setter
    def car(self, car):
        self.__car = car

    @ABC.abstractmethod
    def implement_decision(self, decision, __world_map, __grid):
        """

        :param decision: decision to be implemented
        :param __world_map: current world map
        :param __grid: current global perception
        :return:
        """
