from PyQt5.QtCore import Qt, QObject, QThread, QTimer
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QSlider
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QStyle, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
from abc import abstractmethod
import cv2
import numpy as np

class MediaSource(QObject):
    """ A class that defines media source functionality"""
    changePreview = pyqtSignal(QImage)  # Изображение
    changePixmap = pyqtSignal(int, QImage)  # Номер фрейма, Изображение
    finished = pyqtSignal()
    metaDataChanged = pyqtSignal(dict)  # Словарь с метаданными медиа
    newStatisticData = pyqtSignal(dict)

    @abstractmethod
    def run(self):
        print("Base class run")
        self.cap = cv2.VideoCapture(0)
        self.is_run = True

    @pyqtSlot(int)
    def moveTo(self, position):
        self.changePosition(position)

    @pyqtSlot()
    def stopRequest(self):
        QThread.currentThread().exit()

    @pyqtSlot()
    def metadataRequest(self):
        meta = self.getMediaMetaData()
        if meta is not None:
            self.metaDataChanged.emit(meta)

    @pyqtSlot()
    def nextFrameRequest(self):
        position, frame = self.loadNextFrame()
        if frame is not None:
            convertToQtFormat = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            frame = convertToQtFormat.scaled(1920, 1080, Qt.KeepAspectRatio)
            self.changePixmap.emit(position, frame.copy())

    @pyqtSlot()
    def prevFrameRequest(self):
        position, frame = self.loadPrevFrame()
        if frame is not None and position > -1:
            convertToQtFormat = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            frame = convertToQtFormat.scaled(1920, 1080, Qt.KeepAspectRatio)
            self.changePixmap.emit(position, frame.copy())

    @abstractmethod
    def changePosition(self, position):
        pass

    @abstractmethod
    def loadNextFrame(self):
        ret, frame = self.cap.read()
        p = None
        if ret:
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        return None, p

    @abstractmethod
    def loadPrevFrame(self):
        return None, None

    @abstractmethod
    def getMediaMetaData(self):
        return None


class VideoWidget(QWidget):
    """The class represents the  GUI widget"""

    playCMD = pyqtSignal()
    pauseCMD = pyqtSignal()
    moveTo = pyqtSignal(int)
    frameRequest = pyqtSignal()
    prevFrameRequest = pyqtSignal()
    stopRequest = pyqtSignal()
    mediametaRequest = pyqtSignal()

    def __init__(self, media_source=None, parent=None):
        super().__init__(parent)
        self.initUI()

        if media_source is None:  # В отладочных целях, если нет источника загружается с камеры
            print("Use default mediadource")
            self._media_source = MediaSource()
        else:
            self._media_source = media_source

        # creates new thread for video player
        self.objThread = QThread()

        # connects the thread functionality with MediaSource
        self._media_source.finished.connect(self.objThread.quit)
        self._media_source.changePixmap.connect(self.setImage)
        self._media_source.changePreview.connect(self.setPreview)
        self._media_source.metaDataChanged.connect(self.updateMediaMeta)

        # connects the GUI with the MediaSource functionality
        self.frameRequest.connect(self._media_source.nextFrameRequest)
        self.prevFrameRequest.connect(self._media_source.prevFrameRequest)
        self.stopRequest.connect(self._media_source.stopRequest)
        self.mediametaRequest.connect(self._media_source.metadataRequest)
        self.moveTo.connect(self._media_source.moveTo)

        self._media_source.moveToThread(self.objThread)

        self.objThread.started.connect(self._media_source.run)
        self.objThread.finished.connect(self.mediaFinished)
        self.objThread.finished.connect(self.objThread.deleteLater)
        self.objThread.start()

        self._fps_timer = QTimer()
        self._fps_timer.timeout.connect(self._nextFrameRequest)
        self._fps_timer_duration = 100

        self._video_is_play = False

    @pyqtSlot()
    def _nextFrameRequest(self):
        self.frameRequest.emit()

    @pyqtSlot()
    def _prevFrameRequest(self):
        self.prevFrameRequest.emit()

    def initUI(self):
        self._canvas = QLabel()
        self._canvas.setAlignment(Qt.AlignCenter)
        self._canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # TODO: add controll layout with timeline and control buttons

        self._root_layout = QVBoxLayout()
        self._control_layout = QHBoxLayout()

        self._play_button = QPushButton()
        self._play_button.setText("Play")
        self._play_button.clicked.connect(self.playButtonClicked)

        self._timeslider = QSlider(Qt.Horizontal)
        self._timeslider.sliderReleased.connect(self.onChangeSliderPosition)

        self._control_layout.addWidget(self._play_button)
        self._control_layout.addWidget(self._timeslider)

        self._root_layout.addWidget(self._canvas)
        self._root_layout.addLayout(self._control_layout)

        self.setLayout(self._root_layout)

    @pyqtSlot()
    def playButtonClicked(self):
        if self._video_is_play:
            self.stop()
        else:
            self.play()

    def play(self):
        self._play_button.setText("Stop")
        self._fps_timer.start(self._fps_timer_duration)
        self._video_is_play = True

    def stop(self):
        self._play_button.setText("Play")
        self._fps_timer.stop()
        self._video_is_play = False

    @pyqtSlot()
    def mediaFinished(self):
        print("Stoped")

    @pyqtSlot()
    def on_delete(self):
        self.stopRequest.emit()

    @pyqtSlot(QImage)
    def setPreview(self, image):
        """sets the image on the screen"""
        try:
            image = image.scaled(int(self.width() * 0.95), int(self.height() * 0.95), Qt.KeepAspectRatio)
        except Exception as e:
            print(str(e))
        self._current_image = QPixmap.fromImage(image)
        self._canvas.setPixmap(self._current_image)

    @pyqtSlot(int, QImage)
    def setImage(self, position, image):
        """sets the image on the screen"""
        self.setPreview(image)
        if position is not None:
            self._timeslider.setValue(position)

    @pyqtSlot(dict)
    def updateMediaMeta(self, metadata):
        """Handling video metadata changes"""
        print(metadata)
        self._timeslider.setMaximum(metadata.get("frame_count", 99))
        self._timeslider.setMinimum(0)
        self._fps_timer_duration = metadata.get("fps", 100)
        return

    @pyqtSlot()
    def onChangeSliderPosition(self):
        """
        Handles a change in the timeline position of a video
        """
        newPos = self._timeslider.value()
        self.moveTo.emit(newPos)
