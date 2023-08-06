from PyQt5.QtCore import QObject, QThread, QTimer
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from blyzer.common.settings import BlyzerSettings
import blyzer.server.python_api.blyzer_api as api

class RemoteNeuralProcessor(QObject):
    """The class for the asynchronous image processor."""
    onError = pyqtSignal(str)
    finished = pyqtSignal()
    nextDataLoaded = pyqtSignal(dict)
    end_of_file = pyqtSignal(str)

    on_server_connect_error = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()
        self.ip = BlyzerSettings().getParam("ip")
        self.port = BlyzerSettings().getParam("port")
        self._cache_file_name = None
        self._api = api.InferenceApi(self.ip, self.port)
        self._tasks_queue = {}
        self._task_checker_timer = None

    def start_connection(self):
        # TODO: Checking server availability
        self._task_checker_timer = QTimer()
        self._task_checker_timer.timeout.connect(self._resultChecker)
        self._task_checker_timer.start(2000)

    def close_connection(self):
        self._task_checker_timer.stop()

    def process_new_response(self, response, video_path, task_id):
        self.nextDataLoaded.emit({'response':response, 'video_path':video_path, 'task_id':task_id})

    def run(self):
        """The function is called when the thread starts, can be used as a constructor"""
        print("RemoteNeuralProcessor Start")
        self.start_connection()

    @pyqtSlot(str)
    def setup_model(self, model_path):
        self._api.upload_model(model_path)

    @pyqtSlot()
    def _resultChecker(self):
        closed_tasks = []
        for task_id, video_path in self._tasks_queue.items():
            result, is_all = self._api.get_result(task_id)
            if result is not None:
                self.process_new_response(result, video_path, task_id)
                if is_all:
                    closed_tasks.append(task_id)
                    self.end_of_file.emit(video_path)
        for task_id in closed_tasks:
            self._tasks_queue.pop(task_id)

    @pyqtSlot(str, str, int)
    def processVideo(self, video_path, existed_task=None, progress=0):
        print("processVideo(self, video_path):", video_path, existed_task)
        task_id = None
        if existed_task is not None:
            result, _ = self._api.get_result(existed_task)
            if result is not None:
                task_id = existed_task
            else:
                task_id = self._api.upload_video(video_path, progress)
        else:
            task_id = self._api.upload_video(video_path, progress)
        if task_id is not None:
            self._tasks_queue[task_id] = video_path

    def close(self):
        """
        Strictly synchronous (in the stream) method, we call when we request the completion
        of the stream in this method you need to free resources if necessary
        """
        self.close_connection()

    @pyqtSlot()
    def stopRequest(self):
        self.close()
        QThread.currentThread().exit()
