from abc import abstractmethod

import numpy as np
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtCore import QThread

from blyzer.client2.remote_neural_processor import RemoteNeuralProcessor
from blyzer.common.video import AnnotatedVideo


"""
File contains plugins for dogs
"""


class NeuralProcessor(QObject):
    """ Plugin for video processing"""

    requestDataProcess = pyqtSignal(np.ndarray, dict)
    requestVideoProcess = pyqtSignal(str, str, int)
    setupModel = pyqtSignal(str)
    stopRemoteNeuralProcessor = pyqtSignal()

    end_of_process = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_video = None
        self._current_file = None

        self._frameProcessor = RemoteNeuralProcessor()
        self._processorThread = QThread()

        self._frameProcessor.finished.connect(self._processorThread.quit)
        self._frameProcessor.nextDataLoaded.connect(self.nextDataLoaded)
        self._frameProcessor.end_of_file.connect(self.onEndOfFile)
        self._frameProcessor.moveToThread(self._processorThread)

        self.requestVideoProcess.connect(self._frameProcessor.processVideo)
        self.setupModel.connect(self._frameProcessor.setup_model)
        self.stopRemoteNeuralProcessor.connect(self._frameProcessor.stopRequest)

        self._processorThread.started.connect(self._frameProcessor.run)
        self._processorThread.finished.connect(self._processorThread.deleteLater)
        self._processorThread.start()

        self.is_bisy = False

    def setup_model(self, model_path):
        self.setupModel.emit(model_path)

    @pyqtSlot(AnnotatedVideo)
    def process_file(self, video: AnnotatedVideo):
        """
        start processing the video inside the filename
        Setting the GUI for the file processing

        :param filename: full path of file
        """
        self._current_video = video
        self._current_file = video.get_path()
        print("self.setVideoSrc.emit(self._current_video)")
        if len(self._current_video.get_full_annotation()) >= self._current_video.get_frames_count():
            self.end_of_process.emit(self._current_file)
        else:
            self.is_bisy = True
            self.requestVideoProcess.emit(self._current_file,
                                          self._current_video.get_existed_task(),
                                          len(self._current_video.get_full_annotation()))


    @pyqtSlot(dict)
    def nextDataLoaded(self, response):
        self._current_video.update_frame_annotation(response['response'])
        self._current_video.set_existed_task(response['task_id'])

    def close(self):
        pass

    @pyqtSlot(str)
    def onEndOfFile(self, file_name):
        self.is_bisy = False
        self.end_of_process.emit(file_name)
        print("End of file")
