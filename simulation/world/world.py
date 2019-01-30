from simulation.traffic.traffic_creator.traffic_creator import TrafficCreator
from collections import defaultdict
from common.logging.logger import *
from simulation.renderer.adapter import Adapter
import gc


class World:

    def __init__(self, map1, _id):
        self.__id = _id
        self.__world_map = map1  # Map(map_id, name, version, roads)
        self.__cars = TrafficCreator.create_traffic(map1, self.__id)
        self.__grid = []
        self.__grid = self.__update_init_perception()

    def __update_init_perception(self):
        del self.__grid
        gc.collect()

        _grid = defaultdict(lambda: defaultdict(lambda: []))
        for car in self.__cars:
            _grid[car.road_id][car.lane_id].append(car)
        return _grid

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, _id):
        self.__id = _id

    @property
    def cars(self):
        return self.__cars

    @cars.setter
    def cars(self, cars):
        self.__cars = cars

    @property
    def world_map(self):
        return self.__world_map

    @world_map.setter
    def world_map(self, world_map):
        self.__world_map = world_map

    @property
    def serialize(self):
        return {
            'id': self.id,
            'world_map': self.world_map.serialize,
            'cars': list(car.serialize for car in self.cars)

        }

    def update(self, event=None):
        log = Logger.get_logger("FILE")
        for i in range(1000):

            event.wait()
            # extract ys of all cars with lane ids
            # check the difference including car width
            for car in self.cars:

                lane_points, d_points = self.__world_map.get_lane_points(car.road_id, car.lane_id)
                right_lane_points = []
                right_d_points = []
                left_lane_points = []
                left_d_points = []

                if self.world_map.is_last_lane_id(car.road_id, car.lane_id):
                    right_car_list = []
                else:
                    right_car_list = self.__grid[car.road_id][car.lane_id + 1]
                    right_lane_points, right_d_points = self.__world_map.get_lane_points(car.road_id, car.lane_id + 1)

                if self.world_map.is_first_lane_id(car.road_id, car.lane_id):
                    left_car_list = []
                else:
                    left_car_list = self.__grid[car.road_id][car.lane_id - 1]
                    left_lane_points, left_d_points = self.__world_map.get_lane_points(car.road_id, car.lane_id - 1)

                dec = car.make_decision(self.__grid, lane_points, d_points, right_lane_points, right_d_points,
                                        right_car_list, left_lane_points, left_d_points, left_car_list)

                log_information = car.get_info()
                log.info(log_information)

                car.move(dec, lane_points, right_lane_points, left_lane_points)

                car.lane_id = self.__world_map.update_lane_info(car.road_id, car.lane_id, dec)
                old_min, old_max = self.__world_map.calculate_initials()

                if car.front_point[1] >= old_max[1]:
                    self.cars.remove(car)

                self.__grid = self.__update_init_perception()

            event.clear()
