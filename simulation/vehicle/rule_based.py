from simulation.vehicle.vehicle import Vehicle
from common.config_reader import ConfigReader
from common.enums.decisions import Decisions
from common.utility.conversions import *
from common.utility.driving.angle_calculator import *
from common.utility.driving.driving_calculations import *
import copy


class RuleBased(Vehicle):

    def __init__(self, perception_size, speed_limit, acceleration, de_acceleration, length, type1):
        super(RuleBased, self).__init__(perception_size, speed_limit, acceleration, de_acceleration, length, type1)
    #
    # def move(self, road_type, intercept, decision, lane_points):
    #     pass

    # Good
    def lane_change_assistant(self, right_lane_points, right_d_points, right_car_list):
        if len(right_car_list) == 0:
            return False

        _neigh_1, _neigh_2 = get_neighbouring_points(right_lane_points, [self.x, self.y])

        next_point = point_to_line_intersection(np.array([self.x, self.y]), np.array([_neigh_1[0], _neigh_2[0]]))
        car_at_next_point = copy.deepcopy(self)

        car_at_next_point.x = next_point[0]
        car_at_next_point.y = next_point[1]

        upper_limit = car_at_next_point.y + (car_at_next_point.car_length / 2.0 + 1)
        lower_limit = car_at_next_point.y - (car_at_next_point.car_length / 2.0 + 1)

        for car in right_car_list:
            if lower_limit <= car.y + car.car_length/2.0 + 1 and upper_limit >= car.y - car.car_length/2.0 - 1:
                return False

            #right_bool = False

        # right lane checking
        # two_sec_rule(self_car, bearing, car_list, lane_points, distance_points, _bool=True):
        decision = two_sec_rule(car_at_next_point, right_car_list, right_lane_points, right_d_points)

        if decision == "Lane_change":
            # right_bool = False
            return False
        else:
            #return "Move_right"
            return True

    def make_decision(self, grid, lane_points, d_points, right_lane_points,right_d_points,right_car_list, left_lane_points, left_d_points, left_car_list):
        current_road = grid[self.road_id][self.lane_id]
        two_sec_decision = two_sec_rule(self, current_road, lane_points, d_points)
        margin_point = self.speed_limit - (self.speed_limit * .01)

        if self.speed > self.speed_limit or two_sec_decision == "De_accelerate":
            self._Vehicle__decision = "De_accelerate"
            return "De_accelerate"

        elif two_sec_decision == "Lane_change":
            self._Vehicle__decision = self.lane_change(right_lane_points,right_d_points,right_car_list,left_lane_points, left_d_points, left_car_list)
            return self._Vehicle__decision

        elif margin_point <= self.speed <= self.speed_limit:
            self._Vehicle__decision = "Constant_speed"
            return "Constant_speed"
        elif self.speed < margin_point:
            self._Vehicle__decision = "Accelerate"
            return "Accelerate"

    def lane_change(self, right_lane_points, right_d_points, right_car_list, left_lane_points, left_d_points,
                    left_car_list):

        right_bool = self.lane_change_assistant(right_lane_points, right_d_points, right_car_list)

        if right_bool is True:
            return "Move_right"
        else:
            left_bool = self.lane_change_assistant(left_lane_points, left_d_points, left_car_list)
            if left_bool is True:
                return "Move_left"
            else:
                # self.acceleration = -8.64
                self.current_acc = 0
                self.speed = 0
                return "De_accelerate"

        # if right_bool is False:
        #     # left lane checking
        #
        #     _neigh_1, _neigh_2 = get_neighbouring_points(left_lane_points, [self.x, self.y])
        #
        #     next_point = point_to_line_intersection(np.array([self.x, self.y]), np.array([_neigh_1, _neigh_2]))
        #     car_at_next_point = copy.deepcopy(self)
        #
        #     car_at_next_point.x = next_point[0]
        #     car_at_next_point.y = next_point[1]
        #
        #     upper_limit = car_at_next_point.y + (car_at_next_point.car_length / 2.0 + 1)
        #     lower_limit = car_at_next_point.y - (car_at_next_point.car_length / 2.0 + 1)
        #
        #     left_bool = True
        #     if len(left_car_list) == 0:
        #         left_bool = False
        #
        #     for car in left_car_list:
        #         if lower_limit <= car.y <= upper_limit:
        #             left_bool = False
        #             break
        #     # right lane checking
        #     if left_bool is True:
        #         decision = two_sec_rule(car_at_next_point, left_car_list, left_lane_points, left_d_points, False)
        #
        #         if decision == "Lane_change":
        #             # self.acceleration = -8.64
        #             self.acceleration =0
        #             self.speed=0
        #             return "De_accelerate"
        #         else:
        #             return "Move_left"
        #     else:
        #         # self.acceleration = -8.64
        #         self.acceleration = 0
        #         self.speed = 0
        #         return "De_accelerate"
