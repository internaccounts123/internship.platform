import json
from jsonpath_rw import jsonpath, parse


class ConfigReader:
    __data = ""
    __instance = ""

    def __init__(self, filename="base-configuration.json"):
        """
        Virtually private constructor
        :param filename: json (base-config) containing basic config of simulation and all other json file names 
        """
        if ConfigReader.__instance == "":
            ConfigReader.__data = ConfigReader.__create_data(filename)
        else:
            raise Exception("Object already exists")

    @staticmethod
    def get_instance(filename="base-configuration.json"):
        if ConfigReader.__instance == "":
            __instance = ConfigReader(filename)
        return __instance

    @staticmethod
    def get_data(query):
        """
        :param query: string containing query for the value it needs from the dictionary
        :return: matches found for the query
        """
        path = parse('$..' + query)
        matches = [match.value for match in path.find(ConfigReader.__data)]
        return matches

    @staticmethod
    def __create_data(filename):
        """
        Iterates over file names in base-config and concatenates all data into one data structure
        :param filename: json (base-config) containing basic config of simulation and all other json file names
        :return: concatenated data structure of all json files
        """

        with open("../data/configs/app_config/"+filename) as f:
            data = json.load(f)

        for i in range(len(data["driving"])):

            with open("../data/driving/" + list(data["driving"].values())[i]) as f:
                data["driving"][list(data["driving"].keys())[i]] = json.load(f)

        return data
