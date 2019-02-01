
from simulation.traffic.vehicle.vehicle_class import Vehicle


class RuleBased(Vehicle):

    def __init__(self, perception_size, speed_limit, acceleration, de_acceleration, length, type1):
        self.__decision_workflow = "none"
        super(RuleBased, self).__init__(perception_size, speed_limit, acceleration, de_acceleration, length, type1)
