from simulation.game_dir.game import Game
import numpy as np
if __name__ == '__main__':
    g = Game()
    g.run()
    # lane_points = None
    # distance_points = None
    # for road in range(len(g.map1.roads)):
    #     for lane in range(len(g.map1.roads[road].lanes)):
    #         lane_points = g.map1.roads[road].lanes[lane].lane_points
    #         distance_points = g.map1.roads[road].lanes[lane].distance_points
    #         break
    #     print()
    #     break

