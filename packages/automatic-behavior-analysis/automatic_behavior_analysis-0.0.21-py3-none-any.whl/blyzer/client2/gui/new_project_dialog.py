import sys
import os

from PyQt5 import  QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.QtWidgets import QSizePolicy, QGridLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog
from blyzer.common.settings import BlyzerSettings


class NewProjectDialog(QDialog):
    def __init__(self):
        super(NewProjectDialog, self).__init__()
        self.setObjectName("self")
        w = 450
        h = 30 * 7 + 1
        self.resize(w, h)
        self.setMinimumSize(QtCore.QSize(w, h))
        self.setMaximumSize(QtCore.QSize(w, h))
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
        self.setWindowIcon(QIcon(os.path.join(res_path, "blyzer_logo.ico")))

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        ## Project name ##
        self.project_name_lbl = QLabel(self)
        self.project_name_lbl.setObjectName("project_name_lbl")
        self.gridLayout.addWidget(self.project_name_lbl, 0, 0, 1, 15)

        self.project_name = QLineEdit(self)
        self.project_name.setObjectName("project_name")
        self.gridLayout.addWidget(self.project_name, 1, 0, 1, 15)

        ## Project path ##
        self.project_path_lbl = QLabel(self)
        self.project_path_lbl.setObjectName("project_path_lbl")
        self.gridLayout.addWidget(self.project_path_lbl, 2, 0, 1, 15)

        self.project_path = QLineEdit(self)
        self.project_path.setObjectName("project_path")
        self.gridLayout.addWidget(self.project_path, 3, 0, 1, 14)

        self.project_path_button = QPushButton(self)
        self.project_path_button.setObjectName("project_path_button")
        self.project_path_button.setSizePolicy(QSizePolicy.Minimum,
                                               QSizePolicy.Minimum)
        self.gridLayout.addWidget(self.project_path_button, 3, 14, 1, 1)
        self.project_path_button.clicked.connect(self.project_path_button_clicked)

        ## Model path ##
        self.model_path_lbl = QLabel(self)
        self.model_path_lbl.setObjectName("model_path_lbl")
        self.gridLayout.addWidget(self.model_path_lbl, 4, 0, 1, 15)

        self.model_path = QLineEdit(self)
        self.model_path.setObjectName("model_path")
        self.gridLayout.addWidget(self.model_path, 5, 0, 1, 14)

        self.model_path_button = QPushButton(self)
        self.model_path_button.setObjectName("model_path_button")
        self.model_path_button.setSizePolicy(QSizePolicy.Minimum,
                                             QSizePolicy.Minimum)
        self.gridLayout.addWidget(self.model_path_button, 5, 14, 1, 1)
        self.model_path_button.clicked.connect(self.model_path_button_clicked)

        ## OK / CHANCEL ##
        self.ok_button = QPushButton(self)
        self.ok_button.setObjectName("ok_button")
        self.gridLayout.addWidget(self.ok_button, 6, 9, 1, 3)
        self.ok_button.clicked.connect(self.ok_clicked)

        self.cancel_button = QPushButton(self)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 6, 12, 1, 3)
        self.cancel_button.clicked.connect(self.reject)

        self.retranslateUi(self)
        self.retrun_val = None

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "New Project"))
        self.project_name_lbl.setText(_translate("Dialog", "Project name"))

        self.project_path_lbl.setText(_translate("Dialog", "Project path (folder)"))
        self.project_path_button.setText(_translate("Dialog", "..."))

        self.model_path_lbl.setText(_translate("Dialog", "Model path (zip)"))
        self.model_path_button.setText(_translate("Dialog", "..."))

        self.ok_button.setText(_translate("Dialog", "Ok"))
        self.cancel_button.setText(_translate("Dialog", "Cancel"))

    def ok_clicked(self):
        self.retrun_val = (self.project_name.text(), self.project_path.text(), self.model_path.text())
        self.accept()

    def project_path_button_clicked(self):
        folderName = QFileDialog.getExistingDirectory(
            self, "Select Folder", BlyzerSettings().getParam('last_open_dir', "./"))
        if folderName:
            self.project_path.setText(folderName)
            BlyzerSettings().setParam('last_open_dir', folderName, force=True)

    def model_path_button_clicked(self):
        file_name = QFileDialog.getOpenFileName(self, "Choose model zip",
                                                BlyzerSettings().getParam('last_open_dir', "./"),
                                                "Zip files (*.zip) ;; All files (*.*)")[0]
        if file_name:
            self.model_path.setText(file_name)
            BlyzerSettings().setParam('last_open_dir', os.path.dirname(file_name), force=True)

    def exec_(self):
        super(NewProjectDialog, self).exec_()
        return self.retrun_val
