from abc import abstractmethod
import os
from blyzer.common.saver import load_annotation, save_annotation
import time


class Annotation():
    def __init__(self):
        pass

    @abstractmethod
    def add_frame_annotation(self, frame:int, annotation):
        raise NotImplementedError

    @abstractmethod
    def get_frame_annotation(self, frame:int):
        raise NotImplementedError

    @abstractmethod
    def get_full_annotation(self):
        return None

class JsonAnnotation(Annotation):
    def __init__(self, annotation_path:str, video_name:str, width = None, height = None, fps = None):
        super().__init__()
        self._annotation_path = annotation_path
        self._width = width
        self._height = height
        self._fps = fps
        self._video_name = video_name

        self._annotation, self._existed_task = self._load_annotation()


    def _load_annotation(self):
        if os.path.isfile(self._annotation_path):
            annotation_raw = load_annotation(self._annotation_path)
            annotation = {}

            if "width" in annotation_raw:
                self._width = annotation_raw["width"]
            if "height" in annotation_raw:
                self._height = annotation_raw["height"]
            if "fps" in annotation_raw:
                self._fps = annotation_raw["fps"]
            if "video_name" in annotation_raw:
                self._video_name = annotation_raw["video_name"]

            frame_annotation_raw = annotation_raw["frame_annotations"]
            for key, value in frame_annotation_raw.items():
                annotation[int(key)] = value
            return annotation, annotation_raw.get("existed_task", None)
        else:
            return {}, None

    def _save_annotation(self):
        if self._annotation_path is not None:
            save_annotation(self._annotation_path, {"existed_task":self._existed_task,
                                                                    'video_name': self._video_name,
                                                                    'fps': self._fps,
                                                                    'width': self._width,
                                                                    'height' : self._height,
                                                                    "frame_annotations": self._annotation})

    @abstractmethod
    def add_frame_annotation(self, frame:int, annotation, save = True):
        if frame not in self._annotation:
            self._annotation[int(frame)] = annotation
            if save:
                self._save_annotation()

    def force_save(self):
        self._save_annotation()

    def has_annotation(self, frame:int)->bool:
        return frame in self._annotation.keys()

    @abstractmethod
    def get_frame_annotation(self, frame:int):
        try:
            return self._annotation[frame]
        except Exception:
            return None

    @abstractmethod
    def get_full_annotation(self):
        return self._annotation

    def get_existed_task(self):
        return self._existed_task

    def set_existed_task(self, task_id):
        self._existed_task = task_id
