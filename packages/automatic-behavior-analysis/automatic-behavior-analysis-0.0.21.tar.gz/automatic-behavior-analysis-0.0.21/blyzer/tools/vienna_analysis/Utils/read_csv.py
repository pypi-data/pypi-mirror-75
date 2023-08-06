"""
A tool to read  csv files with vienna analysis
"""


import csv


class csv_helper:
    def __init__(self, path):
        self.path = path

    def header_generator(self):
        """Generates head data"""
        with open(self.path, "r") as file:
            csv_reader = csv.reader(file, delimiter=',')
            for index,row in enumerate(csv_reader):
                if index > 2:
                    yield [float(row[1]),float(row[2]),float(row[3])]

    def nose_generator(self):
        """Generates nose data"""
        with open(self.path, "r") as file:
            csv_reader = csv.reader(file, delimiter=',')
            for index,row in enumerate(csv_reader):
                if index > 2:
                    yield [float(row[4]),float(row[5]),float(row[6])]




