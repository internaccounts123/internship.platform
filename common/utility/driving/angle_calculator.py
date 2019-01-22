from map.map_class import Map
from common.utility.conversions import rad2deg


class AngleCalculator:

    @staticmethod
    def calculate_angle(lane_points, self_point, second_point, _neigh_1, _neigh_2):
        # _neigh_1, _neigh_2 = get_neighbouring_points(lane_points, self_point)
        _bearing = AngleCalculator.get_bearing(_neigh_1, _neigh_2)
        return rad2deg(Map.calculate_bearing((second_point[0] - self_point[0]),
                                             (second_point[1] - self_point[1])) - _bearing) % 360

    @staticmethod
    def get_bearing(_neigh_1, _neigh_2):
        _vector = _neigh_2 - _neigh_1
        return Map.calculate_bearing(_vector[0], _vector[1])

    @staticmethod
    def is_forward(_angle):
        if (0 <= _angle < 90) or (270 < _angle <= 360):
            return True
        return False

    @staticmethod
    def is_backward(_angle):
        if (0 <= _angle < 90) or (270 < _angle <= 360):
            return False
        return True

    @staticmethod
    def is_right(_angle):
        if 180 < _angle <= 360:
            return True
        return False

    @staticmethod
    def is_left(_angle):
        if 180 < _angle <= 360:
            return False
        return True
