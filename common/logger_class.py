import logging
from common.config_reader import ConfigReader
from time import gmtime, strftime
import datetime
import copy
import json
import os

class Logger:
    __config_filename = "logger_config.json"
    __log_filename = ""
    __config_type = ""


    def __init__(self):
        file_name = self.__config_filename

        maps_path = os.path.join(ConfigReader.get_data('base_path'), 'data/map/{}'.format(file_name))
        with open(maps_path, 'r') as f:
            __data = json.load(f)

        data = copy.deepcopy(__data)

        __log_filename = data["log_filename"]
        __config_type = data["config_type"]

    """
     A function to return logger 
            """

    @staticmethod
    def get_logger():
        file_name = "logger_config.json"
        maps_path = os.path.join(ConfigReader.get_data('base_path'), 'data/configs/app_config/{}'.format(file_name))
        with open(maps_path, 'r') as f:
            __data = json.load(f)

        data = copy.deepcopy(__data)

        if data["config_type"] == "DEBUG":
            logging.basicConfig(filename=data["log_filename"], level=logging.DEBUG)
        else:
            logging.basicConfig(filename=data["log_filename"], level=logging.INFO)

        logging.getLogger().addHandler(logging.StreamHandler())
        return logging.getLogger("traffic-logger")



