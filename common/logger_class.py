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
    def log_cars(cars):
        logging.basicConfig(filename='traffic.log', level=logging.DEBUG)

        x = datetime.datetime.now()
        logging.getLogger().addHandler(logging.StreamHandler())
        for car in cars:
            car_id = car.id
            car_speed_limit = car.speed_limit
            car_x = car.x
            car_y = car.y

            car_road = car.road_id
            car_lane = car.lane_id
            log = logging.getLogger("traffic-logger")
            log.info('Time : '+str(x) + 'car_speed limit : ' + str(car_speed_limit) + 'car_id : ' + str(car_id)
                     + 'car_x: '
                     + str(car_x) + 'car_y : ' + str(car_y)
                     + 'car road: ' + str(
                    car_road) + 'car lane : ' + str(car_lane))

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
