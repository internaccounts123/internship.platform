import numpy as np

from common.config_reader import ConfigReader
from common.enums.decisions import Decisions
from common.utility.driving.angle_calculator import AngleCalculator
from common.utility.driving.driving_calculations import DrivingCalculations
from simulation.work_flows.driving_workflow.driving_work_flow import DrivingWorkFlow


class GeoBasedDrivingWorkflow(DrivingWorkFlow):
    def __init__(self):
        super().__init__()

    @property
    def car(self):
        return self.__car

    @car.setter
    def car(self, car):
        self.__car = car

    def __get_decision_arguments(self, __world_map, __grid):

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
                :param car_list: list of cars present currently
                :param __world_map: current world map
                :param __grid: current global perception
                :return:
                """

        car = self.car
        default_acceleration = ConfigReader.get_data("driving." + self.car.type1 + ".acceleration")[0]
        car_list = __grid[self.car.road_id][self.car.lane_id]
        lane_points, d_points, right_lane_points, right_d_points, left_lane_points, left_d_points, right_car_list, left_car_list = \
            self.__get_decision_arguments(__world_map, __grid)

        _neigh_1, _neigh_2 = DrivingCalculations.get_neighbouring_points(lane_points, [self.car.x, self.car.y])
        bearing = AngleCalculator.get_bearing(_neigh_1[0], _neigh_2[0])

        if decision == Decisions.Accelerate:
            self.car.acceleration = default_acceleration
            self.car.speed += DrivingCalculations.speed_increment(self.car.acceleration)

            self.car.x, self.car.y = DrivingCalculations.get_next_point(self.car.x, self.car.y, self.car.speed, bearing)

        elif decision == Decisions.Constant_speed:
            self.car.acceleration = default_acceleration
            self.car.x, self.car.y = DrivingCalculations.get_next_point(self.car.x, self.car.y, self.car.speed, bearing)

        elif decision == Decisions.De_accelerate:
            c, dis = DrivingCalculations.get_immediate_car(self.car, car_list, lane_points)
            immediate_car = c[np.argmin(np.array(dis))]

            self_car_neigh_1, self_car_neigh_2, imm_neigh_1, imm_neigh_2 =\
                DrivingCalculations.initialize_immediate_distance_arguments(car, immediate_car, lane_points)

            distance_between_me_and_immediate_car = DrivingCalculations.get_distance_from_immediate_car\
                (self.car.car_length, immediate_car.car_length, d_points, imm_neigh_1, self_car_neigh_2)

            self.car.acceleration = DrivingCalculations.calculate_deceleration_rate\
                (self.car.speed, distance_between_me_and_immediate_car, self.car.acceleration)

            new_speed = DrivingCalculations.update_speed(self.car.speed, self.car.acceleration)
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


