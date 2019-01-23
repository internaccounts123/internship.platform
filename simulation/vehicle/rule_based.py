from simulation.vehicle.vehicle import Vehicle
from common.config_reader import ConfigReader
from common.enums.decisions import Decisions
from common.utility.conversions import *
from common.utility.driving.angle_calculator import *
from common.utility.driving.driving_calculations import *


class RuleBased(Vehicle):

    def __init__(self, perception_size, speed_limit, acceleration, de_acceleration, length, type1):
        super(RuleBased, self).__init__(perception_size, speed_limit, acceleration, de_acceleration, length, type1)
    #
    # def move(self, road_type, intercept, decision, lane_points):
    #     pass

    def __two_sec_rule(self, bearing, car_list, lane_points, distance_points):
        # ASSUMING BEARING -> map.calculate_bearing
        # # v^2 = u^2 +2as
        # # 2as = u^2
        # # s = u^2/2a deg2r
        # if len(car_list) == 1:
        #     self.current_acc = self.acceleration
        #     return False
        # bearing = deg2rad(bearing)

        c = []
        dis = []
        for car in car_list:

            if car.id != self.id:
                _neigh_1, _neigh_2 = get_neighbouring_points(lane_points, [self.x, self.y])
                angle = AngleCalculator.calculate_angle(lane_points, [self.x, self.y], [car.x, car.y], _neigh_1[0], _neigh_2[0])

                if AngleCalculator.is_forward(angle):
                    c.append(car)
                    dis.append(np.linalg.norm(np.array([car.x, car.y]) - np.array([self.x, self.y])))

        if len(c) == 0:
            self.current_acc = self.acceleration
            self.extra = (self.current_acc, "no immediate car", "no immediate car")
            return False

        immediate_car = c[np.argmin(np.array(dis))]

        self_neigh_1, self_neigh_2 = get_neighbouring_points(lane_points, [self.x, self.y])
        imm_neigh_1,imm_neigh_2 = get_neighbouring_points(lane_points, [immediate_car.x, immediate_car.y])
        distance_between_me_and_immediate_car = np.abs(distance_points[imm_neigh_1[1]] - distance_points[self_neigh_1[1]])
        #distance_two_sec_rule = (self.speed * (2.0)) + self.car_length + 1
        distance_two_sec_rule = (self.speed * (2.0)) + ((1/2.0) * self.acceleration * np.square(2)) + self.car_length + 1
        if distance_between_me_and_immediate_car < distance_two_sec_rule:
            if distance_between_me_and_immediate_car > 0:
                self.current_acc = (np.square(immediate_car.speed) - np.square(self.speed)) / float(
                    2 * distance_between_me_and_immediate_car)

                if self.current_acc > -1:
                    self.current_acc = -1.0

            else:
                self.current_acc = 0

            self.extra = (self.current_acc, distance_between_me_and_immediate_car, distance_two_sec_rule)
            # "De_accelerate"
            return True
        else:
            self.current_acc = self.acceleration
            self.extra = (self.current_acc, distance_between_me_and_immediate_car, distance_two_sec_rule)
            return False

        # acc = (np.square(immediate_car.speed) - np.square(self.speed))/float(2 * s)
        # bearing = AngleCalculator.get_bearing(_neigh_1, _neigh_2)
        # s = (np.square(self.speed)) / (2.0 * self.de_acceleration)
        # s += self.car_length
        # x = self.x + s * np.cos(bearing)
        # y = self.y + s * np.sin(bearing)
        # _neigh_1, _neigh_2 = get_neighbouring_points(lane_points, [x, y])
        # _angle = AngleCalculator.calculate_angle(lane_points, [x, y],
        # [immediate_car.x, immediate_car.y], _neigh_1, _neigh_2)
        # self.extra= (s, x, y, _angle,bearing)
        # if AngleCalculator.is_forward(_angle):
        #     # car is ahead of the point
        #     return False
        # # De_accelerate
        # return True

    def make_decision(self, bearing, grid, lane_points, d_points):
        current_road = grid[self.road_id][self.lane_id]
        margin_point = self.speed_limit - (self.speed_limit * .01)

        if self.speed > self.speed_limit or self.__two_sec_rule(bearing, current_road, lane_points, d_points):
            self._Vehicle__decision = "De_accelerate"
            return "De_accelerate"
            # self._Vehicle__decision = "De_accelerate"
            # return "De_accelerate"
        elif margin_point <= self.speed <= self.speed_limit:
            self._Vehicle__decision = "Constant_speed"
            return "Constant_speed"
        elif self.speed < margin_point:
            self._Vehicle__decision = "Accelerate"
            return "Accelerate"
