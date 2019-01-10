class Road:
    def __init__(self, length, name, roadtype, starting_pos, bearing, connection, lanes):
        self.__length = length
        self.__name = name
        self.__connection = connection
        self.__roadtype = roadtype
        self.__lanes = lanes

    @property
    def length(self):
        return self.__length

    @id.setter
    def length(self, length):
        self.__length = length

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def connection(self):
        return self.__connection

    @connection.setter
    def connection(self, connection):
        self.__length = connection

    @property
    def roadtype(self):
        return self.__roadtype

    @roadtype.setter
    def id(self, roadtype):
        self.__length = roadtype

    @property
    def lanes(self):
        return self.__lanes

    @roadtype.setter
    def id(self, lanes):
        self.__length = lanes


