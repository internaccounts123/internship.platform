from simulation.vehicle.traffic_creator import TrafficCreator
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
        self.__grid = self.__update_perception()

    def __update_perception(self):
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

                # args = road_type, bearing, intercept
                lane_points, d_points = self.__world_map.get_lane_points(car.road_id, car.lane_id)
                args = self.__world_map.straight_road_info(car.road_id, car.lane_id)

                # bearing, grid, lane points
                decision = car.make_decision(self.__grid, lane_points, d_points)

                Logger.log_cars(car)

                car.move(args[0], args[2], decision, lane_points)

                # car.road_id, car.lane_id = self.world_map.get_road_info([car.x, car.y])
                self.__grid = self.__update_perception()

                Logger.log_cars(car)

                if car.front_point[1] >= Adapter.old_max[1]:
                    self.cars.remove(car)
                    self.__grid[car.road_id][car.lane_id].remove(car)

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
