from map.map_creator import MapCreator
from simulation.World.world import World
from simulation.renderer.Renderer import Renderer
from common.config_reader import ConfigReader


class Game:

    def __init__(self):
        ConfigReader()
        self.__map = MapCreator.create_map()  # Map(map_id, name, version, roads)
        self.__world = World(self.__map, 1)
        self.__renderer = Renderer(self.__world)

    def run(self):
        self.renderer.run_simulation()

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

