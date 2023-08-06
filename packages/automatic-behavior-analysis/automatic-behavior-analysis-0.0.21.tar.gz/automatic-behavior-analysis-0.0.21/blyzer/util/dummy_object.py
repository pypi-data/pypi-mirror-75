import json
import copy

class UniversalDummy:
    def __init__(self):
        def func(*args): pass
        self.func = func

    def __getattr__(self, attr):
        return self.func

class DummyModel:
    def __init__(self, response_filename):
        with open(response_filename, 'r', encoding='utf-8') as file:
            self.response = json.load(file)

    def process_decoded_image(self, frame):
        return copy.deepcopy(self.response)

class EmptyModel:
    def process_decoded_image(self, frame):
        return {}