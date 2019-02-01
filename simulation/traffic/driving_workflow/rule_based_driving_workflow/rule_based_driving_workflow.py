import numpy as np

from common.config_reader import ConfigReader
from common.enums.decisions import Decisions
from common.utility.driving.angle_calculator import AngleCalculator
from common.utility.driving.driving_calculations import DrivingCalculations
from simulation.traffic.driving_workflow.driving_workflow_class import DrivingWorkFlow


class RuleBasedDrivingWorkflow(DrivingWorkFlow):

    def implement_decision(self, decision, lane_points, right_lane_points, left_lane_points):
        """

        :param decision: decision taken by the make_decision function
        :param lane_points: list of points for the respective lane
        :param right_lane_points: lane points at the right of the current position
        :param left_lane_points: lane points at the left of the current position
        :return:
        """
        _neigh_1, _neigh_2 = DrivingCalculations.get_neighbouring_points(lane_points, [self.self_car.x, self.self_car.y])
        bearing = AngleCalculator.get_bearing(_neigh_1[0], _neigh_2[0])

        if Decisions[decision].value == Decisions.Accelerate.value:
            self.self_car.speed += (self.self_car.current_acc * (1.0/ConfigReader.get_data("fps")[0]))

            self.self_car.x, self.self_car.y = DrivingCalculations.get_next_point(self.self_car.x, self.self_car.y, self.self_car.speed, bearing)

        elif Decisions[decision].value == Decisions.Constant_speed.value:
            self.x, self.y = DrivingCalculations.get_next_point(self.self_car.x, self.self_car.y, self.self_car.speed, bearing)

        elif Decisions[decision].value == Decisions.De_accelerate.value:
            new_speed = self.self_car.speed + (self.self_car.current_acc * (1.0/ConfigReader.get_data("fps")[0]))
            if new_speed >= 0:
                self.self_car.__speed = new_speed
            else:
                pass

            self.self_car.x, self.self_car.y = DrivingCalculations.get_next_point(self.self_car.x, self.self_car.y, self.self_car.speed, bearing)

        elif Decisions[decision].value == Decisions.Move_right.value:

            _neigh_1, _neigh_2 = DrivingCalculations.get_neighbouring_points(right_lane_points, [self.self_car.x, self.self_car.y])
            self.self_car.x, self.self_car.y = DrivingCalculations.point_to_line_intersection(np.array([self.self_car.x, self.self_car.y]), np.array([_neigh_1[0], _neigh_2[0]]))



        elif Decisions[decision].value == Decisions.Move_left.value:
            _neigh_1, _neigh_2 = DrivingCalculations.get_neighbouring_points(left_lane_points, [self.self_car.x, self.self_car.y])
            self.self_car.x, self.self_car.y = DrivingCalculations.point_to_line_intersection(np.array([self.self_car.x, self.self_car.y]), np.array([_neigh_1[0], _neigh_2[0]]))

        self.self_car.back_point, self.self_car.front_point = DrivingCalculations.get_front_and_back_points(self.self_car.x,self.self_car.y,self.self_car.car_length,bearing)


