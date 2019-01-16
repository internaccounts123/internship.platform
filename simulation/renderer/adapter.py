class Adapter:

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
    def scaling(value, old_max, old_min, new_max, new_min):
        """

        :param value:
        :param old_max:
        :param old_min:
        :param new_max:
        :param new_min:
        :return:
        """
        return (((new_max - new_min) * (value - old_min)) / (old_max - old_min)) + new_min
