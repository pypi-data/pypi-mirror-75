import os
import csv
from csv import DictWriter

from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QListWidget, QAction
from PyQt5.QtWidgets import QFileDialog

from blyzer.common.video import AnnotatedVideo
from blyzer.common.blyzer_project import BlyzerProject
from blyzer.common.settings import BlyzerSettings
from blyzer.client2.neural_processor import NeuralProcessor
from statistic_holder import StatisticHolder

class ProjectManager(QObject):
    open_file = pyqtSignal(AnnotatedVideo)
    project_opened = pyqtSignal(str)

    process_video = pyqtSignal(AnnotatedVideo)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_project = None

        self._menu_project = None
        self._status_bar = None
        self._videos_list_widget = None

        self._refresh_timer = QTimer()
        self._refresh_timer.timeout.connect(self._refresh)

        self._video_processor = NeuralProcessor()
        self._video_processor.end_of_process.connect(self.end_video_process)
        self.process_video.connect(self._video_processor.process_file)

        self._processing_queue = {}
        self._force_rescan_counter = 10

        self._inprocessing_video_name = ""

    ### PUBLIC METHODS ###

    def create_project(self, project_dir: str, project_name: str, model_path: str, project_version=1):

        new_project = BlyzerProject.create_project(project_dir,
                                                   project_name,
                                                   model_path,
                                                   project_version)
        self.open_project(new_project)

    def open_project(self, prj_path: str):
        self._current_project = BlyzerProject(prj_path)
        self._video_processor.setup_model(self._current_project.get_model_path())
        self._refresh_timer.start(5000)
        self._activate_menu()
        self._refresh()
        self.project_opened.emit(self._current_project.get_project_name())

    def close_project(self):
        """ """
        self._refresh_timer.stop()

    def set_menu(self, root_menu):
        """ setting the actions to the menu """
        self._menu_project = root_menu

        action = self._menu_project.addAction("Add video")
        action.triggered.connect(self.add_video_clicked)

        action = self._menu_project.addAction("Add folder")
        action.triggered.connect(self.add_folder_clicked)

        self._menu_project.addSeparator()

        _composition_menu = self._menu_project.addMenu("Report composition")
        self._is_save_statistics = QAction("Summary statistics (csv)" , checkable=True)
        _composition_menu.addAction(self._is_save_statistics)
        self._is_save_video = QAction("Video (mp4)" , checkable=True)
        _composition_menu.addAction(self._is_save_video)
        self._is_save_trajectory = QAction("Trajectory (csv)" , checkable=True)
        _composition_menu.addAction(self._is_save_trajectory)


        action = self._menu_project.addAction("Save summary statistics as")
        action.triggered.connect(self.save_all_summary_clicked)

        action = self._menu_project.addAction("Save report to")
        action.triggered.connect(self.save_report_clicked)

        self._deactivate_menu()

    def get_widget(self):
        """ creating widget for project manager """
        self._videos_list_widget = QListWidget()
        self._videos_list_widget.itemClicked.connect(self._videos_list_widgetclicked)

        return self._videos_list_widget

    def set_status_bar(self, status_bar):
        self._status_bar = status_bar

    ### PRIVATE METHODS ###

    def _deactivate_menu(self):
        if self._menu_project is not None:
            self._menu_project.setEnabled(False)

    def _activate_menu(self):
        if self._menu_project is not None:
            self._menu_project.setEnabled(True)

    def _update_video_list(self):
        if self._videos_list_widget is None:
            return
        self._videos_list_widget.clear()

        if self._force_rescan_counter <= 0:
            self._current_project.rescan_folder()
            self._force_rescan_counter -= 1
        else:
            self._current_project.rescan_folder(force=True)
            self._force_rescan_counter = 10

        for i in range(self._current_project.get_video_count()):
            name, progress = self._current_project.get_video_base_info(i)
            self._videos_list_widget.addItem("[{:.1%}] - {}".format(progress, name))
            if (progress < 1.0
                    and name not in self._processing_queue
                    and name != self._inprocessing_video_name):
                self._processing_queue[name] = self._current_project.get_video(i)

    def _process_next_video(self):
        if not self._video_processor.is_bisy and len(self._processing_queue) > 0:
            name, vid = self._processing_queue.popitem()
            self._inprocessing_video_name = name
            self.process_video.emit(vid)
    ### QT SLOTS ###

    @pyqtSlot()
    def on_close_listener(self):
        self.close_project()

    @pyqtSlot()
    def _refresh(self):
        self._update_video_list()
        self._process_next_video()

    @pyqtSlot()
    def add_video_clicked(self):
        file_name = QFileDialog.getOpenFileName(None, "Open video",
                                                BlyzerSettings().getParam('last_open_video_dir',
                                                                          "./"),
                                                "Video files (*.mp4) ;; All files (*.*)")[0]
        if file_name:
            BlyzerSettings().setParam('last_open_video_dir', os.path.dirname(file_name), force=True)
            print("Add video: {}".format(file_name))
            self._current_project.add_video_path(file_name)
            self._refresh()

    @pyqtSlot()
    def add_folder_clicked(self):
        folder_name = QFileDialog.getExistingDirectory(
            None, "Select Folder", BlyzerSettings().getParam('last_open_video_dir', "./"))
        if folder_name:
            BlyzerSettings().setParam('last_open_video_dir', folder_name, force=True)
            print("Add folder: {}".format(folder_name))
            self._current_project.add_video_folder(folder_name)
            self._refresh()

    def _save_all_summary(self, path):
        for i in range(self._current_project.get_video_count()):
            name, progress = self._current_project.get_video_base_info(i)
            if progress == 1.0:
                vid = self._current_project.get_video(i)
                summary = self._get_summary_from_video(vid)
                summary["File name"] = os.path.basename(vid.get_path())
                if os.path.exists(path):
                    with open(path, 'a+', newline='') as write_obj:
                        # Create a writer object from csv module
                        dict_writer = DictWriter(write_obj, fieldnames=list(summary.keys()))
                        # Add dictionary as wor in the csv
                        dict_writer.writerow(summary)
                else:
                    with open(path, 'w', newline='') as write_obj:
                        # Create a writer object from csv module
                        dict_writer = DictWriter(write_obj, fieldnames=list(summary.keys()))
                        dict_writer.writeheader()
                        dict_writer.writerow(summary)

    @pyqtSlot()
    def save_all_summary_clicked(self):
        path = QFileDialog.getSaveFileName(None,
                                           "Save report",
                                           (os.path.join(BlyzerSettings().getParam('last_open_video_dir', "./")
                                                + self._current_project.get_project_name() + '_summary.csv')),
                                           'CSV(*.csv)')
        print(path)
        path = path[0]
        if path:
            self._save_all_summary(path)


    @pyqtSlot()
    def save_report_clicked(self):
        folder_name = QFileDialog.getExistingDirectory(
            None, "Select Folder", BlyzerSettings().getParam('last_open_video_dir', "./"))
        if folder_name:
            if self._is_save_statistics.isChecked():
                self._save_all_summary(os.path.join(folder_name, self._current_project.get_project_name() + '_summary.csv'))

            for i in range(self._current_project.get_video_count()):
                name, progress = self._current_project.get_video_base_info(i)
                if progress == 1.0:
                    vid = self._current_project.get_video(i)
                    file_name = os.path.basename(vid.get_path()).split('.')[0]
                    fps = vid.get_fps()
                    total_frames = vid.get_frames_count()
                    statistic_holder = StatisticHolder(vid.get_path(), fps, vid.preview, total_frames)
                    for frame_annotation in vid.get_full_annotation().values():
                        statistic_holder.add_frame_annotation(frame_annotation)

                    if self._is_save_video.isChecked():
                        vid.save_annotated_video(save_path = os.path.join(folder_name, file_name + '.mp4'))
                    if self._is_save_trajectory.isChecked():                        
                        path = os.path.join(folder_name, file_name + '_trajectory.csv')
                        tr = statistic_holder.to_dataframe()
                        tr.to_csv(path)

    def _get_summary_from_video(self, video: AnnotatedVideo):
        fps = video.get_fps()
        total_frames = video.get_frames_count()
        statistic_holder = StatisticHolder(video.get_path(), fps, video.preview, total_frames)
        for frame_annotation in video.get_full_annotation().values():
            statistic_holder.add_frame_annotation(frame_annotation)
        basic_statisic = statistic_holder.get_statistics()
        return basic_statisic

    def _videos_list_widgetclicked(self, item):
        v_ind = self._videos_list_widget.indexFromItem(item).row()
        self.open_file.emit(self._current_project.get_video(v_ind))

    @pyqtSlot(str)
    def end_video_process(self, file_name):
        self._inprocessing_video_name = ""
        self._process_next_video()
