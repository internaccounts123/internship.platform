class Vehicle(object):

    def __init__(self, args):

        self.name = args[0]
        self.speed = args[1]
        self.color = args[2]
        self.baring = args[3]
        self.carLength = args[4]
        self.carWidth = args[5]
        self.id = args[6]
        self.road = args[7]

        self.x = args[7]
        self.y = args[8]
        self.lane = args[9]

        self.perception = args[11]

    # def move(self):
    #     raise NotImplementedError('subclasses must override')

    # def update_grid(self, grid):
    #     self.grid = grid
