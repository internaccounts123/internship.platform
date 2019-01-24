import logging
from common.config_reader import ConfigReader
from time import gmtime, strftime
import datetime
import copy
import json
import os

class Logger:
    __config_filename = "log_config.json"
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
    def get_log_file_name():
        return Logger.__log_filename

    @staticmethod
    def get_logger(log_type):
        if log_type == "FILE":
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)

            formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

            file_handler = logging.FileHandler('traffic.log', mode='w')
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            return logger

        if log_type == "CONSOLE":
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)

            formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)

            logger.addHandler(stream_handler)
            return logger

        if log_type == "BOTH":
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)

            formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            file_handler = logging.FileHandler('traffic.log', mode='w')
            file_handler.setFormatter(formatter)

            logger.addHandler(stream_handler)
            logger.addHandler(file_handler)


            return logger

