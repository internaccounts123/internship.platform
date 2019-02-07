from common.enums.decisions import Decisions
from common.utility.driving.driving_calculations import DrivingCalculations
from simulation.work_flows.decision_workflow.decision_workflow import DecisionWorkFlow


class RuleBasedDecisionWorkFlow(DecisionWorkFlow):

    def __init__(self):
        super().__init__()

    def __get_decision_arguments(self, __world_map, __grid):

        car = self.car
        grid = __grid
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

        return grid, lane_points, d_points,  right_lane_points, right_d_points, left_lane_points\
            , left_d_points, left_car_list, right_car_list

    def make_decision(self, __grid, __world_map):

        grid, lane_points, d_points, right_lane_points, right_d_points,\
        left_lane_points, left_d_points, left_car_list, right_car_list = self.__get_decision_arguments(__world_map, __grid)
        grid = __grid
        current_road = grid[self.car.road_id][self.car.lane_id]
        two_sec_decision = DrivingCalculations.two_sec_rule(self.car, current_road, lane_points, d_points)
        margin_point = DrivingCalculations.get_margin_point(self.car)

        if self.car.speed > self.car.speed_limit or two_sec_decision == Decisions.De_accelerate:
            self.car.decision = Decisions.De_accelerate
            return Decisions.De_accelerate

        elif two_sec_decision == Decisions.Lane_change:
            self.car.decision = DrivingCalculations.predict_lane_change(self.car, right_lane_points, right_d_points, right_car_list,
                                                                        left_lane_points, left_d_points, left_car_list)
            return self.car.decision

        if two_sec_decision == Decisions.No_obstructions_ahead:

            if margin_point <= self.car.speed <= self.car.speed_limit:
                self.car.decision = Decisions.Constant_speed
                return Decisions.Constant_speed
            elif self.car.speed < margin_point:
                self.car.decision = Decisions.Accelerate
                return Decisions.Accelerate

