import math
from Point import *


class Line:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.slope = None
        self.intercept = None
        self.calc_slope()
        self.calc_intercept()

    def calc_slope(self):
        self.slope = (self.p2.y-self.p1.y)/(self.p2.x-self.p1.x)

    def calc_intercept(self):
        self.intercept = -(self.slope * self.p1.x) + self.p1.y

    def calc_x(self, y):
        return (y-self.intercept)/self.slope

    def calc_y(self, x):
        return x * self.slope + self.intercept

    def get_p1(self):
        return self.p1

    def get_p2(self):
        return self.p2

    def get_slope(self):
        return self.slope

    def rotate_line(self, Theta):
        p3 = Point(self.p2.x, self.p2.y)
        p3.setX(math.cos(Theta) * (self.p2.x - self.p1.x) - math.sin(Theta) * (self.p2.y - self.p1.y) + self.p1.x)
        p3.setY(math.sin(Theta) * (self.p2.x - self.p1.x) + math.cos(Theta) * (self.p2.y - self.p1.y) + self.p1.y)
        new_line = Line(Point(self.p1.x, self.p1.y), p3)
        return new_line

    def extend_line(self, width, height):
        p3 = Point(0, 0)
        if 0.05 >= self.slope >= -0.05:
            if self.p2.getX()>self.p1.getX():
                p3 = Point(width, int(self.intercept))
            else:
                p3 = Point(0, int(self.intercept))
        elif 15<= self.slope or self.slope<= -15:
            if self.p2.getY()>self.p1.getY():
                p3 = Point(self.p1.getX(), height)
            else:
                p3 = Point(self.p1.getX(), 0)

        elif self.p2.getX() > self.p1.getX() and self.p2.getY() > self.p1.getY():
            if self.slope * width + self.intercept <= height:
                p3 = Point(width, int(self.slope*width + self.intercept))
            else:
                p3 = Point(int((height-self.intercept)/self.slope), height)

        elif self.p2.getX() < self.p1.getX() and self.p2.getY() < self.p1.getY():
            if self.intercept >= 0:
                p3 = Point(0, int(self.intercept))
            else:
                p3 = Point(int(-self.intercept/self.slope), 0)

        elif self.p2.getX() > self.p1.getX() and self.p2.getY() < self.p1.getY():
            if (-self.intercept/self.slope) <= width:
                p3 = Point(int(-self.intercept/self.slope), 0)

            else:
                p3 = Point(width, int(self.slope*width + self.intercept))
        else:
            if self.intercept <= height:
                p3 = Point(0, int(self.intercept))
            else:
                p3 = Point(int((height-self.intercept)/self.slope), int(height))
        self.p2 = p3

    def print_line(self):
        print("y =", self.slope, "x +", self.intercept)
        print("points:", self.p1.to_str(), self.p2.to_str())