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

    def get_name(self):
        return self.__name

    def get_color(self):
        return self.__color

    def get_car_length(self):
        return self.__car_length

    def get_car_width(self):
        return self.__car_width

    def get_road(self):
        return self.__road

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_lane(self):
        return self.__lane

    def get_perception(self):
        return self.__perception

    def set_name(self, name):
        self.__name = name

    def set_color(self, color):
        self.__color = color

    def set_car_length(self, car_length):
        self.__car_length = car_length

    def set_car_width(self, car_width):
        self.__car_width = car_width

    def set_road(self, road):
        self.__road = road

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def set_lane(self, lane):
        self.__lane = lane