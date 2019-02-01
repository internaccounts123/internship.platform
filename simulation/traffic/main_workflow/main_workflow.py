
class MainWorkFlow:
    def __init__(self):
        self.__self_car = None
        self.__decision_work_flow = None
        self.__driving_work_flow = None

    @property
    def self_car(self):
        return self.__self_car

    @self_car.setter
    def self_car(self, self_car):
        self.__self_car = self_car

    @property
    def decision_work_flow(self):
        return self.__decision_work_flow

    @decision_work_flow.setter
    def decision_work_flow(self, a):
        self.__decision_work_flow = a

    @property
    def driving_work_flow(self):
        return self.__driving_work_flow

    @driving_work_flow.setter
    def driving_work_flow(self, a):
        self.__driving_work_flow = a


    def play_car_step(self, __grid, __world_map):

        car = self.self_car
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
        dec = self.__decision_work_flow.make_decision(__grid, lane_points, d_points, right_lane_points,
                                                   right_d_points,
                                                   right_car_list, left_lane_points, left_d_points, left_car_list)

        car.lane_id = __world_map.update_lane_info(car.road_id, car.lane_id, dec)

        self.__driving_work_flow.implement_decision(dec, lane_points, right_lane_points, left_lane_points)
