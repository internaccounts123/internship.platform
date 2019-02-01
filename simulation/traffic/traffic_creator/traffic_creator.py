from common.config_reader import ConfigReader
from simulation.traffic.decision_workflow.rule_based_decision_workflow.rule_based_decision_workflow import \
    RuleBasedDecisionWorkFlow
from simulation.traffic.driving_workflow.rule_based_driving_workflow.rule_based_driving_workflow import RuleBasedDrivingWorkflow
from simulation.traffic.main_workflow.main_workflow import MainWorkFlow
from simulation.traffic.vehicle.rule_based.rule_based import RuleBased
from common.enums.model_types import ModelTypes
import random
from common.utility.conversions import deg2rad
from common.enums.road_types import RoadType
from common.utility.driving.driving_calculations import DrivingCalculations
from common.utility.driving.angle_calculator import AngleCalculator
import numpy as np


class TrafficCreator(object):

    __traffic = []

    @staticmethod
    def create_traffic(map1, world_id):

        # names of models
        model_names = list(ConfigReader.get_data("driving.traffic.driver_profile_type")[0].keys())

        taken = []
        ind_x = 1
        for model_name in model_names:

            # percentage share of each model in traffic
            model_percentage = ConfigReader.get_data("driving.traffic.driver_profile_type." + model_name +
                                                     ".model_percentage")[0]

            for type_name in ConfigReader.get_data("driving.traffic.driver_profile_type." + model_name +
                                                   ".type_percentages")[0].keys():

                # percentage share of each type of a specific model in traffic
                type_percentage = ConfigReader.get_data("driving.traffic.driver_profile_type." + model_name +
                                                        ".type_percentages." + type_name)[0]

                # vehicle_creator(percentage, type1, model_name)
                vehicles = TrafficCreator.vehicle_creator(type_percentage * model_percentage, type_name, model_name)

                for v in vehicles:
                    v.id = (1000 * world_id) + ind_x
                    v = TrafficCreator.set_position(v, map1, taken)
                    TrafficCreator.__traffic.append(v)
                    ind_x += 1

        return TrafficCreator.__traffic

    @staticmethod
    def set_position(v, map1, taken):
        """
        :param v: Vehicle not assigned a position
        :param map1: full map
        :param taken: already allotted points
        :return: traffic with assigned initial position
        """

        tup = None
        _do = True
        road_idx = None
        lane_idx = None
        xy_id = None
        lane_points = []
        car_length = v.car_length



        # choose a point where a car is not already present
        while (TrafficCreator.__is_tuple_valid(tup, taken, lane_points, xy_id, car_length, map1,
                                               road_idx, lane_idx) is False) or (_do is True):
            _do = False
            road_idx = 1
            lane_idx = random.randint(1, len(map1.roads[road_idx].lanes)-1)

        # pick random points from list of possible lane points
            __road = map1.roads[road_idx]

            lane_points = TrafficCreator.generate_lane_points(__road.starting_pos, __road.length, __road.road_type,
                                                              __road.bearing, __road.lanes[lane_idx].width,
                                                              __road.lanes[lane_idx].id)

            xy_id = random.randint((v.car_length/2.0), (len(lane_points) - (v.car_length/2.0))-1)
            tup = (map1.roads[road_idx].road_id, map1.roads[road_idx].lanes[lane_idx].id, lane_points[xy_id][1])

        neigh_1, neigh_2 = DrivingCalculations.get_neighbouring_points(lane_points, lane_points[xy_id])
        bearing = AngleCalculator.get_bearing(neigh_1[0], neigh_2[0])

        lower_limit, upper_limit = DrivingCalculations.get_limits(xy_id, lane_points, v.car_length, bearing)


        # taken points by this car
        points = DrivingCalculations.points_in_range(lane_points, upper_limit, lower_limit)

        # remove taken points by this car
        for p in points:
            tup = (map1.roads[road_idx].road_id, map1.roads[road_idx].lanes[lane_idx].id, p[1])
            taken.append(tup)

        # set car attributes
        v.road_id = map1.roads[road_idx].road_id
        v.lane_id = map1.roads[road_idx].lanes[lane_idx].id
        v.x = lane_points[xy_id][0]
        v.y = lane_points[xy_id][1]
        v.front_point = (upper_limit[0], upper_limit[1])
        v.back_point = (lower_limit[0], lower_limit[1])
        return v

    @staticmethod
    def __is_tuple_valid(tup, taken, lane_points, xy_id, car_length, map1, road_idx, lane_idx):
        """
        :param tup: (road id, lane id, y-coordinate)
        :param taken: list of already taken tup
        :param lane_points: possible generated lane points of a road
        :param xy_id: index of selected lane_point
        :param car_length: length of car
        :param map1: map object
        :param road_idx:  index of selected road
        :param lane_idx:  index of selected lane
        :return: bool
        """
        _taken = taken.copy()
        if (tup is not None) and (len(taken) != 0):
            neigh_1, neigh_2 = DrivingCalculations.get_neighbouring_points(lane_points, lane_points[xy_id])
            bearing = AngleCalculator.get_bearing(neigh_1[0], neigh_2[0])

            lower_limit,  upper_limit= DrivingCalculations.get_limits(xy_id, lane_points, car_length, bearing)


            # taken points by this car
            #points_in_range(lane_points, upper_limit, lower_limit)
            points = DrivingCalculations.points_in_range(lane_points, upper_limit, lower_limit)

            for p in points:
                p_tup = (map1.roads[road_idx].road_id, map1.roads[road_idx].lanes[lane_idx].id, p[1])
                if p_tup in taken:
                    return False
            return True
        else:
            return True

    @staticmethod
    def vehicle_creator(percentage, type1, model_name):

        vehicles = []
        for i in range(int(ConfigReader.get_data("driving.traffic.traffic_amount")[0] * percentage)):
            if ModelTypes[model_name].value == ModelTypes.Rule_based.value:
                vehicle = RuleBased(ConfigReader.get_data("driving." + type1 + ".perception_size")[0],
                                          ConfigReader.get_data("driving." + type1 + ".speed_limit")[0],
                                          ConfigReader.get_data("driving." + type1 + ".acceleration")[0],
                                          ConfigReader.get_data("driving." + type1 + ".de_acceleration")[0],
                                          ConfigReader.get_data("driving." + type1 + ".length")[0], type1)

                main_work_flow = MainWorkFlow()
                main_work_flow.self_car = vehicle

                vehicle.main_work_flow = main_work_flow

                decision_work_flow = RuleBasedDecisionWorkFlow()
                decision_work_flow.self_car = vehicle

                vehicle.main_work_flow.decision_work_flow = decision_work_flow

                driving_work_flow = RuleBasedDrivingWorkflow()
                driving_work_flow.self_car = vehicle
                vehicle.main_work_flow.driving_work_flow = driving_work_flow
                vehicles.append(vehicle)

        return vehicles

    @property
    def traffic(self):
        return TrafficCreator.__traffic

    @traffic.setter
    def traffic(self, traffic):
        TrafficCreator.__traffic = traffic

    @staticmethod
    def generate_lane_points(starting_position, length, road_type, bearing, lane_width, lane_id):
        """
        Sample and return lane points based on road type, starting point and length
        : param road_type: type of road/lane
        : param starting_point: starting position of lane/road points
        : param length:
        : return:
        """

        coordinates = np.array([])
        starting_position_x = lane_width*(lane_id-1) + (lane_width / 2.0)
        starting_position_y = starting_position[1]
        bearing = deg2rad(bearing)

        if RoadType[road_type].value == RoadType.Straight.value:

            final_x = length * np.cos(bearing) + starting_position_x
            final_y = length * np.sin(bearing) + starting_position_y
            x = np.linspace(starting_position_x, final_x, num=length)
            y = np.linspace(starting_position_y, final_y, num=length)
            coordinates = np.array([x, y]).T


        return coordinates


