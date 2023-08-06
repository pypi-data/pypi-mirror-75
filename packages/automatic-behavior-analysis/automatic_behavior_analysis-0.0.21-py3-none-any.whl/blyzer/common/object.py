import numpy as np
import cv2
import pandas as pd

from blyzer.common.trajectory import Trajectory
from blyzer.common.settings import BlyzerSettings
import blyzer.visualization.frame_decorators as fd

class ObservableObject:
    def __init__(self,
                 object_type: str,
                 frame_shape,
                 max_hole_size = 75,
                 name: str=None):
        self._frame_width = frame_shape[1]
        self._frame_height = frame_shape[0]
        self._object_type = object_type
        self._name = name
        self._max_hole_size = max_hole_size
        self._trajectory = Trajectory(max_hole_size)
        self._heatmap = np.zeros(frame_shape[:2])
        self._annotations = []
        self._keypoints = {}

    def get_last_position(self):
        return None

    def add_annotation(self, frame_index, observable_object):
        x = (observable_object['coordinates']['x1'] +
                observable_object['coordinates']['x2'])*self._frame_width / 2
        y = (observable_object['coordinates']['y1'] +
                observable_object['coordinates']['y2'])*self._frame_height / 2

        while frame_index >= len(self._annotations):
            self._annotations.append(None)
        self._annotations[int(frame_index)] = observable_object

        self._trajectory.add_point(frame_index, (x, y))
        self._heatmap[int(y)][int(x)] += 1

        xmin = int(self._frame_width * observable_object['coordinates']['x1'])
        ymin = int(self._frame_height * observable_object['coordinates']['y1'])
        xmax = int(self._frame_width * observable_object['coordinates']['x2'])
        ymax = int(self._frame_height * observable_object['coordinates']['y2'])

        keypoints_conf_threshold = BlyzerSettings().getParam("keypoints_confidence_threshold", 0.5)
        for name, kp in observable_object['keypoints'].items():
            if kp and kp['rate']>keypoints_conf_threshold:
                x = int(xmin + (xmax - xmin) * kp['x'])
                y = int(ymin + (ymax - ymin) * kp['y'])
                self._add_keypoint_item(frame_index, name, x, y)

    def get_type(self):
        return self._object_type

    def get_name(self):
        return self._name

    def set_name(self, name: str):
        self._name = name

    def get_trajectory_points(self):
        return self._trajectory.get_trajectory_points()

    def get_trajectory_np(self):
        return self._trajectory.get_trajectory_np()

    def len(self):
        return self._trajectory.len()
    
    def decorate_frame_with_keypoints(self, frame, index):
        color_unknown = BlyzerSettings().getParam("color_unknown")
        for name, kp_tr in self._keypoints.items():
            x, y = kp_tr.get_point(index)
            if not np.isnan(x):
                frame = fd.draw_keypoint(frame, x, y, 1.0, color_unknown, name)
        return frame

    def decorate_frame_with_bb(self, frame, index):
        color_unknown = BlyzerSettings().getParam("color_unknown")
        show_name = BlyzerSettings().getParam("show_name", False)
        show_rate = BlyzerSettings().getParam("show_rate", True)
        show_type = BlyzerSettings().getParam("show_type", True)
        text_format = fd.calc_text_format(show_name, show_rate, show_type)

        item = self._annotations[index]
        if item:
            frame = fd.draw_boundingbox(image=frame, 
                                        xmin=int(self._frame_width * item['coordinates']['x1']), 
                                        ymin=int(self._frame_height * item['coordinates']['y1']), 
                                        xmax=int(self._frame_width * item['coordinates']['x2']), 
                                        ymax=int(self._frame_height * item['coordinates']['y2']), 
                                        text_format=text_format, 
                                        color=color_unknown,
                                        category=item['category'],
                                        rate=item['rate'], 
                                        name="")
        return frame

    def decorate_frame_with_heatmap(self, frame, n_row=18, n_collumn=32, transparency=0.5):
        heatmap = self.get_heatmap(n_row, n_collumn, True)
        y_step = int(frame.shape[0] / n_row)
        x_step = int(frame.shape[1] / n_collumn)
        output = frame.copy()
        for x in range(n_collumn):
           for y in range(n_row):
               x1 = x*x_step
               x2 = (x+1)*x_step
               y1 = y*y_step
               y2 = (y+1)*y_step
               r = heatmap[y][x]
               overlay = frame.copy()
               cv2.rectangle(overlay, (x1, y1), (x2, y2), (255, 0, 0), -1)
               transp = transparency * (r)
               cv2.addWeighted(overlay, transp, output,
                               1 - transp, 0, output)
        frame = output
        return frame

    def to_dataframe(self):
        df = pd.DataFrame()
        bb_trajectory = self._trajectory.get_trajectory_np()
        df['x'] = bb_trajectory[:,0]
        df['y'] = bb_trajectory[:,1]
        for name, kp_tr in self._keypoints.items():
            print(name)
            kp_trajectory = kp_tr.get_trajectory_np()
            dif = len(df.index) - kp_trajectory.shape[0]
            kp_trajectory = np.pad(kp_trajectory, ((0,dif),(0,0)), mode='constant', constant_values=np.NaN)
            print(kp_trajectory.shape)
            df[name, 'x'] = kp_trajectory[:,0]
            df[name, 'y'] = kp_trajectory[:,1]
        return df

    def get_heatmap(self, n_row=18, n_collumn=32, is_norm=True):
       heatmap = np.zeros((n_row, n_collumn), dtype=np.int64)
       y_step = int(self._frame_height / n_row)
       x_step = int(self._frame_width / n_collumn)
       for x in range(n_collumn):
           for y in range(n_row):
               x1 = x*x_step
               x2 = (x+1)*x_step
               y1 = y*y_step
               y2 = (y+1)*y_step
               hm_crop = self._heatmap[y1:y2, x1:x2]
               s = np.sum(hm_crop)
               heatmap[y][x] = s

       if is_norm:
           hm_max = np.amax(heatmap)
           heatmap = heatmap / hm_max
       return heatmap

    def _add_keypoint_item(self, frame_index:int, keypoint_name:str, x:int, y:int):
        if keypoint_name not in self._keypoints:
            self._keypoints[keypoint_name] = Trajectory(self._max_hole_size)
        self._keypoints[keypoint_name].add_point(frame_index, (x, y))
