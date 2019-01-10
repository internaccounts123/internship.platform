import json


class ConfigReader:
    def __init__(self):
        pass

    @staticmethod
    def create_data(filename):
        """
        Iterates over file names in base-config and concatenates all data into one data structure
        :param filename: name of file containing simulation data (base-config)
        :return: concatenated data structure of all json files


        """

        with open("../data/configs/app_config/"+filename) as f:
            data = json.load(f)

        for i in range(len(data["files"])):

            with open("../data/" + list(data["files"].keys())[i] + "/" + list(data["files"].values())[i]) as f:
                data["files"][list(data["files"].keys())[i]] = json.load(f)

        return data
