from map.map_creator import MapCreator
from simulation.world.world import World
from simulation.renderer.renderer import Renderer
from common.config_reader import ConfigReader

from server.server import My_server

import threading, time
import json


class Game:

    def __init__(self):
        ConfigReader()
        self.__map = MapCreator.create_map()  # Map(map_id, name, version, roads)
        self.__world = World(self.__map, 1)
        # self.__renderer = Renderer(self.__world)
        # print(self.world.world_map.roads[0].starting_pos)
        # print(self.world.cars)

        s = My_server()

        s.run_server()

        print("server running")

        data_to_send = self.world.serialize
        # print(json.dumps(data_to_send))
        string_data = str(data_to_send)
        string_data = string_data.replace('\'', '\"')
        # print(string_data)

        time.sleep(11)
        s.send_data("FRAME", data_to_send)
        while True:

            # print(self.world.world_map.roads[0].starting_pos)
            # print(self.world.cars)
            data_to_send = self.world.serialize
            print("sending data...")
            print(data_to_send)
            s.send_data("FRAME", data_to_send)
            self.__world.update()
            time.sleep(0.1)

    def run(self):
        # for i in range(1000):
        event = threading.Event()
        threading.Thread(target=self.world.update, args=(event,)).start()
        # time.sleep(0.5)
        self.renderer.run_simulation(event)
        # time.sleep(0.5)

    @property
    def map1(self):
        return self.__map

    @map1.setter
    def map1(self, _map):
        self.__map = _map

    @property
    def world(self):
        return self.__world

    @world.setter
    def world(self, world):
        self.__world = world

    @property
    def renderer(self):
        return self.__renderer

    @renderer.setter
    def renderer(self, renderer):
        self.__renderer = renderer
