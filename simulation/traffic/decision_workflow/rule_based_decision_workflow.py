import numpy as np

from common.enums.decisions import Decisions
from common.utility.driving.angle_calculator import AngleCalculator
from common.utility.driving.driving_calculations import DrivingCalculations
from simulation.traffic.decision_workflow.decision_workflow_class import DecisionWorkFlow

import copy


class RuleBasedDecisionWorkFlow(DecisionWorkFlow):

    def __init__(self):
        super().__init__()




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
            self.car._Vehicle__decision = DrivingCalculations.lane_change(self.car, right_lane_points, right_d_points, right_car_list,
                                                           left_lane_points, left_d_points, left_car_list)
            return self.car._Vehicle__decision

        if two_sec_decision == Decisions.Positive:

            if margin_point <= self.car.speed <= self.car.speed_limit:
                self.car._Vehicle__decision = Decisions.Constant_speed
                return Decisions.Constant_speed
            elif self.car.speed < margin_point:
                self._Vehicle__decision = Decisions.Accelerate
                return Decisions.Accelerate

