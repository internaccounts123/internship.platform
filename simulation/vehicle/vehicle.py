class Vehicle(object):

    def __init__(self, name, color, car_length, car_width, road, x, y, lane, perception):

        self.__name = name
        self.__color = color
        self.__car_length = car_length
        self.__car_width = car_width
        self.__road = road

        self.__x = x
        self.__y = y
        self.__lane = lane

        self.__perception = perception

    # def move(self):
    #     raise NotImplementedError('subclasses must override')

    # def update_grid(self, grid):
    #     self.grid = grid

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color

    @property
    def car_length(self):
        return self.__car_length

    @car_length.setter
    def car_length(self, car_length):
        self.__car_length = car_length

    @property
    def car_width(self):
        return self.__car_width

    @car_width.setter
    def car_width(self, car_width):
        self.__car_width = car_width

    @property
    def road(self):
        return self.__road

    @road.setter
    def road(self, road):
        self.__road = road

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

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

    @x.setter
    def perception(self, perception):
        self.__perception = perception