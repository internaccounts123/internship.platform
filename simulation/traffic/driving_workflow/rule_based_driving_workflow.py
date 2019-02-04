import numpy as np

from common.config_reader import ConfigReader
from common.enums.decisions import Decisions
from common.utility.driving.angle_calculator import AngleCalculator
from common.utility.driving.driving_calculations import DrivingCalculations

class RuleBasedDrivingWorkflow():

    def __init__(self):
        self.__car = None

    @property
    def car(self):
        return self.__car

    @car.setter
    def car(self, car):
        self.__car = car

    def implement_decision(self, decision, lane_points, right_lane_points, left_lane_points):
        """

        :param decision: decision taken by the make_decision function
        :param lane_points: list of points for the respective lane
        :param right_lane_points: lane points at the right of the current position
        :param left_lane_points: lane points at the left of the current position
        :return:
        """


        _neigh_1, _neigh_2 = DrivingCalculations.get_neighbouring_points(lane_points, [self.car.x, self.car.y])
        bearing = AngleCalculator.get_bearing(_neigh_1[0], _neigh_2[0])

        if decision == Decisions.Accelerate:
            self.car.speed += DrivingCalculations.speed_increment(self.car)

            self.car.x, self.car.y = DrivingCalculations.get_next_point(self.car.x, self.car.y, self.car.speed, bearing)

        elif decision == Decisions.Constant_speed:
            self.x, self.y = DrivingCalculations.get_next_point(self.car.x, self.car.y, self.car.speed, bearing)

        elif decision == Decisions.De_accelerate:
            new_speed = self.car.speed + DrivingCalculations.speed_increment(self.car)
            if new_speed >= 0:
                self.car.__speed = new_speed
            else:
                pass

            self.car.x, self.car.y = DrivingCalculations.get_next_point(self.car.x, self.car.y, self.car.speed, bearing)

        elif decision == Decisions.Move_right:

            _neigh_1, _neigh_2 = DrivingCalculations.get_neighbouring_points(right_lane_points, [self.car.x, self.car.y])
            self.car.x, self.car.y = DrivingCalculations.point_to_line_intersection(np.array([self.car.x, self.car.y]), np.array([_neigh_1[0], _neigh_2[0]]))



        elif decision == Decisions.Move_left:
            _neigh_1, _neigh_2 = DrivingCalculations.get_neighbouring_points(left_lane_points, [self.car.x, self.car.y])
            self.car.x, self.car.y = DrivingCalculations.point_to_line_intersection(np.array([self.car.x, self.car.y]), np.array([_neigh_1[0], _neigh_2[0]]))

        self.car.back_point, self.car.front_point = DrivingCalculations.get_front_and_back_points(self.car.x, self.car.y, self.car.car_length, bearing)


