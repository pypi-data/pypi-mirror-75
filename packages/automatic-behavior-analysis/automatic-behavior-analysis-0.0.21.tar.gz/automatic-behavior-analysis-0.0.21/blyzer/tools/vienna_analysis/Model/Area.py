"""
A class that represents an area in the video
"""


class Area:
    def __init__(self, top_left, top_right, bottom_left, bottom_right):
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right

    def __str__(self):
        return "top left {} \n" \
               "top right {} \n" \
               "bottom left {} " \
               "\nbottom right {}".format(self.top_left, self.top_right, self.bottom_left, self.bottom_right)


