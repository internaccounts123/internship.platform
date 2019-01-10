class Lane:
    def __init__(self, name, width, lane_points):
        self.__width = width
        self.__name = name
        self.__lane_points = lane_points

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        self.__width = width

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def lane_points(self):
        return self.__lane_points

    @name.setter
    def lane_points(self, lane_ponts):
        self.__lane_points = lane_ponts



