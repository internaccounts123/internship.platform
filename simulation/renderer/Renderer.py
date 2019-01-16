import pygame
import os
from common.config_reader import ConfigReader
from simulation.renderer.adapter import Adapter


class Renderer:

    def __init__(self, world, fps=30, screen_width=800, screen_height=800):
        """
        Default constructor
        :param world: world object to draw
        :param fps: frames per second, default value: 30
        :param screen_width: width of screen, default value: 1024
        :param screen_height: height of screen, default value: 720
        """
        self.__FPS = fps
        self.__world = world
        self.__screen_width = screen_width
        self.__screen_height = screen_height

        self.__screen = pygame.display.set_mode((screen_width, screen_height))

        Adapter.calculate_initials(world.world_map)

        try:
            self.__myCar = pygame.image.load(os.path.join(ConfigReader.get_data('base_path'),
                                                          'data/sprites/{}'.format('red_car.png'))).convert_alpha()
        except FileNotFoundError:
            raise UserWarning("Error reading red_car.png file from sprites folder")

        pygame.init()

    def draw_car(self, x, y):
        """

        :param x: int x coordinate
        :param y: int y coordinate
        :return:
        """
        self.__screen.blit(self.__myCar, (x, y))

    def scale_car(self, scale_x, scale_y):
        """
        Change the size of car to scale_x by scale_y
        :param scale_x: width
        :param scale_y: height
        :return:
        """
        self.__myCar = pygame.transform.scale(self.__myCar, (scale_x, scale_y))

    # def draw_road(self, number_of_lanes):
    #     """
    #     Draws road based on number_of_lanes
    #     :param number_of_lanes:
    #     :return:
    #     """
    #     # Width of one lane
    #     lane_width = self.__myCar.get_size()[0] + 20
    #     # x coordinate for road
    #     road_start_x = (self.__screen_width / 2) - (lane_width * (number_of_lanes / 2))
    #     # total width of road(all lanes)
    #     road_width = lane_width * number_of_lanes
    #     # Grey road background
    #     # pygame.draw.rect(screen, color, (x,y,width,height), thickness)
    #     pygame.draw.rect(self.__screen, (204, 204, 204), (road_start_x, 0, road_width, self.__screen_height))
    #
    #     # Lane splitting lines
    #     for i in range(number_of_lanes):
    #         if i > 0:
    #             # pygame.draw.lines(screen, color, closed, pointlist, thickness)
    #             pygame.draw.lines(self.__screen, (255, 255, 255), True,
    #                               [(road_start_x + (lane_width * i), 0), (road_start_x + (lane_width * i), self.__screen_height)],
    #                               5)

    # def draw_road(self, road):
    #
    #     for i in range(len(road)):
    #         print(road[i])
    #
    #         for j in range(len(road[i])):
    #             print(road[i].lanes[j])

    def draw_road(self, road):
        """
        Convert real coordinates to pygame coordinates and draws a road based on the road object passed
        :param road:
        :return:
        """

        # Bottom left coordinate
        road_coordinate_start = road.starting_pos
        road_coordinate_start = Adapter.scaling(road_coordinate_start, [self.__screen_width, self.__screen_height], [0, 0])

        # Top left coordinate
        road_coordinate_end = road.ending_height
        road_coordinate_end = Adapter.scaling(road_coordinate_end, [self.__screen_width, self.__screen_height], [0, 0])

        road_length = Adapter.get_length(road.road_type, road_coordinate_start, road_coordinate_end)

        # Bottom right coordinate
        road_coordinate_start_end_width = road.ending_width
        road_coordinate_start_end_width = Adapter.scaling(road_coordinate_start_end_width, [self.__screen_width, self.__screen_height], [0, 0])

        road_width = Adapter.get_length(road.road_type, road_coordinate_start, road_coordinate_start_end_width)

        # Road Inversion
        road_coordinate_start = Adapter.inversion(road_coordinate_start, self.__screen_height, road_length)
        road_coordinate_end = Adapter.inversion(road_coordinate_end, self.__screen_height, road_length)

        # Grey road background
        grey_color = (204, 204, 204)
        #      pygame.draw.rect(self.__screen, color, (x,y,width,height), thickness)
        pygame.draw.rect(self.__screen, grey_color,
                         (road_coordinate_start, road_coordinate_end, road_width, road_length))

        # Lane / road splitter
        number_of_lanes = len(road.lanes)
        lane_width = road_width / number_of_lanes
        white_color = (255, 255, 255)
        # Lane splitting lines
        for i in range(number_of_lanes):
            if i > 0:
                #       pygame.draw.lines(screen, color, closed, pointlist, thickness)
                pygame.draw.lines(self.__screen, white_color, True,
                                  [(road_coordinate_start + (lane_width * i), 0), (road_coordinate_start + (lane_width * i), road_length)],
                                  5)

    def run_simulation(self):
        """
        Run the main loop of simulation
        :return: playtime in seconds
        """
        clock = pygame.time.Clock()
        mainloop = True
        playtime = 0.0

        # self.draw_road(3)

        # pygame.display.update(self.draw_car(520, road))
        # print("Run simulation")
        while mainloop:
            milliseconds = clock.tick(self.__FPS)  # do not go faster than this frame rate
            playtime += milliseconds / 1000.0

            self.draw_road(self.__world.world_map.roads[0])

            # self.draw_car(520, road)
            pygame.display.update()
            # ----- event handler -----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False  # window closed by user
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False  # user pressed ESC
            pygame.display.set_caption("renderer")

        pygame.quit()
        return playtime
