import json


class ConfigReader:
    __data = ""

    def __init__(self, filename="base-configuration.json"):
        """
        Virtually private constructor
        :param filename: json (base-config) containing basic config of simulation and all other json file names 
        """
        if ConfigReader.__data == "":
            ConfigReader.__data = self.create_data(filename)
        else:
            raise Exception("Object already exists")

    @staticmethod
    def get_data(filename="base-configuration.json"):
        if ConfigReader.__data == "":
            ConfigReader(filename)
        return ConfigReader.__data

    def create_data(self, filename):
        """
        Iterates over file names in base-config and concatenates all data into one data structure
        :param filename: json (base-config) containing basic config of simulation and all other json file names
        :return: concatenated data structure of all json files
        """

        with open("../data/configs/app_config/"+filename) as f:
            data = json.load(f)

        for i in range(len(data["files"])):

            with open("../data/" + list(data["files"].keys())[i] + "/" + list(data["files"].values())[i]) as f:
                data["files"][list(data["files"].keys())[i]] = json.load(f)

        return data
