import numpy as np

class Adapter:

    old_max = []
    old_min = [0, 0]


    @staticmethod
    def calculate_initials(_map):
        """

        :param _map:
        :return:
        """
        array_x = []
        array_y = []

        for i in range(len(_map.roads)):
            if _map.roads[i].road_type == "Straight":
                array_x.append(_map.roads[i].lanes[-1].lane_points[0][0])
                array_y.append(_map.roads[i].lanes[0].lane_points[-1][1])

        Adapter.old_max.append(max(array_x))
        Adapter.old_max.append(max(array_y))








    @staticmethod
    def inversion(coords, height, obj_height):
        """
        Convert an object's coords into pygame coordinates (lower-left of object => top left in pygame coords).
        :param coords:
        :param height:
        :param objHeight:
        :return:
        """
        return coords[0], height - coords[1] - obj_height

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

        return np.add(np.divide((np.subtract(new_max, new_min) * np.subtract(value, Adapter.old_min)), np.subtract(Adapter.old_max, Adapter.old_min)), new_min)


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
        if road_type == "straight":
            return np.linalg.norm(ending_pos-starting_pos)