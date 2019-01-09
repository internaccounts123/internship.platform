class Map:
    def __init__(self, map_id, name, version, roads):
        self.__id = map_id
        self.__name = name
        self.__version = version
        self.__roads = roads

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_version(self):
        return self.__version

    def get_roads(self):
        return self.__roads

    def set_id(self, map_id):
        self.__id = map_id

    def set_name(self, name):
        self.__name = name

    def set_version(self, version):
        self.__version = version

    def set_roads(self, roads):
        self.__roads = roads
