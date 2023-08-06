import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QMainWindow
from PyQt5.QtWidgets import QSizePolicy, QGridLayout
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QIcon

# to import from this project without instalation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from settings_widget import SettingsWidget
from blyzer.common.settings import BlyzerSettings
from blyzer.client2.gui.about_widget import AboutWidget
from blyzer.client2.preview import Preview
from blyzer.client2.project_manager import ProjectManager
from blyzer.client2.gui.new_project_dialog import NewProjectDialog

DEFAULT_SETTING_FILE_NAME = "settings.json"
APP_NAME = "automatic-behavior-analysis-client"


class Client_GUI(QMainWindow):
    onOpenFile = pyqtSignal(str)
    onOpenFolder = pyqtSignal(str)
    onClose = pyqtSignal()

    def __init__(self, title, min_width, min_height, args):
        super().__init__()

        self.config = BlyzerSettings()

        self._title = title  # type:String
        self._min_width = min_width
        self._min_height = min_height

        self._project_manager = ProjectManager()
        self._preview = Preview()
        self._project_manager.open_file.connect(self._preview.open_file)
        self._project_manager.project_opened.connect(self.on_project_opened)
        self.onClose.connect(self._preview.onCloseListener)

        self.initUI()
        self.setAttribute(Qt.WA_DeleteOnClose, True)


    def initUI(self):
        """constructs the GUI  """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.setWindowTitle(self._title)

        ### creating the menu ###
        self._menu_bar = self.menuBar()

        self._menu_file = self._menu_bar.addMenu("File")

        action = self._menu_file.addAction("New project")
        action.triggered.connect(self.new_project_clicked)

        action = self._menu_file.addAction("Open project")
        action.triggered.connect(self.open_project_clicked)

        self._menu_file.addSeparator()

        action = self._menu_file.addAction("Save video")
        action.triggered.connect(self.save_clicked)

        self._menu_file.addSeparator()

        action = self._menu_file.addAction("Exit")
        action.triggered.connect(self.exit_clicked)

        self._menu_plugin = self._menu_bar.addMenu("Analysis")
        self._preview.set_menu(self._menu_plugin)

        self._project_menu = self._menu_bar.addMenu("Project")
        self._project_manager.set_menu(self._project_menu)

        self._menu_settings = self._menu_bar.addMenu("Settings")
        self._menu_settings.addSeparator()
        action = self._menu_settings.addAction("Edit Settings")
        action.triggered.connect(self.settings_edit_clicked)

        self._menu_help = self._menu_bar.addMenu("Help")
        self._menu_help.addSeparator()
        action = self._menu_help.addAction("About")
        action.triggered.connect(self.about_clicked)

        ### create status bar ###

        self.status_bar = self.statusBar()
        self._preview.set_status_bar(self.status_bar)
        self.status_bar.showMessage('Ready')

        ws = self.config.getParam('window', {})
        q = QDesktopWidget().availableGeometry()  # Get screen size

        ### Widgets ###
        self._main_widget = QWidget()
        self._main_widget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        mainLayout = QGridLayout()
        mainLayout.setSpacing(5)

        project_info = self._project_manager.get_widget()
        mainLayout.addWidget(project_info, 0, 0, -1, 3)

        preview = self._preview.getWidget()
        mainLayout.addWidget(preview, 0, 4, -1, 10)

        self._main_widget.setLayout(mainLayout)
        self.setCentralWidget(self._main_widget)

        # Set main windows geometry
        width = ws.get('width') or max(q.width() // 2, self._min_width)
        height = ws.get('height') or max(q.height() // 2, self._min_height)
        x = ws.get('x') or (q.width() - width) // 2
        y = ws.get('y') or (q.height() - height) // 2
        self.setGeometry(x, y, width, height)

        # Icon
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
        QApplication.instance().setWindowIcon(QIcon(os.path.join(res_path,"blyzer_logo.ico")))

        # Show gui
        self.show()

    @pyqtSlot()
    def save_clicked(self):
        self._preview.save_video()


    @pyqtSlot()
    def new_project_clicked(self):
        dialog = NewProjectDialog()
        value = dialog.exec_()
        if value:
            self._project_manager.create_project(value[1], value[0], value[2])

    @pyqtSlot()
    def open_project_clicked(self):
        """Handler clicking on open file"""
        file_name = QFileDialog.getOpenFileName(self, "Open project",
                                                self.config.getParam('last_open_dir', "./"),
                                                "Blyzer projects (*.blzprj) ;; All files (*.*)")[0]
        if file_name:
            self.config.setParam('last_open_dir', os.path.dirname(file_name), force=True)
            print("Opening project: {}".format(file_name))
            self._project_manager.open_project(file_name)

    @pyqtSlot()
    def about_clicked(self):
        self.aboutWidget = AboutWidget()
        self.aboutWidget.show()

    @pyqtSlot()
    def settings_edit_clicked(self):
        self.settingsWidget = SettingsWidget()
        self.settingsWidget.show()

    @pyqtSlot()
    def exit_clicked(self):
        self.onClose.emit()
        self.deleteLater()
        QApplication.closeAllWindows()
        QCoreApplication.instance().quit()

    @pyqtSlot(str)
    def on_project_opened(self, project_name):
        self.setWindowTitle("{} : {}".format(project_name, self._title))

    def closeEvent(self, event):
        pass
        # msg = QMessageBox(self)
        # msg.setIcon(QMessageBox.Question)
        # msg.setWindowTitle('Exit')
        # msg.setText(
        #     'Did you save the statistics? (to save the statistics, give the dogs names and click on the "Save statistic" button)')
        # no = msg.addButton(
        #     'No', QMessageBox.NoRole)
        # yes = msg.addButton(
        #     'Yes', QMessageBox.YesRole)
        # msg.setDefaultButton(yes)
        # msg.exec_()
        # msg.deleteLater()
        # if msg.clickedButton() is yes:
        #     self.exit_clicked()
        #     event.accept()
        # else:
        #     event.ignore()
