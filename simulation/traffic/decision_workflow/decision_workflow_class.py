

class DecisionWorkFlow:
    def __init__(self):
        self.__car = None

    @property
    def car(self):
        return self.__car

    @car.setter
    def car(self, car):
        self.__car = car
