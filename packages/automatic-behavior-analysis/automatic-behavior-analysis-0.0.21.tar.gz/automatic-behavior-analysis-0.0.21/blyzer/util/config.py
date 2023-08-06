import json
from util.object_dict import ObjectDict


class Config(ObjectDict):
    def __init__(self, filename):
        self.load(filename)

    def load(self, filename):
        with open(filename, 'r') as f:
            json_data = json.load(f)
            for key in json_data:
                self[key] = json_data.get(key)
