import numpy as np
from common.road_types import RoadType


class Adapter:

    old_max = []
    old_min = []
    new_min = []
    new_max = []

    @staticmethod
    def calculate_initials(_map, screen_width, screen_height):
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
        Adapter.old_min = [-40, 0]
        Adapter.new_min = [0,0]
        Adapter.new_max = [screen_width, screen_height]

    @staticmethod
    def inversion(coordinates, height, obj_height):
        """
        Convert an object's coordinates into pygame coordinates (lower-left of object => top left in pygame coords).
        :param coordinates:
        :param height:
        :param obj_height:
        :return:
        """
        # if (coordinates[1] - obj_height) < 0:
        #     return coordinates[0], 0
        return (coordinates[0]), height - abs(coordinates[1] - obj_height)

    @staticmethod
    def scaling(value):
        """

        :param value:
        :return:
        """

        if len(Adapter.old_max) == 0:
            raise Exception("Old ranges not set.")

        return np.add(np.divide((np.subtract(Adapter.new_max, Adapter.new_min) * np.subtract(value, Adapter.old_min)),
                                np.subtract(Adapter.old_max, Adapter.old_min)), Adapter.new_min)

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

    # @staticmethod
    # def zoom_in(screen_width, screen_height):
    #     Adapter.old_min = [-40, 0]
    #     Adapter.old_max = [64, 60]
    #     Adapter.new_min = [-400, 0]
    #     Adapter.new_max = [1000, 1000]
    #     screen_height = np.abs(Adapter.new_max[1] - Adapter.new_min[1])
    #     screen_width = np.abs(Adapter.new_max[0] - Adapter.new_min[0])
    #
    #     return
    #
    # @staticmethod
    # def zoom_out(screen_width, screen_height):
    #     Adapter.old_min = [-40, 0]
    #     Adapter.old_max = [64, 60]
    #     Adapter.new_min = [0, 0]
    #     Adapter.new_max = [800, 800]
    #     screen_height = np.abs(Adapter.new_max[1] - Adapter.new_min[1])
    #     screen_width = np.abs(Adapter.new_max[0] - Adapter.new_min[0])
    #     return
