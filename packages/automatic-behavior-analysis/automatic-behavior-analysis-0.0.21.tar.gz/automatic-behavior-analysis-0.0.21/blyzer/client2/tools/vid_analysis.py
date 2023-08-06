"""
@author: Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>
"""
import glob
import matplotlib.pyplot as plt
import numpy as np
import cv2

from blyzer.common.settings import BlyzerSettings
from blyzer.common.object import ObservableObject
import blyzer.client2.tools.Vienna_lines_screens as vls
import blyzer.analitics.trajectory.calc_features as blyzer_tr_f
import blyzer.visualization.frame_decorators as fd


def calculate_tail_angle(key_points):
    return None

class Analysis():
    """
    Warning!!! Class can work only with one object
    """

    def __init__(self, sample_frame, fps):
        self._tail_angles = {}

        self._total_distance = 0
        self._fps = fps

        self._frame_shape = sample_frame.shape
        self._frame_width = sample_frame.shape[1]
        self._frame_height = sample_frame.shape[0]

        if str(BlyzerSettings().getParam('project', "None")).lower() == 'Vienna'.lower():
            environment_settings = vls.get_data(sample_frame)
            self._center_x = environment_settings[0]
            self._center_y = environment_settings[1]
            self._TL_left = environment_settings[2]
            self._BR_left = environment_settings[3]
            self._TL_right = environment_settings[4]
            self._BR_right = environment_settings[5]

        self._object_of_interests = []
        self._dog = ObservableObject('dog', self._frame_shape, max_hole_size=self._fps)
        self._frame_annotations = []

    def add_object_of_interests(self, objects):
        self._object_of_interests.append(objects)

    def get_trajectory_points(self):
        return self._dog.get_trajectory_points()

    def get_trajectory_np(self, filter_fcn=None):
        trajectory_np = self._dog.get_trajectory_np()
        if filter_fcn is not None:
            trajectory_np = trajectory_np[~np.isnan(trajectory_np).any(axis=1)]
            trajectory_x_np = filter_fcn(trajectory_np[:, 0])
            trajectory_y_np = filter_fcn(trajectory_np[:, 1])
            trajectory_np = np.stack((trajectory_x_np, trajectory_y_np), axis=-1)
        return trajectory_np

    def get_average_distances(self):
        """
            What is the avarage distance between the object we are detecting, and an object of interst
        """
        average_distance = np.zeros(len(self._object_of_interests))
        objects_position = np.array(self._object_of_interests)

        for position in self._dog.get_trajectory_points():
            distance = np.add(objects_position, -1 * np.array(position))
            distance = np.linalg.norm(distance, 1)
            average_distance += distance
        average_distance /= self._dog.len()
        return average_distance

    def len(self):
        return self._dog.len()

    def add_frame_annotation(self, annotation):
        frame_index = annotation["frame_index"]

        while frame_index >= len(self._frame_annotations):
            self._frame_annotations.append(None)
        self._frame_annotations[int(frame_index)] = annotation

        for observable_object in annotation["objects"]:
            if observable_object['category'] == 'dog':
                self._dog.add_annotation(frame_index, observable_object)
                break

    def decorate_frame_with_bb(self, frame:np.array, index:int):
        frame = self._dog.decorate_frame_with_bb(frame, index)
        return frame

    def decorate_frame_with_keypoints(self, frame:np.array, index:int):
        frame = self._dog.decorate_frame_with_keypoints(frame, index)
        return frame

    def decorate_frame_with_heatmap(self, frame, n_row=18, n_collumn=32, transparency=0.5):
        return self._dog.decorate_frame_with_heatmap(frame, n_row, n_collumn, transparency)

    def decorate_frame_with_trajectory(self, frame, index=-1, duration=None, thickness=3, color=(0, 0, 255)):

        if str(duration).lower() == 'All'.lower():
            duration = self._dog.len()
            pts = self.get_trajectory_np(self.moving_average_filter)
        else:
            if duration is None:
                duration = self._fps * 3
            elif duration > index:
                duration = index
            pts = self._dog.get_trajectory_points()[index-int(duration):index]
            pts = np.array(pts)

        try:
            pts = pts[~np.isnan(pts).any(axis=1)]
            #pts = np.reshape(pts, (pts.shape[0]//2, 2))
            cv2.polylines(frame, np.int32([pts]), False, color, thickness)
        except np.AxisError as e:
            pass
        return frame

    def to_dataframe(self):
        return self._dog.to_dataframe()

    def get_total_distance(self):
        traj_np = self.get_trajectory_np(self.moving_average_filter)
        deltas_np = np.diff(traj_np, axis=0)
        deltas_np = deltas_np[~np.isnan(deltas_np).any(axis=1)]
        total_distance = np.sum(np.linalg.norm(deltas_np, axis=1))
        return total_distance

    def get_total_duration(self):
        traj_np = self.get_trajectory_np()
        return traj_np.shape[0] / self._fps

    def get_useful_duration(self):
        traj_np = self.get_trajectory_np(self.moving_average_filter)
        usefull_traj = traj_np[~np.isnan(traj_np).any(axis=1)]
        return usefull_traj.shape[0] / self._fps

    def get_average_speed(self):
        return self.get_total_distance() / self._dog.len() * self._fps

    def get_specific_trajectory_stat(self):
        return blyzer_tr_f.trajectory_features(self.get_trajectory_np(self.moving_average_filter), self.get_total_distance())

    def get_statistics(self):
        """
        Collect ant return dictinary with basic statistics
        """
        stats = {}
        stats['Total distance'] = self.get_total_distance()
        stats['Average speed'] = self.get_average_speed()
        stats['Total duration'] = self.get_total_duration()
        stats['Useful duration'] = self.get_useful_duration()
        stats['Useful ratio'] = stats['Useful duration'] / stats['Total duration']
        ext_stat = self.get_specific_trajectory_stat()
        for name, val in zip (blyzer_tr_f.FEATURES_NAMES, ext_stat):
            stats[name] = val
        return stats

    def moving_average_filter(self, data):
        w = 3
        return np.convolve(data, np.ones(w), 'valid') / w

    def get_quartiles_times(self):
        top_left_samples = np.sum(
            self._heatmap[0:self._center_x, 0:self._center_y])
        top_right_samples = np.sum(
            self._heatmap[self._center_x:self._frame_width, 0:self._center_y])
        bottom_left_samples = np.sum(
            self._heatmap[0:self._center_x, self._center_y:self._frame_height])
        bottom_right_samples = np.sum(
            self._heatmap[self._center_x:self._frame_width, self._center_y:self._frame_height])
        quartiles_time = [top_left_samples, top_right_samples,
                          bottom_left_samples, bottom_right_samples]
        quartiles_time /= self._fps
        return quartiles_time
