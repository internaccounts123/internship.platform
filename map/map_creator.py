from map.lane import Lane
from map.road import Road
from map.map import Map
import json


class MapCreator:


    @staticmethod
    def create_map(self):
        """
        Create a map from map file which it will get from ConfigReader
        :param self:
        :return: Map object
        """
        # Get map file name
        # file_name = ConfigReader.get_value("map")

        file_name = "maps.json"

        with open(file_name) as f:

            data = json.load(f)

        map_id = data["Mapid"]
        map_name = data["MapName"]
        map_version = data["MapVersion"]
        roads = self.__create_roads(data["roads"])
        return Map(map_id, map_name, map_version, roads)



    @staticmethod
    def __create_roads(self, roads):
        """
        Create a list of roads from dictionary and return
        :param self:
        :param roads: roads dictionary from the json file
        :return: list of road objects
        """
        road_objects = []

        for i in list(roads):
            data = roads[str(i)]
            lanes = self.__create_lanes(data["lanes"], data["roadtype"], data["starting_pos"], data["length"])

            road_objects.append(Road(data["length"], data["name"], data["roadtype"], data["starting_pos"], data["bearing"], data["connection"], lanes))

        return road_objects


    @staticmethod
    def __create_lanes(self, lanes, road_type, starting_position, length):
        """
        Create a list of lanes from the dictionary and return
        :param self:
        :param lanes: lanes dictionary from the json file
        :param road_type: type of road
        :param starting_position: starting point of lane/road
        :param length: length of road
        :return: list of lanes
        """
        lanes_objects = []

        for i in list(lanes):
            data = lanes[str(i)]
            lane_points = self.generate_lane_points(road_type, starting_position, length)
            lanes_objects.append(Lane(data["name"], data["width"], lane_points))
        return lanes_objects

    @staticmethod
    def generate_lane_points(self, road_type, starting_point, length):
        """
        Sample and return lane points based on road type, starting point and length
        :param self:
        :param road_type: tpye of road/lane
        :param starting_point: starting position of lane/road points
        :param length:
        :return:
        """
        return [1,2,3]

