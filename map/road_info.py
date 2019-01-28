
class RoadInfo:
    def __init__(self, lane_id, road_id, bearing, road_type):
        self.__lane_id = lane_id
        self.__road_id = road_id
        self.__bearing = bearing
        self.__road_type = road_type

    @property
    def lane_id(self):
        return self.lane__id

    @lane_id.setter
    def lane_id(self, lane_id):
        self.lane__id = lane_id

    @property
    def road_id(self):
        return self.__road_id

    @road_id.setter
    def road_id(self, road_id):
        self.__road_id = road_id

    @property
    def bearing(self):
        return self.__bearing

    @bearing.setter
    def bearing(self, bearing):
        self.__bearing= bearing

    @property
    def road_type(self):
        return self.road_type

    @road_type.setter
    def road_type(self, road_type):
        self.__road_type = road_type





