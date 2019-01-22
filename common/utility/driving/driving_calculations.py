from common.enums.road_types import *
from common.utility.driving.angle_calculator import AngleCalculator
import numpy as np


def point_to_line(road_type, point, bearing, intercept):

    distance = 0
    # d = |Equation of line| / (a^2 + b^2)^0.5
    if RoadType[road_type].value == RoadType.Straight.value:
        distance = (abs(bearing*point[0] + point[1] + intercept)) / (np.sqrt(np.square(bearing)+np.square(-1)))

    return distance


def get_neighbouring_points(lane_points, point):
    distances = []
    lane_points = np.array(lane_points)

    for i in range(len(lane_points)):
        distances.append(np.linalg.norm(lane_points[i] - np.array(point)))

    point_index = np.argmin(distances)

    if point_index == 0:
        return lane_points[point_index],lane_points[point_index+1]

    elif point_index == len(lane_points)-1:
        return lane_points[point_index-1], lane_points[point_index]

    angle = AngleCalculator.calculate_angle(lane_points, list(lane_points[point_index]), list(point),
                                            lane_points[point_index-1], lane_points[point_index + 1])

    if AngleCalculator.is_forward(angle):
        return lane_points[point_index], lane_points[point_index + 1]
    else:
        return lane_points[point_index - 1], lane_points[point_index]
