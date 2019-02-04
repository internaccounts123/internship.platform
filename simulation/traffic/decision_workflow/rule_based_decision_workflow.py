import numpy as np

from common.enums.decisions import Decisions
from common.utility.driving.angle_calculator import AngleCalculator
from common.utility.driving.driving_calculations import DrivingCalculations
from simulation.traffic.decision_workflow.decision_workflow_class import DecisionWorkFlow

import copy


class RuleBasedDecisionWorkFlow(DecisionWorkFlow):

    def __init__(self):
        super().__init__()


    def lane_change_assistant(self, side_lane_points, side_d_points, side_car_list):
        if len(side_car_list) == 0:
            return False

        _neigh_1, _neigh_2 = DrivingCalculations.get_neighbouring_points(side_lane_points, [self.car.x, self.car.y])

        next_point = DrivingCalculations.point_to_line_intersection(np.array([self.car.x, self.car.y]), np.array([_neigh_1[0], _neigh_2[0]]))
        car_at_next_point = copy.deepcopy(self.car)

        car_at_next_point.x = next_point[0]
        car_at_next_point.y = next_point[1]

        neigh_1, neigh_2 = DrivingCalculations.get_neighbouring_points(side_lane_points, [car_at_next_point.x ,car_at_next_point.y])
        bearing = AngleCalculator.get_bearing(neigh_1[0], neigh_2[0])
        lower_limit, upper_limit = DrivingCalculations.get_front_and_back_points(car_at_next_point.x ,car_at_next_point.y,
                                                                                 car_at_next_point.car_length, bearing)

        #####################################################################################

        u_neigh_1, u_neigh_2 = DrivingCalculations.get_neighbouring_points(side_lane_points, upper_limit)
        l_neigh_1, l_neigh_2 = DrivingCalculations.get_neighbouring_points(side_lane_points, lower_limit)

        distances = DrivingCalculations.generate_distance_points(side_lane_points)

        for car in side_car_list:
            # c_neigh_1, c_neigh_2 = get_neighbouring_points(side_lane_points, [car.x,car.y])
            neigh_1, neigh_2 = DrivingCalculations.get_neighbouring_points(side_lane_points, [car.x, car.y])
            bearing = AngleCalculator.get_bearing(neigh_1[0], neigh_2[0])

            car_lower_limit, car_upper_limit = DrivingCalculations.get_car_limits(car.x ,car.y ,car.car_length ,bearing)

            car_front_prev_neigh, car_front_next_neigh = DrivingCalculations.get_neighbouring_points(side_lane_points, car_upper_limit)
            car_back_prev_neigh, car_back_next_neigh = DrivingCalculations.get_neighbouring_points(side_lane_points, car_lower_limit)

            if distances[l_neigh_1[1]] <= distances[car_front_next_neigh[1]] and distances[car_back_prev_neigh[1]] <= distances[u_neigh_2[1]]:
                return False

        decision = DrivingCalculations.two_sec_rule(car_at_next_point, side_car_list, side_lane_points, side_d_points)

        if decision == Decisions.Lane_change:
            return False
        else:
            return True

    def make_decision(self,  grid, lane_points, d_points, right_lane_points, right_d_points, right_car_list,
                      left_lane_points, left_d_points, left_car_list):
        """
        :param grid:
        :param lane_points:
        :param d_points:
        :param right_lane_points:
        :param right_d_points:
        :param right_car_list:
        :param left_lane_points:
        :param left_d_points:
        :param left_car_list:
        :return:
        """

        current_road = grid[self.car.road_id][self.car.lane_id]
        two_sec_decision = DrivingCalculations.two_sec_rule(self.car, current_road, lane_points, d_points)
        margin_point = DrivingCalculations.get_margin_point(self.car)

        if self.car.speed > self.car.speed_limit or two_sec_decision == Decisions.De_accelerate:
            self.car._Vehicle__decision = Decisions.De_accelerate
            return Decisions.De_accelerate

        elif two_sec_decision == Decisions.Lane_change:
            self.car._Vehicle__decision = self.lane_change(right_lane_points, right_d_points, right_car_list,
                                                           left_lane_points, left_d_points, left_car_list)
            return self.car._Vehicle__decision

        elif margin_point <= self.car.speed <= self.car.speed_limit:
            self.car._Vehicle__decision = Decisions.Constant_speed
            return Decisions.Constant_speed
        elif self.car.speed < margin_point:
            self._Vehicle__decision = Decisions.Accelerate
            return Decisions.Accelerate
    def lane_change(self, right_lane_points, right_d_points, right_car_list, left_lane_points, left_d_points,
                    left_car_list):

        right_bool = self.lane_change_assistant( right_lane_points, right_d_points, right_car_list)

        if right_bool is True:
            return Decisions.Move_right
        else:
            left_bool = self.lane_change_assistant( left_lane_points, left_d_points, left_car_list)
            if left_bool is True:
                return Decisions.Move_left
            else:
                # self.acceleration = -8.64
                self.car.current_acc = 0
                self.car.speed = 0
                return Decisions.De_accelerate