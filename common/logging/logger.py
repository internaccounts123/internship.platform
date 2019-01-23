import logging
from time import gmtime, strftime
import datetime


class Logger:

    def __init__(self):
        """

        """

    """
     A function to log all information about cars to traffic.log and also to the console
    """
    @staticmethod
    def log_cars(car):
        logging.basicConfig(filename='traffic.log', filemode='w', level=logging.DEBUG)

        current_time = datetime.datetime.now()
        #logging.getLogger().addHandler(logging.StreamHandler())
        car_id = car.id
        car_speed_limit = car.speed_limit
        car_x = car.x
        car_y = car.y

        car_road = car.road_id
        car_lane = car.lane_id
        car_acc = car.acceleration
        car_de_acc = car.de_acceleration
        car_speed = car.speed
        log = logging.getLogger("traffic-logger")
        log.info('Time : ' + str(current_time)
                 + '  Car ID: ' + str(car_id)
                 + '  Speed limit: ' + str(car_speed_limit)
                 + '  Car x: ' + str(car_x)
                 + '  Car y: ' + str(car_y)
                 + '  Speed: ' + str(car_speed)
                 + '  Acceleration: ' + str(car_acc)
                 + '  De-acceleration: ' + str(car_de_acc)
                 + '  Car road: ' + str(car_road)
                 + '  Car lane: ' + str(car_lane)
                 + '  Car decision: ' + car.decision
                 + '  Car Extra:  ' + str(car.extra))

    @staticmethod
    def log_end():
        logging.basicConfig(filename='traffic.log', filemode='w', level=logging.DEBUG)
        logging.getLogger().addHandler(logging.StreamHandler())
        log = logging.getLogger("traffic-logger")
        log.info("-------------------------------------------------------------")

    """
         A function to log all information about the Map to traffic.log and also to the console
                """
    @staticmethod
    def log_map(map1):
        logging.basicConfig(filename='traffic.log', level=logging.DEBUG)
        logging.getLogger().addHandler(logging.StreamHandler())
        x = datetime.datetime.now()
        map_id = map1.id
        map_name = map1.name
        log = logging.getLogger("traffic-logger")
        log.info("Time : "+str(x) + "map_id: "+str(map_id) + "map_id : "+map_name)

    @staticmethod
    def get_logger(map1):
        logging.basicConfig(filename='traffic.log', level=logging.DEBUG)
        logger = logging.getLogger().addHandler(logging.StreamHandler())
        return logger