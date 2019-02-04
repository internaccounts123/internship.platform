import numpy as np

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


    def get_decision_arguments(self, decision, __world_map, __grid):

        car = self.car
        lane_points, d_points = __world_map.get_lane_points(car.road_id, car.lane_id)
        right_lane_points = []
        right_d_points = []
        left_lane_points = []
        left_d_points = []

        if __world_map.is_last_lane_id(car.road_id, car.lane_id):
            right_car_list = []
        else:
            right_car_list = __grid[car.road_id][car.lane_id + 1]
            right_lane_points, right_d_points = __world_map.get_lane_points(car.road_id, car.lane_id + 1)

        if __world_map.is_first_lane_id(car.road_id, car.lane_id):
            left_car_list = []
        else:
            left_car_list = __grid[car.road_id][car.lane_id - 1]
            left_lane_points, left_d_points = __world_map.get_lane_points(car.road_id, car.lane_id - 1)

        return lane_points, d_points, right_lane_points, right_d_points, left_lane_points, left_d_points


    def implement_decision(self, decision, __world_map, __grid):
        """

        :param decision: decision taken by the make_decision function
        :param lane_points: list of points for the respective lane
        :param right_lane_points: lane points at the right of the current position
        :param left_lane_points: lane points at the left of the current position
        :return:
        """


        car = self.car

        lane_points, d_points, right_lane_points, right_d_points, left_lane_points, left_d_points = \
            self.get_decision_arguments(decision, __world_map, __grid)

        car.lane_id = __world_map.update_lane_info(car.road_id, car.lane_id, decision)

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


