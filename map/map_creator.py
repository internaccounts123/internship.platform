from map.lane import Lane
from map.road import Road
from map.map_class import Map
import json
import numpy as np


class MapCreator:

    @staticmethod
    def create_map():
        """
        Create a map from map file which it will get from ConfigReader
        :return: Map object
        """

        # TODO: Implement this after game class is done
        # Get map file name
        # file_name = ConfigReader.get_data('map')[0]

        # For testing delete this when Game class is made
        file_name = "maps.json"

        with open("../data/map/" + file_name) as f:
            data = json.load(f)

        map_id = data["Map_id"]
        map_name = data["Map_Name"]
        map_version = data["Map_Version"]
        roads = MapCreator.__create_roads(data["roads"])
        return Map(map_id, map_name, map_version, roads)

    @staticmethod
    def __create_roads(roads):
        """
        Create a list of roads from dictionary and return
        : param roads: roads dictionary from the json file
        : return: list of road objects
        """
        road_objects = []

        for i in list(roads):
            data = roads[str(i)]
            lanes = MapCreator.__create_lanes(data["lanes"], data["road_type"], data["starting_pos"],
                                              data["length"], data["bearing"])

            road_objects.append(Road(data["length"], data["name"], data["road_type"], data["starting_pos"],
                                data["bearing"], data["connection"], lanes))

        return road_objects

    @staticmethod
    def __create_lanes(lanes, road_type, starting_position, length, bearing):
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
            data = lanes[str(i)]
            lane_points = MapCreator.__generate_lane_points(starting_position, length, road_type, bearing, lane_width)
            starting_position[1] += lane_width  # Subject to change on the basis of renderer meeting
            lane_objects.append(Lane(i, data["name"], lane_width, lane_points))
        return lane_objects

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

        if road_type == "Straight":

            starting_position_x = starting_position[0] + (lane_width/2)
            starting_position_y = starting_position[1] + (lane_width/2)
            final_x = length * np.cos(bearing) + starting_position_x
            final_y = length * np.sin(bearing) + starting_position_y
            x = np.linspace(starting_position_x, final_x, num=length)
            y = np.linspace(starting_position_y, final_y, num=length)
            coordinates = np.array([x, y]).T
            coordinates = coordinates.astype(int)

        return coordinates
