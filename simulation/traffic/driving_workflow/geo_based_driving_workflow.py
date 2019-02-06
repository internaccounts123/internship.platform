import numpy as np

from common.enums.decisions import Decisions
from common.utility.driving.angle_calculator import AngleCalculator
from common.utility.driving.driving_calculations import DrivingCalculations
from simulation.traffic.driving_workflow.driving_work_flow import DrivingWorkFlow


class GeoBasedDrivingWorkflow(DrivingWorkFlow):
    def __init__(self):
        super().__init__()

    @property
    def car(self):
        return self.__car

    @car.setter
    def car(self, car):
        self.__car = car

    def get_decision_arguments(self, __world_map, __grid):

        """

        :param __world_map: map of the current world
        :param __grid: grid denotes the overall, global perception
        :return:
        """
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

        return lane_points, d_points, right_lane_points, right_d_points, left_lane_points, left_d_points, right_car_list, left_car_list

    def implement_decision(self, decision, __world_map, __grid):
        """
                :param decision: decision to be implemented
                :param __world_map: current world map
                :param __grid: current global perception
                :return:
                """
        car = self.car

        lane_points, d_points, right_lane_points, right_d_points, left_lane_points, left_d_points, right_car_list, left_car_list = \
            self.get_decision_arguments(__world_map, __grid)

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
            car.lane_id = __world_map.update_lane_info(car.road_id, car.lane_id, decision)

        elif decision == Decisions.Move_left:
            _neigh_1, _neigh_2 = DrivingCalculations.get_neighbouring_points(left_lane_points, [self.car.x, self.car.y])
            self.car.x, self.car.y = DrivingCalculations.point_to_line_intersection(np.array([self.car.x, self.car.y]), np.array([_neigh_1[0], _neigh_2[0]]))
            car.lane_id = __world_map.update_lane_info(car.road_id, car.lane_id, decision)

        self.car.back_point, self.car.front_point = DrivingCalculations.get_front_and_back_points(self.car.x, self.car.y, self.car.car_length, bearing)


