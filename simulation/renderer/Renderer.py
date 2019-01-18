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

        Adapter.calculate_initials(world.world_map, screen_width, screen_height)

        try:
            self.__myCar = pygame.image.load(os.path.join(ConfigReader.get_data('base_path'),
                                                          'data/sprites/{}'.format('red_car.png'))).convert_alpha()
        except FileNotFoundError:
            raise UserWarning("Error reading red_car.png file from sprites folder")

        pygame.init()

    def draw_car(self, front_point, back_point, road_width, no_of_lanes):
        """
        :param front_point: car front point
        :param back_point: car back point
        :param road_width: scaled road width
        :param no_of_lanes: number of lanes in the road
        :return: None
        """
        self.__myCar = pygame.image.load(os.path.join(ConfigReader.get_data('base_path'),
                                                      'data/sprites/{}'.format('red_car.png'))).convert_alpha()

        # Scaling
        front_coordinate = Adapter.scaling([front_point[0], front_point[1]])
        back_coordinate = Adapter.scaling([back_point[0], back_point[1]])

        car_length = Adapter.get_length("Straight", list(front_coordinate), list(back_coordinate))

        car_width = int((road_width / float(no_of_lanes)) * 0.6)

        # Inversion
        # front_coordinate = Adapter.inversion(front_coordinate, self.__screen_height, car_length)
        back_coordinate = Adapter.inversion(back_coordinate, self.__screen_height, car_length)

        # Scaling Car
        self.scale_car(car_width, car_length)

        # Draw Car
        self.__screen.blit(self.__myCar, ((back_coordinate[0]-(car_width/2)), back_coordinate[1]))

    def scale_car(self, scale_w, scale_h):
        """
        Change the size of car to scale_x by scale_y
        :param scale_w: width
        :param scale_h: height
        :return:
        """
        self.__myCar = pygame.transform.scale(self.__myCar, (int(scale_w), int(scale_h)))

    def draw_road(self, road):
        """
        Convert real coordinates to pygame coordinates and draws a road based on the road object passed
        :param road:
        :return: scaled road width
        """

        # Bottom left coordinate
        road_coordinate_start = road.starting_pos
        road_coordinate_start = Adapter.scaling(road_coordinate_start)

        # Top left coordinate
        road_coordinate_end = road.ending_height
        road_coordinate_end = Adapter.scaling(road_coordinate_end)

        road_length = Adapter.get_length(road.road_type, road_coordinate_start, road_coordinate_end)

        # Bottom right coordinate
        road_coordinate_start_end_width = road.ending_width
        road_coordinate_start_end_width = Adapter.scaling(road_coordinate_start_end_width)

        road_width = Adapter.get_length(road.road_type, road_coordinate_start, road_coordinate_start_end_width)

        # Road Inversion
        road_coordinate_start = Adapter.inversion(road_coordinate_start, self.__screen_height, road_length)
        road_coordinate_end = Adapter.inversion(road_coordinate_end, self.__screen_height, road_length)

        # Grey road background
        grey_color = (204, 204, 204)
        #      pygame.draw.rect(self.__screen, color, (x,y,width,height), thickness)
        pygame.draw.rect(self.__screen, grey_color,
                         (road_coordinate_start[0], road_coordinate_start[1], road_width, road_length))

        # Lane / road splitter
        number_of_lanes = len(road.lanes)
        lane_width = road_width / number_of_lanes
        white_color = (255, 255, 255)
        # Lane splitting lines
        for i in range(number_of_lanes):
            if i > 0:
                #       pygame.draw.lines(screen, color, closed, pointlist, thickness)
                pygame.draw.lines(self.__screen, white_color, True,
                                  [(road_coordinate_start[0] + (lane_width * i), road_coordinate_start[1]),
                                   (road_coordinate_end[0] + (lane_width * i), road_coordinate_end[1])], 5)

        return road_width

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
            self.__screen.fill([255, 255, 255])
            milliseconds = clock.tick(self.__FPS)  # do not go faster than this frame rate
            playtime += milliseconds / 1000.0

            road_width = self.draw_road(self.__world.world_map.roads[0])

            for car in self.__world.cars:
                if car.road_id == self.__world.world_map.roads[0].road_id:
                    self.draw_car(car.front_point, car.back_point, road_width,
                                  len(self.__world.world_map.roads[0].lanes))

            pygame.display.update()
            # ----- event handler -----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False  # window closed by user
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False  # user pressed ESC

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event)
                    print(event.type)

                    if event.button == 4:
                        pass
                        # Adapter.zoom_in(self.__screen_width, self.__screen_height)

                    elif event.button == 5:
                        pass
                        # Adapter.zoom_out(self.__screen_width, self.__screen_height)

            pygame.display.set_caption("renderer")

        pygame.quit()
        return playtime
