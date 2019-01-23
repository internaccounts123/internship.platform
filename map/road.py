class Road:
    def __init__(self, road_id, length, name, road_type, starting_pos, ending_height, ending_width, bearing, connection, lanes):
        self.__road_id = road_id
        self.__length = length
        self.__name = name
        self.__starting_pos = starting_pos
        self.__ending_height = ending_height
        self.__ending_width = ending_width
        self.__bearing = bearing
        self.__connection = connection
        self.__road_type = road_type
        self.__lanes = lanes

    @property
    def road_id(self):
        return self.__road_id

    @road_id.setter
    def road_id(self, road_id):
        self.__road_id = road_id

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
    def ending_height(self):
        return self.__ending_height

    @ending_height.setter
    def ending_height(self, ending_height):
        self.__ending_height = ending_height

    @property
    def ending_width(self):
        return self.__ending_width

    @ending_width.setter
    def ending_width(self, ending_width):
        self.__ending_width = ending_width

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

    @property
    def serialize(self):
        return {
            'road_id': self.road_id,
            'length': self.length,
            'name': self.name,
            'starting_pos': self.starting_pos,
            'ending_height': list(self.ending_height),
            'ending_width': list(self.ending_width),
            'bearing': self.bearing,
            'connection': self.connection,
            'road_type': self.road_type,
            'lanes': list(lane.serialize for lane in self.lanes)
        }
