from simulation.traffic.traffic_creator.traffic_creator import TrafficCreator
from collections import defaultdict
from common.logging.logger import *
from simulation.renderer.adapter import Adapter
import gc


class World(object):

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
    def world_map (self):
        return self.__world_map

    @world_map.setter
    def world_map (self, world_map ):
        self.__world_map = world_map

    def update(self, event):
        for i in range(1000):

            event.wait()
            # extract ys of all cars with lane ids
            # check the difference icluding car width
            for car in self.cars:
                # car.y += 1
                # car.front_point = (car.front_point[0], car.front_point[1] + 1)
                # car.back_point = (car.back_point[0], car.back_point[1] + 1)


                # args = road_type, bearing, intercept
                lane_points, d_points = self.__world_map.get_lane_points(car.road_id, car.lane_id)
                right_lane_points = []
                right_d_points = []
                left_lane_points = []
                left_d_points = []
                # args = self.__world_map.straight_road_info(car.road_id, car.lane_id)

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

                # bearing, grid, lane points
                dec = car.make_decision(self.__grid, lane_points, d_points, right_lane_points,right_d_points,right_car_list, left_lane_points, left_d_points, left_car_list)

                #dec = car.make_decision(args[1], self.__grid, lane_points, d_points)
                Logger.log_cars(car)
                car.move(dec, lane_points, right_lane_points, left_lane_points)

                car.lane_id = self.__world_map.update_lane_info(car.road_id, car.lane_id, dec)

                Logger.log_cars(car)

                if car.front_point[1] >= Adapter.old_max[1]:
                    self.cars.remove(car)
                    #self.__grid[car.road_id][car.lane_id].remove(car)
                self.__grid = self.__update_init_perception()

            Logger.log_end()
            event.clear()
            # time.sleep(0.01)

    # def init_cars(self, type):
    #
    #     for i in range(len(self.data[type])):
    #         arg_list = []
    #
    #         for j in self.data[type][i]:
    #             arg_list.append(self.data[type][i][j])
    #
    #         indx=random.randint(len(map.roads))
    #         arg_list.append(map.roads[indx].name)  #road name
    #
    #
    #         set=0
    #         while (set==0):
    #             id_ = map.roads[indx].lanes[random.randint(len(map.roads[indx].lanes))].id
    #             arg_list.append(id_)  # lane id
    #
    #         width=0
    #         while(map.roads[indx].lanes.id != id_):
    #             width+=map.roads[indx].lanes.width
    #         arg_list.append(width) #x
    #
    #
    #         y= random.randint(map.roads[indx].length)

    # arg_list.append()  # y
    #
    # for j in range(1):
    #     arg_list.append(None)
    #
    # self.rbCars.append(RuleBased(arg_list))
    # self.rbSize += 1

    # function update args[6:] map road grid
