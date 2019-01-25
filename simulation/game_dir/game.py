import threading
import time
from common.config_reader import ConfigReader
from map.map_creator import MapCreator
from server.server import My_server
from simulation.renderer.renderer import Renderer
from simulation.world.world import World


class Game:

    def __init__(self):
        ConfigReader()
        self.__map = MapCreator.create_map()  # Map(map_id, name, version, roads)
        self.__world = World(self.__map, 1)

        if ConfigReader.get_data('renderer')[0] == 'web':
            self.s = My_server()
            print("server running")
            self.s.run_server()
        else:
            self.__renderer = Renderer(self.__world)

    def run(self):
        # for i in range(1000):
        event = threading.Event()
        threading.Thread(target=self.world.update, args=(event,)).start()
        # time.sleep(0.5)

        if ConfigReader.get_data('renderer')[0] == 'web':
            while True:

                data_to_send = self.world.serialize
                time.sleep(0.1)
                print("sending data")
                self.s.send_data("FRAME", data_to_send)
                event.set()

        else:
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
