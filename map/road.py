class Road:
    def __init__(self, length, name, road_type, starting_pos, bearing, connection, lanes):
        self.__length = length
        self.__name = name
        self.__starting_pos = starting_pos
        self.__bearing = bearing
        self.__connection = connection
        self.__road_type = road_type
        self.__lanes = lanes

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, length):
        self.__length = length

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def starting_pos(self):
        return self.__starting_pos

    @starting_pos.setter
    def starting_pos(self, starting_pos):
        self.__starting_pos = starting_pos

    @property
    def bearing(self):
        return self.__bearing

    @bearing.setter
    def bearing(self, bearing):
        self.__bearing = bearing

    @property
    def connection(self):
        return self.__connection

    @connection.setter
    def connection(self, connection):
        self.__length = connection

    @property
    def road_type(self):
        return self.__road_type

    @road_type.setter
    def road_type(self, road_type):
        self.__length = road_type

    @property
    def lanes(self):
        return self.__lanes

    @lanes.setter
    def lanes(self, lanes):
        self.__lanes = lanes
