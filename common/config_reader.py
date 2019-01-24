import json, os
from jsonpath_rw import jsonpath, parse


class ConfigReader:
    __data = ""
    __instance = ""
    __base_path = ""

    def __init__(self, filename = "base-configuration.json"):
        """
        Virtually private constructor
        :param filename: json (base-config) containing basic config of simulation and all other json file names 
        """
        if ConfigReader.__instance == "":

            ConfigReader.__base_path = os.path.realpath(os.path.join(os.getcwd(), '../'))
            ConfigReader.__data = ConfigReader.__create_data(filename)

        else:
            raise Exception("Object already exists")

    @staticmethod
    def get_instance(filename = "base-configuration.json"):

        if ConfigReader.__instance == "":
            __instance = ConfigReader(filename)
        return __instance

    @staticmethod
    def get_data(query):
        """
        :param query: string containing query for the value it neeqsds from the dictionary
        :return: matches found for the query
        """
        if query == 'base_path':
            return ConfigReader.__base_path
        path = parse(query)
        matches = [match.value for match in path.find(ConfigReader.__data)]
        return matches

    @staticmethod
    def __create_data(filename):
        """
        Iterates over file names in base-config and concatenates all data into one data structure
        :param filename: json (base-config) containing basic config of simulation and all other json file names
        :return: concatenated data structure of all json files
        """

        with open(os.path.join(ConfigReader.get_data('base_path'), 'data/configs/app_config/{}'.format(filename))) as f:
            data = json.load(f)

        for i in range(len(data["driving"])):
            with open(os.path.join(ConfigReader.get_data('base_path'), 'data/driving/{}'.format(list(data["driving"].values())[i])) ) as f:
                data["driving"][list(data["driving"].keys())[i]] = json.load(f)

        return data

