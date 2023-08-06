import os
import cv2
from blyzer.common.settings import BlyzerSettings
import blyzer.visualization.frame_decorators as fd

class VideoSaver:
    """ A class that writes video to a file """
    def __init__(self, path, fps, width, height):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # TODO: put video output format into the config file
        print("VideoSaver.__init__: fourcc: {}, fps: {}, width: {}, height: {}".format(fourcc, fps, width, height))
        self.writer = cv2.VideoWriter(path, fourcc, fps, (width, height))

    @staticmethod
    def create(path, vidcap):
        """
        Creates a class of VideosSaver and adds parameters to it

        Args:
            output_dir: folder which the written video will be saved
            base_filename: filename
            vidcap: video capture object

        Returns:

        """
        # print("Output video path:", path)
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))
        width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return VideoSaver(path, fps, width, height)

    def add_frame(self, image):
        """Add Frame to output video

        Parameters
        ----------
        image : numpy.array
            BGR image
        """
        self.writer.write(image)

    def close(self):
        self.writer.release()

