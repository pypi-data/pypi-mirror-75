"""
Represents a single coordinate
"""


class Point:
    def __init__(self, x_coordinate, y_coordinate,percentage):
        self._percentage = percentage
        self._x = x_coordinate
        self._y = y_coordinate

    def __str__(self):
        return "x {} y {} % {}".format(self._x, self._y,self._percentage)
