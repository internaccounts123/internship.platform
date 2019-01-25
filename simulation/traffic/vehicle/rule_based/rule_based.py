from simulation.traffic.vehicle.vehicle_class import Vehicle
from common.utility.driving.driving_calculations import *
import copy


class RuleBased(Vehicle):

    def __init__(self, perception_size, speed_limit, acceleration, de_acceleration, length, type1):
        super(RuleBased, self).__init__(perception_size, speed_limit, acceleration, de_acceleration, length, type1)

    def lane_change_assistant(self, side_lane_points, side_d_points, side_car_list):
        if len(side_car_list) == 0:
            return False

        _neigh_1, _neigh_2 = get_neighbouring_points(side_lane_points, [self.x, self.y])

        next_point = point_to_line_intersection(np.array([self.x, self.y]), np.array([_neigh_1[0], _neigh_2[0]]))
        car_at_next_point = copy.deepcopy(self)

        car_at_next_point.x = next_point[0]
        car_at_next_point.y = next_point[1]

        neigh_1, neigh_2 = get_neighbouring_points(side_lane_points, [car_at_next_point.x,car_at_next_point.y])
        bearing = AngleCalculator.get_bearing(neigh_1[0], neigh_2[0])
        lower_limit = (car_at_next_point.x - (car_at_next_point.car_length / 2.0) * np.cos(bearing), car_at_next_point.y
                       - (car_at_next_point.car_length / 2.0) * np.sin(bearing))
        upper_limit = (car_at_next_point.x + (car_at_next_point.car_length / 2.0) * np.cos(bearing), car_at_next_point.y
                       + (car_at_next_point.car_length / 2.0) * np.sin(bearing))

        #####################################################################################

        u_neigh_1, u_neigh_2 = get_neighbouring_points(side_lane_points, upper_limit)
        l_neigh_1, l_neigh_2 = get_neighbouring_points(side_lane_points, lower_limit)

        distances = generate_distance_points(side_lane_points)

        for car in side_car_list:
            # c_neigh_1, c_neigh_2 = get_neighbouring_points(side_lane_points, [car.x,car.y])
            neigh_1, neigh_2 = get_neighbouring_points(side_lane_points, [car.x, car.y])
            bearing = AngleCalculator.get_bearing(neigh_1[0], neigh_2[0])
            car_lower_limit = (car.x - (car.car_length / 2.0) * np.cos(bearing), car.y - (car.car_length / 2.0) * np.sin(bearing))
            car_upper_limit = (car.x + (car.car_length / 2.0) * np.cos(bearing), car.y + (car.car_length / 2.0) * np.sin(bearing))

            car_front_prev_neigh, car_front_next_neigh = get_neighbouring_points(side_lane_points, car_upper_limit)
            car_back_prev_neigh, car_back_next_neigh = get_neighbouring_points(side_lane_points, car_lower_limit)

            if distances[l_neigh_1[1]] <= distances[car_front_next_neigh[1]] and distances[car_back_prev_neigh[1]] <= distances[u_neigh_2[1]]:
                return False

        decision = two_sec_rule(car_at_next_point, side_car_list, side_lane_points, side_d_points)

        if decision == "Lane_change":
            return False
        else:
            return True

    def make_decision(self, grid, lane_points, d_points, right_lane_points, right_d_points, right_car_list,
                      left_lane_points, left_d_points, left_car_list):
        current_road = grid[self.road_id][self.lane_id]
        two_sec_decision = two_sec_rule(self, current_road, lane_points, d_points)
        margin_point = self.speed_limit - (self.speed_limit * .01)

        if self.speed > self.speed_limit or two_sec_decision == "De_accelerate":
            self._Vehicle__decision = "De_accelerate"
            return "De_accelerate"

        elif two_sec_decision == "Lane_change":
            self._Vehicle__decision = self.lane_change(right_lane_points, right_d_points, right_car_list,
                                                       left_lane_points, left_d_points, left_car_list)
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
