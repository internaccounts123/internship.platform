import numpy as np
M_PI = np.pi


def deg2rad(degree):
    """
    :param degree: Angle in Degrees
    :return: Converted Angle in Radians
    """
    return (degree / 180.0) * M_PI


def rad2deg(angle):
    """

    :param angle: Angle in Radians
    :return: Converted Angle in Degrees
    """
    return angle * (180.0 / M_PI)
