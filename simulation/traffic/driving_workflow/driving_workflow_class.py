

class DrivingWorkFlow:
    def __init__(self):
        self.__car = None

    @property
    def car(self):
        return self.__car

    @car.setter
    def car(self, self_car):
        self.__car = self_car
