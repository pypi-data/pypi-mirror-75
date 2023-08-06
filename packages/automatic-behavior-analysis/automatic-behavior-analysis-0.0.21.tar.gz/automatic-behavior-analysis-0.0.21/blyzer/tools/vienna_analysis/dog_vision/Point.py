class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return int(self.x)

    def getY(self):
        return int(self.y)

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def to_str(self):

        return "(" + str(self.x) + ", " + str(self.y) + ")"
