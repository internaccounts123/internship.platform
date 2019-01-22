from simulation.vehicle.vehicle import Vehicle
from common.config_reader import ConfigReader
from common.enums.decisions import Decisions
from common.utility.conversions import *
from common.utility.driving.angle_calculator import *
from common.utility.driving.driving_calculations import *


class RuleBased(Vehicle):

    def __init__(self, perception_size, speed_limit, acceleration, de_acceleration, length, type1):
        super(RuleBased, self).__init__(perception_size, speed_limit, acceleration, de_acceleration, length, type1)

    def move(self, road_type, intercept, decision, lane_points):

        _neigh_1, _neigh_2 = get_neighbouring_points(lane_points, [self.x, self.y])
        bearing = AngleCalculator.get_bearing(_neigh_1, _neigh_2)

        if Decisions[decision].value == Decisions.Accelerate.value:
            self.speed = (self.acceleration * (1.0/ConfigReader.get_data("fps")[0])) + self.speed
            self.x = self.x + self.speed * np.cos(bearing)
            self.y = self.y + self.speed * np.sin(bearing)

        elif Decisions[decision].value == Decisions.Constant_speed.value:
            self.x = self.x + self.speed*np.cos(bearing)
            self.y = self.y + self.speed * np.sin(bearing)

        elif Decisions[decision].value == Decisions.De_accelerate.value:
            self.speed = (self.de_acceleration * (1.0/ConfigReader.get_data("fps")[0])) + \
                                   self.speed
            self.x = self.x + self.speed * np.cos(bearing)
            self.y = self.y + self.speed * np.sin(bearing)

        elif Decisions[decision].value == Decisions.Move_right.value:
            distance = point_to_line(road_type, (self.x, self.y), bearing, intercept)
            self.x = self.x + distance

        self.front_point = (self.x, self.y + (self.car_length / 2.0))
        self.back_point = (self.x, self.y - (self.car_length / 2.0))

    def __two_sec_rule(self, bearing, car_list, lane_points):
        # ASSUMING BEARING -> map.calculate_bearing
        # # v^2 = u^2 +2as
        # # 2as = u^2
        # # s = u^2/2a deg2r
        if len(car_list) == 1:
            return False

        # bearing = deg2rad(bearing)
        c = []
        dis = []
        for car in car_list:

            if car.id != self.id:
                _neigh_1, _neigh_2 = get_neighbouring_points(lane_points, [self.x, self.y])
                angle = AngleCalculator.calculate_angle(lane_points, [self.x, self.y], [car.x, car.y], _neigh_1, _neigh_2)

                if AngleCalculator.is_forward(angle):
                    c.append(car)
                    dis.append(np.linalg.norm(np.array([car.x, car.y]) - np.array([self.x, self.y])))

        if len(c) == 0 :
            return False
        immediate_car = c[np.argmin(np.array(dis))]

        _neigh_1, _neigh_2 = get_neighbouring_points(lane_points, [self.x, self.y])
        bearing = AngleCalculator.get_bearing(_neigh_1, _neigh_2)
        s = (np.square(self.speed)) / (2.0 * self.de_acceleration)
        s += self.car_length
        x = self.x + s * np.cos(bearing)
        y = self.y + s * np.sin(bearing)

        _neigh_1, _neigh_2 = get_neighbouring_points(lane_points, [x, y])
        _angle = AngleCalculator.calculate_angle(lane_points, [x, y], [immediate_car.x, immediate_car.y], _neigh_1, _neigh_2)

        if AngleCalculator.is_forward(_angle):
            # car is ahead of the point
            return False
        # De_accelerate
        return True

    def make_decision(self, bearing, grid, lane_points):
        current_road = grid[self.road_id][self.lane_id]

        if self.speed > self.speed_limit:
            self._Vehicle__decision = "De_accelerate"
            return "De_accelerate"
        elif self.__two_sec_rule(bearing, current_road, lane_points):
            self._Vehicle__decision = "De_accelerate"
            return "De_accelerate"
        elif self.speed == self.speed_limit:
            self._Vehicle__decision = "Constant_speed"
            return "Constant_speed"
        elif self.speed < self.speed_limit:
            self._Vehicle__decision = "Accelerate"
            return "Accelerate"
