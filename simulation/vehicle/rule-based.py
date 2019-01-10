from simulation.vehicle.vehicle import Vehicle


class RuleBased(Vehicle):

    def __init__(self, name, color, car_length, car_width, road, x, y, lane, perception):
        super(RuleBased, self).__init__(name, color, car_length, car_width, road, x, y, lane, perception)
        pass

    #  def move(self):
    #  self.x = self.x + self.speed
