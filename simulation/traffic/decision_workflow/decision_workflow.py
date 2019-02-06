
import abc as ABC


class DecisionWorkFlow:
    def __init__(self):
        self.__car = None

    @property
    def car(self):
        return self.__car

    @car.setter
    def car(self, car):
        self.__car = car

    @ABC.abstractmethod
    def make_decision(self, __grid, __world_map):
        """

        :param __grid: current global perception
        :param __world_map: current world map
        :return:
        """
