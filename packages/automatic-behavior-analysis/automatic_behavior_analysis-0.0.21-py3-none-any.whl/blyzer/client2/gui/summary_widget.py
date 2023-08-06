import sys
import os
import appdirs
import time
import cv2
import csv
from PyQt5.QtCore import Qt, QObject, pyqtSlot, pyqtSignal, QSize
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QMenuBar, QMainWindow
from PyQt5.QtWidgets import QMenu, QFileDialog, QLabel, QTextEdit
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout
from PyQt5.QtGui import QImage, QPixmap, QTextCursor

import numpy as np

class SummaryWidget(QMainWindow):
    TITLE = "Summary"
    def __init__(self, name:str = "report", parent:QWidget = None):
        super().__init__(parent)
        self._report_name = name
        self.initUI()

    def initUI(self):
        self.setWindowTitle(SummaryWidget.TITLE)

        # Set main windows geometry
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        q = QDesktopWidget().availableGeometry()  # Get screen size
        width = q.width() // 2
        height = q.height() // 2
        x = (q.width() - width) // 2
        y = (q.height() - height) // 2
        self.setGeometry(x, y, width, height)

        ### creating the menu ###
        self._menu_bar = self.menuBar()

        self._menu_file = self._menu_bar.addMenu("File")
        action = self._menu_file.addAction("Save all")
        action.triggered.connect(self.save_all_clicked)

        action = self._menu_file.addAction("Save image as")
        action.triggered.connect(self.save_image_as_clicked)

        action = self._menu_file.addAction("Save report as")
        action.triggered.connect(self.save_report_as_clicked)

        self._menu_file.addSeparator()

        action = self._menu_file.addAction("Exit")
        action.triggered.connect(self.exit_clicked)

        # Image summary
        self._heatmap_canvas = QLabel()
        self._heatmap_canvas.setAlignment(Qt.AlignCenter)
        self._heatmap_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Text summary
        self._summary_layout = QVBoxLayout()

        self._summary_text_browser = QTextEdit()
        self._summary_text_browser.setHtml("<h1>{name}</h1> <br> \n".format(name=self._report_name))
        self._summary_layout.addWidget(self._summary_text_browser)
        self._summary_text_browser.setMinimumWidth(300)

        # Setup main layout
        self._main_layout = QHBoxLayout()
        self._main_layout.addWidget(self._heatmap_canvas)
        self._main_layout.addLayout(self._summary_layout)

        self._main_widget = QWidget(self)
        self._main_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._main_widget.setLayout(self._main_layout)
        self.setCentralWidget(self._main_widget)

    def set_heatmap(self, heatmap_im):
        self._heatmap_im = heatmap_im
        convertToQtFormat = QImage(heatmap_im.data, heatmap_im.shape[1], heatmap_im.shape[0], QImage.Format_RGB888)
        frame = convertToQtFormat.scaled(int(self.width() * 0.95), int(self.height() * 0.95), Qt.KeepAspectRatio)
        frame = QPixmap.fromImage(frame)
        self._heatmap_canvas.setPixmap(frame)

    def set_report(self, report):
        """
        report should be dictionary
        """
        self._report = report
        item_template = "<p><b>{k}</b>: {v}</p>\n"
        item_html = ""
        for key, value in report.items():
            item_html += item_template.format(k=key, v=value)

        self._summary_text_browser.moveCursor(QTextCursor.End)
        self._summary_text_browser.insertHtml(item_html)

    def save_image(self, path):
        cv2.imwrite(path, self._heatmap_im)

    def save_report(self, path):
        with open(path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self._report.keys())
            writer.writeheader()
            writer.writerow(self._report)

    @pyqtSlot()
    def save_all_clicked(self):
        directory = QFileDialog.getExistingDirectory(self, "Choose Directory")
        print("Save all report to {}".format(directory))
        self.save_image(os.path.join(directory, self._report_name + '.jpg'))
        self.save_report(os.path.join(directory, self._report_name + '_basic_stat.csv'))
        pass

    @pyqtSlot()
    def save_image_as_clicked(self):
        path = QFileDialog.getSaveFileName(self, "Save report", self._report_name + '_basic_stat.jpg', 'JPEG(*.jpg)')
        print("Save trajectory to {}".format(path))
        self.save_image(path[0])
        pass

    @pyqtSlot()
    def save_report_as_clicked(self):
        path = QFileDialog.getSaveFileName(self, "Save report", self._report_name + '_basic_stat.csv', 'CSV(*.csv)')
        print("Save report to {}".format(path))
        self.save_report(path[0])

    @pyqtSlot()
    def exit_clicked(self):
        pass


if __name__ == "__main__":
    qapp = QApplication(sys.argv)

    sample_frame = np.random.randint(255, size=(1080, 1920, 3))
    sample_frame[:, 960, :] = 0
    sample_frame[540, :, :] = 0

    app = SummaryWidget(name="Report from video 123")
    app.set_heatmap(sample_frame)
    report = {"Average speed": 0.5,
                "Mean error": 0.3}
    app.set_report(report)
    app.show()
    qapp.exec_()
