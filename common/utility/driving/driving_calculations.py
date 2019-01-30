from common.enums.road_types import *
from common.utility.driving.angle_calculator import AngleCalculator
from common.enums.decisions import Decisions
import numpy as np


class DrivingCalculations :

        @staticmethod
        def point_to_line_intersection(point, neighbours):
            point_to_lane_vector = point - neighbours[0]
            lane_vector = neighbours[1] - neighbours[0]

            if abs(np.dot(lane_vector, lane_vector.T)) == 0.:
                return point
            return neighbours[0] + np.dot (point_to_lane_vector,lane_vector) / np.dot(lane_vector, lane_vector.T) * lane_vector

            # distance = 0

            # # d = |Equation of line| / (a^2 + b^2)^0.5

        @staticmethod
        def get_neighbouring_points(lane_points, point):
            distances = []
            lane_points = np.array(lane_points)

            for i in range(len(lane_points)):
                distances.append(np.linalg.norm(lane_points[i] - np.array(point)))

            point_index = np.argmin(distances)

            if point_index == 0:
                return (lane_points[point_index], point_index), (lane_points[point_index+1], point_index+1)

            elif point_index == len(lane_points)-1:
                return (lane_points[point_index - 1],point_index-1), (lane_points[point_index],point_index)

            self_point = list(lane_points[point_index])
            second_point = list(point)
            angle = AngleCalculator.calculate_angle(lane_points, self_point, second_point,
                                                    lane_points[point_index-1], lane_points[point_index + 1])

            if AngleCalculator.is_forward(angle):
                return (lane_points[point_index], point_index), (lane_points[point_index+1], point_index+1)
            else:
                return (lane_points[point_index - 1], point_index-1), (lane_points[point_index],point_index)

        @staticmethod
        def two_sec_rule(self_car, car_list, lane_points, distance_points, _bool=True):
            # ASSUMING BEARING -> map.calculate_bearing
            # # v^2 = u^2 +2as
            # # 2as = u^2
            # # s = u^2/2a deg2r
            # if len(car_list) == 1:
            #     self_car.current_acc = self_car.acceleration
            #     return False
            # bearing = deg2rad(bearing)

            c = []
            dis = []
            for car in car_list:

                if car.id != self_car.id:
                    _neigh_1, _neigh_2 = DrivingCalculations.get_neighbouring_points(lane_points, [self_car.x, self_car.y])
                    angle = AngleCalculator.calculate_angle(lane_points, [self_car.x, self_car.y], [car.x, car.y],
                                                            _neigh_1[0], _neigh_2[0])

                    if _bool is True:
                        if AngleCalculator.is_forward(angle):
                            c.append(car)
                            dis.append(np.linalg.norm(np.array([car.x, car.y]) - np.array([self_car.x, self_car.y])))
                    else:
                        if AngleCalculator.is_backward(angle):
                            c.append(car)
                            dis.append(np.linalg.norm(np.array([car.x, car.y]) - np.array([self_car.x, self_car.y])))

            if len(c) == 0:
                self_car.current_acc = self_car.acceleration
                self_car.extra = (self_car.current_acc, "no immediate car", "no immediate car")
                return Decisions.Positive
                # return False

            immediate_car = c[np.argmin(np.array(dis))]

            self_car_neigh_1, self_car_neigh_2 = DrivingCalculations.get_neighbouring_points(lane_points, [self_car.x, self_car.y])
            imm_neigh_1, imm_neigh_2 = DrivingCalculations.get_neighbouring_points(lane_points, [immediate_car.x, immediate_car.y])
            distance_between_me_and_immediate_car = np.abs(distance_points[imm_neigh_1[1]]
                                                           - distance_points[self_car_neigh_2[1]]) - (
                                                                self_car.car_length / 2.0 + immediate_car.car_length / 2.0)
            time = 2.0

            # S = vit + 1/2at^2 + car_length + 1
            # This is used instead of S=vt to incorporate acceleration of current car
            distance_two_sec_rule = (self_car.speed * time) + (
                        (1 / 2.0) * self_car.current_acc * np.square(time)) - self_car.car_length / 2.0

            # Change as required
            margin = distance_two_sec_rule * 0.10

            # Audi brake limit
            maximum_brake = -8.64

            # 2 second rule is violated
            if distance_between_me_and_immediate_car < distance_two_sec_rule:

                # Check if it is possible to brake and avoid collision
                if distance_between_me_and_immediate_car > self_car.car_length / 2.0 + immediate_car.car_length / 2.0 + 1 + margin:
                    self_car.current_acc = (np.square(0.0) - np.square(self_car.speed)) / (
                                2.0 * distance_between_me_and_immediate_car)

                    #  Minimum deceleration rate can be not be less than minimum rate
                    if self_car.current_acc > -1:
                        self_car.current_acc = -1

                    # Maximum deceleration rate can be not be more than maximum brake
                    if self_car.current_acc < maximum_brake:
                        self_car.current_acc = maximum_brake

                    # Calculate the distance after hitting max brake
                    safe_distance = (np.square(0.0) - np.square(self_car.speed)) / (
                                2.0 * self_car.current_acc) - self_car.car_length / 2.0

                    # Check if the maximum deceleration does not avoid collision
                    if safe_distance < distance_between_me_and_immediate_car:
                        # self_car.current_acc = maximum_brake
                        return Decisions.De_accelerate
                        # return True

                    # No way out, stop or lane change
                    else:
                        # Change lane
                        # Temporary decision
                        # self_car.current_acc = 0
                        # self_car.speed = 0

                        return Decisions.Lane_change
                # No way out, stop or lane change
                else:
                    # Change lane
                    # Temporary decision
                    # self_car.current_acc = 0
                    # self_car.speed = 0
                    return Decisions.Lane_change

                self_car.extra = (self_car.current_acc, distance_between_me_and_immediate_car, distance_two_sec_rule)
                return Decisions.De_accelerate
                # return True

            # 2 second rule not violated
            else:
                self_car.current_acc = self_car.acceleration
                self_car.extra = (self_car.current_acc, distance_between_me_and_immediate_car, distance_two_sec_rule)
                return Decisions.Positive
                # return False

            # acc = (np.square(immediate_car.speed) - np.square(self_car.speed))/float(2 * s)
            # bearing = AngleCalculator.get_bearing(_neigh_1, _neigh_2)
            # s = (np.square(self_car.speed)) / (2.0 * self_car.de_acceleration)
            # s += self_car.car_length
            # x = self_car.x + s * np.cos(bearing)
            # y = self_car.y + s * np.sin(bearing)
            # _neigh_1, _neigh_2 = get_neighbouring_points(lane_points, [x, y])
            # _angle = AngleCalculator.calculate_angle(lane_points, [x, y],
            # [immediate_car.x, immediate_car.y], _neigh_1, _neigh_2)
            # self_car.extra= (s, x, y, _angle,bearing)
            # if AngleCalculator.is_forward(_angle):
            #     # car is ahead of the point
            #     return False
            # # De_accelerate
            # return True

        @staticmethod
        def generate_distance_points(lane_points):
            distance_points = np.zeros((np.shape(lane_points)[0],))

            for i in range(1, len(lane_points)):
                distance_points[i] = np.linalg.norm(np.array(lane_points[i-1]) - np.array(lane_points[i])) + distance_points[i-1]

            return distance_points

        @staticmethod
        def points_in_range(lane_points, upper_limit, lower_limit):

            """
            :param lane_points: possible lane points of current lane
            :param upper_limit: max point
            :param lower_limit: min point
            :return: this function returns possible points within a range
            """

            possible_points = []

            # [previous neighbour point on lane, index of negihbour 1], [next neighbour point on lane, index of neighbour 2]
            u_neigh_1, u_neigh_2 = DrivingCalculations.get_neighbouring_points(lane_points, upper_limit)
            l_neigh_1, l_neigh_2 = DrivingCalculations.get_neighbouring_points(lane_points, lower_limit)

            distances = DrivingCalculations.generate_distance_points(lane_points)

            for i in range(len(lane_points)):
                if distances[l_neigh_1[1]] <= distances[i] <= distances[u_neigh_2[1]]:
                    possible_points.append(lane_points[i])

            return possible_points

        @staticmethod
        def get_limits(xy_id, lane_points, car_length, bearing):
            limits = []

            lower_limit = (lane_points[xy_id][0] - (car_length / 2.0) * np.cos(bearing), lane_points[xy_id][1]
                           - (car_length / 2.0) * np.sin(bearing))
            upper_limit = (lane_points[xy_id][0] + (car_length / 2.0) * np.cos(bearing), lane_points[xy_id][1]
                           + (car_length / 2.0) * np.sin(bearing))
            limits.append(lower_limit)

            limits.append(upper_limit)

            return limits

        @staticmethod
        def get_car_limits(car_x, car_y, car_length, bearing):
            limits = []

            lower_limit = (car_x - (car_length / 2.0) * np.cos(bearing), car_y - (car_length / 2.0) * np.sin(bearing))
            upper_limit = (car_x + (car_length / 2.0) * np.cos(bearing), car_y + (car_length / 2.0) * np.sin(bearing))

            limits.append(lower_limit)

            limits.append(upper_limit)

            return limits


