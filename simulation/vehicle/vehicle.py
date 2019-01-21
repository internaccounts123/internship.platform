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
        self.__perception = None
        self.__front_point = None
        self.__back_point = None
        self.__speed = 0

    def move(self, road_type, bearing, intercept, decision):
        pass

    @property
    def car_length(self):
        return self.__car_length

    @car_length.setter
    def car_length(self, car_length):
        self.__car_length = car_length

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
    def perception(self):
        return self.__perception

    @perception.setter
    def perception(self, perception):
        self.__perception = perception

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
