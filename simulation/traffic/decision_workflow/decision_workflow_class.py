
class DecisionWorkFlow:
    def __init__(self):
        self.__self_car = None

    @property
    def self_car(self):
        return self.__self_car

    @self_car.setter
    def self_car(self, self_car):
        self.__self_car = self_car
