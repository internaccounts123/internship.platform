class Lane:
    def __init__(self, name, lanetype, starting_pos, width):
        self.__width = width
        self.__name = name

        self.__lanetype = lanetype
        self.__starting_pos = starting_pos

    @property
    def width(self):
        return self.__width

    @width.setter
    def length(self, width):
        self.__width = width

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def lanetype(self):
        return self.__lanetype

    @lanetype.setter
    def lanetype(self, lanetype):
        self.__lanetype = lanetype

    @property
    def starting_pos(self):
        return self.__starting_pos

    @starting_pos.setter
    def id(self, starting_pos):
        self.__starting_pos = starting_pos



