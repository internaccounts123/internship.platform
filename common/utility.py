import numpy as np
from common.road_types import *
M_PI = np.pi

# This function converts an input angle from degree to radians
def deg2rad(degree):
    return (degree / 180.0) * M_PI


def rad2deg(angle):
    return angle * (180.0 / M_PI)


def point_to_line(road_type, point, bearing, intercept):

    distance = 0
    # d = |Equation of line| / (a^2 + b^2)^0.5
    if RoadType[road_type].value == RoadType.Straight.value:
        distance = (abs(bearing*point[0] + point[1] + intercept)) / (np.sqrt(np.square(bearing)+np.square(-1)))

    return distance
