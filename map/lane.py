class Lane:
    def __init__(self, id, name, width, lane_points, distance_points, intercept):
        self.__id = id
        self.__width = width
        self.__name = name
        self.__lane_points = lane_points
        self.__distance_points = distance_points
        self.__intercept = intercept

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

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

    @lane_points.setter
    def lane_points(self, lane_points):
        self.__lane_points = lane_points

    @property
    def serialize(self):
        return {
            'id': self.__id,
            'width': self.__width,
            'name': self.__name,
            'lane_points': list(map(lambda x:list(x), self.lane_points))
        }

    @property
    def intercept(self):
        return self.__intercept

    @intercept.setter
    def intercept(self, intercept):
        self.__intercept = intercept

    @property
    def distance_points(self):
        return self.__distance_points

    @distance_points.setter
    def distance_points(self, distance_points):
        self.__distance_points = distance_points
