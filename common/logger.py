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
    data = ""


    def __init__(self):
        file_name = self.__config_filename

        maps_path = os.path.join(ConfigReader.get_data('base_path'), 'data/configs/app_config/{}'.format(file_name))
        with open(maps_path, 'r') as f:
            __data = json.load(f)

        data = copy.deepcopy(__data)

        __log_filename = data["log_filename"]
        __config_type = data["config_type"]
    @staticmethod

    def get_logger():

        if Logger.__config_type == "DEBUG":
            logging.basicConfig(filename=Logger.__log_filename, level=logging.DEBUG)
        if Logger.__config_type == "WARNING":
            logging.basicConfig(filename=Logger.__log_filename, level=logging.WARNING)
        if Logger.__config_type == "ERROR":
            logging.basicConfig(filename=Logger.__log_filename, level=logging.ERROR)
        else:
            logging.basicConfig(filename=Logger.__log_filename, level=logging.INFO)

        logging.getLogger().addHandler(logging.StreamHandler())
        return logging.getLogger("traffic-logger")



