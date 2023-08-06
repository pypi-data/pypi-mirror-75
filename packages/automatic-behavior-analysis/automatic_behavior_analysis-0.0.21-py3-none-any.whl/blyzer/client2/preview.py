from PyQt5.QtCore import Qt, QObject
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
from PyQt5.QtWidgets import QSizePolicy, QGridLayout
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread, QTimer
from abc import abstractmethod
from statistic_item_widget import StatisticItemWidget
from statistic_widget import StatisticWidget, SummaryStatisticWidget
from statistic_holder import StatisticHolder
from summary_widget import SummaryWidget
from blyzer.common.settings import BlyzerSettings
from blyzer.client2.video_media_source import VideoMediaSource
from blyzer.common.video import AnnotatedVideo

import cv2
import os
import csv
import glob
import numpy as np
from videowidget import VideoWidget

class Preview(QObject):
    """ Plugin for preview result"""
    onClose = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rt_statistic_widget = StatisticWidget()
        self._summary_statistic_widget = SummaryStatisticWidget()

        self._media_source = VideoMediaSource()
        self._media_source.changePixmap.connect(self.frameChanged)

        self._root_widget = None


    def set_menu(self, root_menu):
        """ setting the actions to the menu """
        self._plugin_menu = root_menu#.addMenu("Analysis")
        action = self._plugin_menu.addAction("Summary")
        action.triggered.connect(self.preview_basic_stats_clicked)

        action = self._plugin_menu.addAction("Export Statistics")
        action.triggered.connect(self.save_all_statistic)

        action = self._plugin_menu.addAction("Save trajectory")
        action.triggered.connect(self.save_trajectory)

    def preview_basic_stats_clicked(self):
        try:
            base = os.path.basename(self._current_video.get_path())
            name = os.path.splitext(base)[0]
            self.summaryWidget = SummaryWidget(name=name)
            heatmap = self._statistic_holder.create_heatmap(self._video_preview)
            heatmap = self._statistic_holder.create_full_trajectory(heatmap)
            self.summaryWidget.set_heatmap(heatmap)
            basic_statisic = self._statistic_holder.get_statistics()
            self.summaryWidget.set_report(basic_statisic)
            self.summaryWidget.show()
        except AttributeError as e:
            print(e)
            QMessageBox.warning(None, "Basic statistic", "Have not statistics", QMessageBox.Cancel)

    def save_all_statistic(self):
        try:
            # self._statistic_holder.save_summary_statistics()
            pass
        except:
            pass

    def update_rt_statistic(self, pos):
        """
        updates real-time stats of the widgets
        Args:
            pos: frame number on the video
        """
        objects = self._media_source._cur_video.get_frame_annotation(pos)['objects']
        self._rt_statistic_widget.set_objects_statistic(objects)

    @pyqtSlot(str)
    def nameChanged(self, obj_id, name):
        pass
        # self._statistic_holder.set_object_name(self._current_viewed_frame, obj_id, name)

    def save_video(self):
        path = QFileDialog.getSaveFileName(None, "Save video", self._current_video.get_path().replace('.mp4', '_output.mp4'), 'MP4(*.mp4)')
        path = path[0]
        if path:
            self._media_source.save_output_video(save_path=path)

    def save_trajectory(self):
        is_view_traj = BlyzerSettings().getParam("show_trajectory", True)

        path = QFileDialog.getSaveFileName(None, "Save trajectory video", self._current_video.get_path().replace('.mp4', '_trajectory.mp4'), 'MP4(*.mp4)')
        path = path[0]
        if path:
            self._media_source.save_output_video(white_bg=True, save_path=path)


        path = QFileDialog.getSaveFileName(None, "Save trajectory to csv", self._current_video.get_path().replace('.mp4', '.csv'), 'CSV(*.csv)')
        path = path[0]
        if path:
            tr = self._statistic_holder.to_dataframe()
            tr.to_csv(path)
        BlyzerSettings().setParam("show_trajectory", is_view_traj, force=True)

    def get_rt_statistic_widget(self):
        return self._rt_statistic_widget

    def get_summary_statistic_widget(self):
        return self._summary_statistic_widget

    def close(self):
        pass

    def getWidget(self):
        ### creating video widget ###
        ### setting layout of the GUI window ###
        self._grid_layout = QGridLayout()
        self._grid_layout.setSpacing(5)

        self._videoview = VideoWidget(media_source=self._media_source)
        self.onClose.connect(self._videoview.on_delete)
        self._videoview.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        ### adding widgets to the layout ###
        self._grid_layout.addWidget(self._videoview, 0, 0, -1, 10)
        self._grid_layout.addWidget(QLabel("Dog coordinates"), 0, 10, 1, 1)
        self._grid_layout.addWidget(self._rt_statistic_widget, 1, 10, 10, 3)
        self._grid_layout.setRowStretch(1, 1)
        self._grid_layout.addWidget(QLabel("Summary"), 11, 10, 1, 1)
        self._grid_layout.addWidget(self._summary_statistic_widget, 12, 10, 10, 3)
        self._grid_layout.setRowStretch(12, 2)

        self._root_widget = QWidget()
        self._root_widget.setLayout(self._grid_layout)
        return self._root_widget

    def set_status_bar(self, status_bar):
        self.status_bar = status_bar

    def _open_file(self, video:AnnotatedVideo):
        """
        start processing the video inside the filename
        Setting the GUI for the file processing

        :param filename: AnnotatedVideo object
        """
        self._current_video = video

        self._media_source.set_source(self._current_video)
        self.status_bar.showMessage(self._current_video.get_path())

        total_frames = self._media_source._cur_video.get_frames_count()
        fps = self._media_source._cur_video.get_fps()
        self._video_preview = self._media_source._cur_video.preview.copy()

        self._rt_statistic_widget.deleteAll()
        self._summary_statistic_widget.deleteAll()

        self._statistic_holder = StatisticHolder(self._current_video.get_path(), fps, self._video_preview, total_frames)
        for frame_annotation in self._current_video.get_full_annotation().values():
            self._statistic_holder.add_frame_annotation(frame_annotation)
        self._current_video.add_custom_frame_decorator(self._statistic_holder.custom_frame_decorator)
        self._summary_statistic_widget.setSummaryStatistic(self._statistic_holder.get_summary_statistics())

    @pyqtSlot()
    def onCloseListener(self):
        self.onClose.emit()

    @pyqtSlot(int, QImage)
    def frameChanged(self, position, image):
        """

        """
        self._current_viewed_frame = position
        self.update_rt_statistic(position)


    @pyqtSlot(AnnotatedVideo)
    def open_file(self, video:AnnotatedVideo):
        self._default_name = None
        self._open_file(video)
