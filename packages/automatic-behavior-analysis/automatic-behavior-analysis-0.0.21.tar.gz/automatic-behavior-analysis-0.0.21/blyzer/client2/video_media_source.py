import sys, traceback
from abc import abstractmethod

from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from videowidget import MediaSource
from blyzer.common.settings import BlyzerSettings
from blyzer.common.video import AnnotatedVideo


class VideoMediaSource(MediaSource):
    def __init__(self):
        super().__init__()

    @pyqtSlot(AnnotatedVideo)
    def set_source(self, annotated_video):
        self._cur_video = annotated_video
        preview = self._cur_video.preview.copy()
        convertToQtFormat = QImage(preview.data, preview.shape[1], preview.shape[0], QImage.Format_RGB888)
        preview = convertToQtFormat.scaled(1920, 1080, Qt.KeepAspectRatio)
        self.changePreview.emit(preview.copy())

        self._image_number = -1
        self._current_position = 0
        self._source_width, self._source_height = self._cur_video.get_video_size()
        self._frame_count = self._cur_video.get_frames_count()
        self._fps =  self._cur_video.get_fps()

        print("Opened video: {}".format(self._cur_video.get_path()))
        self.video_params = {
            'width': self._source_width,
            'height': self._source_height,
            'frame_count': self._frame_count,
            'filename': self._cur_video.get_path(),
            'fps':self._fps
        }
        self.metaDataChanged.emit(self.video_params)

    def save_output_video(self, white_bg = False, save_path = None):
        self._cur_video.save_annotated_video(white_bg, save_path)

    @abstractmethod
    def changePosition(self, position):
        # TODO: Переход на новую позицию в файле. Обработка кэша.
        print('changePosition', position)
        self._image_number = position
        self._current_position = position

    # Inherit from MediaSource
    @abstractmethod
    def loadPrevFrame(self):
        try:
            frame = self._cur_video.get_raw_frame(self._current_position - 1)
            if frame is not None:
                self._current_position -= 1
                return self._current_position - 1, frame
            else:
                return None, None
        except:
            return None, None

    @abstractmethod
    def loadNextFrame(self):
        try:
            frame = self._cur_video.get_frame(self._current_position)
            if frame is not None:
                self._current_position += 1
                return self._current_position - 1, frame
            else:
                print("Frame is not exists")
                return None, None
        except Exception as E:
            print(E)
            traceback.print_tb(E.__traceback__)
            return None, None
