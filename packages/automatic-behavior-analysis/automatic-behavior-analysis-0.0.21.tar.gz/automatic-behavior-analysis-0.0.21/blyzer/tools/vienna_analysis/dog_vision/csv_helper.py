import csv


class csv_helper:
    def __init__(self, path):
        self.path = path

    def csv_generator(self):
        with open(self.path, "r") as file:
            for row in file:
                yield row