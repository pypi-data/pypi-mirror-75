import os
from abc import abstractmethod

import cv2
import numpy as np

import common.annotation
from util.video_tools import VideoSaver
from blyzer.common.settings import BlyzerSettings

class Video():
    def __init__(self, video_path: str, name: str = None, video_type: str = 'file', **kwargs):
        """ Class for video
        sourse file will be always open
        source types and specific arguments:
            * file -- video from file
        """
        if not os.path.exists(video_path):
            raise ValueError('Path is not existed')

        self._path = video_path
        if name is not None:
            self._name = name
        else:
            vid_name, _ = os.path.splitext(os.path.basename(video_path))
            self._name = vid_name

        self._vidcap = None
        self._get_raw_frame = None
        self._get_frames_count = None

        if video_type.lower() == 'file':
            print("Created video from file")
            self._video_type = 'file'
            self._get_raw_frame = self._file_get_raw_frame
            self._get_frames_count = self._file_get_frames_count
            self._vidcap = cv2.VideoCapture(self._path)
            if not self._vidcap.isOpened():
                raise RuntimeError("Invalid file format")
            self._vid_src_current_frame = 0
        else:
            raise ValueError('Unsupported source type')

        _, self.preview = self._vidcap.read()
        self._vidcap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def get_fps(self):
        return int(self._vidcap.get(cv2.CAP_PROP_FPS))

    def get_video_size(self):
        """Return size of video: (width, height)
        """
        return (int(self._vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self._vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    def get_path(self):
        return self._path

    def _file_get_raw_frame(self, frame: int) -> np.array:
        frame_r = frame
        success = False
        incr = 1
        while not success:
            if frame_r >= self.get_frames_count(): # If the end of file is achieved, move back
                frame_r = frame - 1
                incr = -1
            if frame_r != self._vid_src_current_frame:
                self._vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_r)
            success, image_np = self._vidcap.read()
            frame_r += incr

        self._vid_src_current_frame = frame + 1
        return cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

    def get_raw_frame(self, frame: int) -> np.array:
        """Return a raw frame from source by frame index
            indexing from 0

         return: numpy.array
         """
        if frame >= self.get_frames_count():
            return None
        return self._get_raw_frame(frame)

    @abstractmethod
    def _decorate_frame(self, frame: int) -> np.array:
        return self.get_raw_frame(frame)

    def get_frame(self, frame: int) -> np.array:
        """Return a decorated frame from source by frame index.

        return: numpy.array
        """
        return self._decorate_frame(frame)

    def _file_get_frames_count(self) -> int:
        try:
            return self._frames_count
        except Exception:
            self._frames_count = int(self._vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
            return self._frames_count

    def get_frames_count(self) -> int:
        return self._get_frames_count()


class AnnotatedVideo(Video):
    def __init__(self, video_path: str,
                 annotation_path: str = None,
                 name: str = None,
                 annotation_type: str = 'json',
                 video_type: str = 'file'):
        super().__init__(video_path, name=name, video_type=video_type)
        if annotation_type.lower() == 'json':
            if annotation_path is None:
                _annotation_path = os.path.splitext(video_path)[0] + '.json'
            else:
                _annotation_path = annotation_path
            w, h = self.get_video_size()
            self._annotation = common.annotation.JsonAnnotation(_annotation_path,
                                                                os.path.basename(video_path),
                                                                w,
                                                                h,
                                                                self.get_fps())
        else:
            raise ValueError('Undefined type of annotation')

        self._custom_frame_decorators = []

    def save_annotated_video(self, white_bg = False, save_path = None):
        if save_path is None:
            output_dir = os.path.dirname(self._path)
            path = os.path.join(output_dir, "{}-output.{}".format(self._name, BlyzerSettings().getParam("video_extension")))
            video_saver = VideoSaver.create(path, self._vidcap)
        else:
            video_saver = VideoSaver.create(save_path, self._vidcap)
        for n in range(self.get_frames_count()):
            frame = self.get_frame(n)
            if frame is not None:
                if not white_bg:
                    video_saver.add_frame(frame)
                else:
                    w_fr = np.full_like(frame, 255)
                    annotation = self.get_frame_annotation(n)
                    if annotation is not None:
                        for fd in self._custom_frame_decorators:
                            frame_np = fd(frame_np, n)
                        frame_np = cv2.cvtColor(frame_np, cv2.COLOR_RGB2BGR)
                        video_saver.add_frame(frame_np)
        video_saver.close()

    def get_existed_task(self):
        return self._annotation.get_existed_task()

    def set_existed_task(self, task_id):
        self._annotation.set_existed_task(task_id)

    def get_frame_annotation(self, frame: int):
        return self._annotation.get_frame_annotation(frame)

    def add_frame_annotation(self, frame: int, annotation):
        self._annotation.add_frame_annotation(frame, annotation)

    def update_frame_annotation(self, all_annotation):
        new_keys = set(all_annotation.keys()).difference(set(self._annotation.get_full_annotation().keys()))
        for frame_id in new_keys:
            self._annotation.add_frame_annotation(frame_id, all_annotation[frame_id], False)
        self._annotation.force_save()

    def get_full_annotation(self):
        return self._annotation.get_full_annotation()

    def get_progress(self):
        return len(self.get_full_annotation()) / self.get_frames_count()

    def get_frame_with_annotation(self, frame: int):
        """ Return annotated frame with annotation
        """
        if not self._annotation.has_annotation(frame):
            return None, None
        return self.get_frame(frame), self.get_frame_annotation(frame)

    def add_custom_frame_decorator(self, frame_decorator):
        self._custom_frame_decorators.append(frame_decorator)

    def is_annotated(self, frame:int) -> bool:
        return self._annotation.get_frame_annotation(frame) is not None

    @abstractmethod
    def _decorate_frame(self, frame: int) -> np.array:
        if not self._annotation.has_annotation(frame):
            return None
        frame_np = self.get_raw_frame(frame)
        if frame_np is None:
            return None
        annotation = self.get_frame_annotation(frame)
        for fd in self._custom_frame_decorators:
            frame_np = fd(frame_np, frame)
        return frame_np
