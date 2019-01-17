import numpy as np
from common.road_types import RoadType


class Adapter:

    old_max = []
    old_min = [-40, 0]

    @staticmethod
    def calculate_initials(_map):
        """

        :param _map:
        :return:
        """
        array_x = []
        array_y = []

        for i in range(len(_map.roads)):
            if RoadType[_map.roads[i].road_type].value == RoadType.Straight.value:
                array_x.append(_map.roads[i].ending_width[0])
                array_y.append(_map.roads[i].ending_height[1])

        Adapter.old_max.append(max(array_x) + 40)
        Adapter.old_max.append(max(array_y))

    @staticmethod
    def inversion(coordinates, height, obj_height):
        """
        Convert an object's coordinates into pygame coordinates (lower-left of object => top left in pygame coords).
        :param coordinates:
        :param height:
        :param obj_height:
        :return:
        """
        return abs(coordinates[0]), abs(height - coordinates[1] - obj_height)

    @staticmethod
    def scaling(value, new_max, new_min):
        """

        :param value:
        :param new_max:
        :param new_min:
        :return:
        """

        if len(Adapter.old_max) == 0:
            raise Exception("Old ranges not set.")

        return np.add(np.divide((np.subtract(new_max, new_min) * np.subtract(value, Adapter.old_min)),
                                np.subtract(Adapter.old_max, Adapter.old_min)), new_min)

    # @staticmethod
    # def scaling_scalar(value, new_max, new_min):
    #     """
    #
    #     :param value:
    #     :param new_max:
    #     :param new_min:
    #     :return:
    #     """
    #
    #     if len(Adapter.old_max) == 0:
    #         raise Exception("Old ranges not set.")
    #     return (((new_max-new_min) * (value-Adapter.old_min)) / (Adapter.old_max-Adapter.old_min)) + new_min

    @staticmethod
    def get_length(road_type, starting_pos, ending_pos):
        if RoadType[road_type].value == RoadType.Straight.value:
            return np.linalg.norm(np.array(ending_pos)-np.array(starting_pos))
