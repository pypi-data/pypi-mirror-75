import datetime
import pandas as pd
import numpy as np
import os
import copy
from blyzer.client2.tools.vid_analysis import Analysis
from blyzer.common.settings import BlyzerSettings


def frame2time(start_time, frame_number, fps):
    """
    returns the time of the frame
    Args:
        start_time: start time of the video
        frame_number: number of frame
        fps: video fps

    Returns:timestamp

    """
    p_ms = int(1000 / fps) * frame_number
    return start_time + pd.Timedelta(np.timedelta64(p_ms, 'ms'))


def filename2time(filename):
    """
    03_20171108201654.mp4
    """
    filename = os.path.basename(filename)
    filename = os.path.basename(filename).split('.')[0][3:]
    time = None
    try:
        time = pd.Timestamp(filename)
    except Exception:
        time = "20000101000000"
    return time

class StatisticHolder:
    """
    The class responsible for storing and processing video annotations
    """

    def __init__(self, file_name, fps, video_preview, total_frames):
        """
        File name in date-time format
        Args:
            file_name: video filename
            fps: video fps
        """
        self.file_name = file_name
        self.fps = fps
        self._total_frames = total_frames
        self.video_time = filename2time(file_name)
        self._analysis = Analysis(video_preview, self.fps)

    def add_frame_annotation(self, annotation):
        """
        adds annotation to the annotation_buffer
        """
        annotation = copy.deepcopy(annotation)
        self._analysis.add_frame_annotation(annotation)

    def custom_frame_decorator(self, image, frame_num):
        image = self._analysis.decorate_frame_with_bb(image, frame_num)
        image = self._analysis.decorate_frame_with_keypoints(image, frame_num)
        if BlyzerSettings().getParam("show_trajectory", True):
            self._analysis.decorate_frame_with_trajectory(image, frame_num)
        return image

    def create_heatmap(self, frame):
        return self._analysis.decorate_frame_with_heatmap(frame)

    def create_full_trajectory(self, frame):
        return self._analysis.decorate_frame_with_trajectory(frame, duration='All')

    def get_statistics(self):
        return self._analysis.get_statistics()

    def get_trajectory(self):
        return self._analysis.get_trajectory_points()

    def get_summary_statistics(self):
        summary = {}
        summary['Video duration'] = '{:.2f} s'.format(
            self._total_frames / self.fps)
        summary['Total distance'] = '{:.2f} px'.format(
            self._analysis.get_total_distance())
        summary['Average speed'] = '{:.2f} px/s'.format(
            self._analysis.get_average_speed())
        summary['Num of processed frames'] = '{}'.format(
            self._analysis.len())
        summary['Progress'] = '{:.2%}'.format(
            self._analysis.len() / self._total_frames)
        return summary

    def save_summary_statistics(self):
        summary = self.get_summary_statistics()
        p = os.path.dirname(self.file_name)
        filename = os.path.basename(self.file_name).split('.')[0]
        fp = os.path.join(p, filename + ".csv")
        data = []
        for key, value in summary.items():
            data.append({'Parameter':key, 'Value':value,})
        data = pd.DataFrame(data)
        data = data.set_index('Parameter')
        data.to_csv(fp)

    def to_dataframe(self):
        return self._analysis.to_dataframe()
