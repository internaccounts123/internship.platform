from simulation.game_dir.game import Game
from common.logger_class import Logger
if __name__ == '__main__':
    g = Game()
    g.run()
    g.world.log_map()
    g.world.log_cars()

    # for i in range(0, 17):
    #     print(g.world.cars[i].id, g.world.cars[i].x, g.world.cars[i].y, g.world.cars[i].front_point,
    #           g.world.cars[i].back_point)
    #     print("\n")

        # print(g.map1.roads[i].name)
        # print(g.map1.roads[i].starting_pos)
        # print(g.map1.roads[i].ending_height)
        # print(g.map1.roads[i].ending_width)

        # for j in range(0, 3):
        #     print("\n\n")
        #     print(g.map1.roads[i].lanes[j].lane_points)

