from map.lane import Lane
from map.road import Road
from map.map_class import Map
import json, os
from common.config_reader import ConfigReader
from common.enums.road_types import RoadType
from common.utility.conversions import *
from common.utility.driving.driving_calculations import DrivingCalculations
import copy


class MapCreator:

    @staticmethod
    def create_map():
        """
        Create a map from map file which it will get from ConfigReader
        :return: Map object
        """
        # Get map file name
        # file_name = ConfigReader.get_data('map')[0]

        # For testing delete this when Game class is made
        file_name = "maps.json"

        maps_path = os.path.join(ConfigReader.get_data('base_path'), 'data/map/{}'.format(file_name))
        with open(maps_path, 'r') as f:
            __data = json.load(f)

        data = copy.deepcopy(__data)
        map_id = data["Map_id"]
        map_name = data["Map_Name"]
        map_version = data["Map_Version"]
        roads = MapCreator.create_roads(data["roads"])
        return Map(map_id, map_name, map_version, roads)

    @staticmethod
    def create_roads(roads):
        """
        Create a list of roads from dictionary and return
        : param roads: roads dictionary from the json file
        : return: list of road objects
        """
        road_objects = {}

        for road_id, road in roads.items():
            data = copy.deepcopy(roads[road_id])
            lanes = MapCreator.create_lanes(data["lanes"], data["road_type"], data["starting_pos"],
                                            data["length"], data["bearing"])
            data = roads[road_id]
            road_id = int(road_id)
            road_width = len(lanes)*lanes[1].width
            ending_height, ending_width = MapCreator.__generate_end_points(data["starting_pos"], data["length"],
                                                                           road_width, data["road_type"],
                                                                           data["bearing"])
            road_objects[road_id] = Road(road_id, data["length"], data["name"],
                                         data["road_type"], data["starting_pos"],
                                         ending_height, ending_width, data["bearing"],
                                         data["connection"], lanes)
        return road_objects

    @staticmethod
    def __generate_end_points(starting_position, length, width, road_type, bearing):
        """
        Sample and return lane points based on road type, starting point and length
        : param road_type: type of road/lane
        : param starting_point: starting position of lane/road points
        : param length:
        : return:
        """
        ending_height_x, ending_height_y, ending_width_x, ending_width_y = 0, 0, 0, 0

        if RoadType[road_type].value == RoadType.Straight.value:
            bearing_height = deg2rad(bearing)
            ending_height_x = length * np.cos(bearing_height) + starting_position[0]
            ending_height_x = ending_height_x.astype(int)
            ending_height_y = length * np.sin(bearing_height) + starting_position[1]
            ending_height_y = ending_height_y.astype(int)

            bearing_width = deg2rad(90 - bearing)
            ending_width_x = width * np.cos(bearing_width) + starting_position[0]
            ending_width_x = ending_width_x.astype(int)
            ending_width_y = width * np.sin(bearing_width) + starting_position[1]
            ending_width_y = ending_width_y.astype(int)

        return (ending_height_x, ending_height_y), (ending_width_x, ending_width_y)

    @staticmethod
    def create_lanes(lanes, road_type, starting_position, length, bearing):
        """
        Create a list of lanes from the dictionary and return
        : param lanes: lanes dictionary from the json file
        : param road_type: type of road
        : param starting_position: starting point of lane/road
        : param length: length of road
        : return: list of lanes
        """

        lane_objects = []
        lane_width = lanes["lane_width"]

        for i in range(1, len(lanes)):
            lane_points = MapCreator.__generate_lane_points(starting_position, length, road_type, bearing, lane_width)
            distance_points = DrivingCalculations.generate_distance_points(lane_points)
            starting_position[0] += lane_width  # Subject to change on the basis of renderer meeting
            data = (lanes[str(i)])
            lane_objects.append(Lane(i, data["name"], lane_width, lane_points, distance_points, data["intercept"]))
            lane_objects_dict = {x.id: x for x in lane_objects}
        return lane_objects_dict

    @staticmethod
    def __generate_lane_points(starting_position, length, road_type, bearing, lane_width):
        """
        Sample and return lane points based on road type, starting point and length
        : param road_type: type of road/lane
        : param starting_point: starting position of lane/road points
        : param length:
        : return:
        """
        coordinates = np.array([])
        starting_position_x = starting_position[0] + (lane_width / 2)
        starting_position_y = starting_position[1]
        bearing = deg2rad(bearing)

        if RoadType[road_type].value == RoadType.Straight.value:

            final_x = length * np.cos(bearing) + starting_position_x
            final_y = length * np.sin(bearing) + starting_position_y
            x = np.linspace(starting_position_x, final_x, num=length)
            y = np.linspace(starting_position_y, final_y, num=length)
            coordinates = np.array([x, y]).T
            coordinates = coordinates.astype(int)

        return list(map(lambda x:list(list(map(lambda x:int(x), x))), coordinates))


