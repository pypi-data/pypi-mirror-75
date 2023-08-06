import sys
import os
import json
from functools import partial

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidget, QPushButton, QVBoxLayout, QLabel, QTableWidgetItem, \
    QMessageBox, QComboBox, QColorDialog
from PyQt5.QtCore import Qt
from blyzer.common.settings import BlyzerSettings

APP_NAME = "blyzer"


class SettingsWidget(QWidget):
    typelist = []

    def __init__(self, parent=None):
        super().__init__(parent)

        self._res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Manage Settings")
        self.main_layout = QVBoxLayout()

        # create label for title
        self.lable_widget = QLabel()
        self.lable_widget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lable_widget.setAutoFillBackground(True)
        self.lable_widget.setAlignment(QtCore.Qt.AlignCenter)
        self.lable_widget.setObjectName("TitleLabel")
        self.lable_widget.setText("Settings")
        self.main_layout.addWidget(self.lable_widget)

        # Create save button
        self.save_button = QPushButton()
        self.save_button.setObjectName("btnSave")
        self.save_button.setToolTip("Button that saves changes in settings.")
        self.save_button.setText("Save Changes")
        self.save_button.setFixedSize(200, 25)
        self.save_button.clicked.connect(self.save_settings)
        self.main_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)

        # Create reset button
        self.reset_button = QPushButton()
        self.reset_button.setObjectName("btnReset")
        self.reset_button.setToolTip("Button that resets changes in settings.")
        self.reset_button.setText("Reset Changes")
        self.reset_button.setFixedSize(200, 25)
        self.reset_button.clicked.connect(self.reset_settings)
        self.main_layout.addWidget(self.reset_button, alignment=Qt.AlignCenter)

        # create table
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setObjectName("tableWidget")
        self.table_widget.setToolTip("This table that holds current settings and allows changing them")
        self.table_widget.setRowCount(0)
        self.table_widget.setHorizontalHeaderLabels(['Label', 'Value'])
        self.fill_table()
        self.table_widget.itemClicked.connect(self.item_clicked)
        self.main_layout.addWidget(self.table_widget)

        width = self.table_widget.columnWidth(0) + self.table_widget.columnWidth(1) + 60
        self.setMinimumWidth(width)
        self.setMinimumHeight(self.table_widget.height())
        self.setLayout(self.main_layout)
        self.setWindowFlag(Qt.Dialog and Qt.MSWindowsFixedSizeDialogHint)

    def fill_table(self):
        """
            This method reads the settings from json file and adds them to the table
        """
        filename = BlyzerSettings.get_settings_filename()
        self.typelist = []
        with open(filename) as mysettings:
            data = mysettings.read()
            obj = json.loads(data)
        for x in obj:
            rowposition = self.table_widget.rowCount()
            self.table_widget.insertRow(rowposition)
            self.add_type(rowposition, obj[x])
            self.table_widget.setItem(rowposition, 0, QTableWidgetItem(x))
            if isinstance(obj[x], bool):
                self.add_bool_combo_box(rowposition, str(obj[x]))
            elif "color" in str(x):
                self.add_color_picker(rowposition, str(obj[x]))
            else:
                self.table_widget.setItem(rowposition, 1, QTableWidgetItem(str(obj[x])))
            # set column 0 to can't edit
            item = self.table_widget.item(rowposition, 0)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
        # Resize the table columns to it's contents
        self.table_widget.resizeColumnsToContents()

    def save_settings(self):
        """
            This method saves the new settings if they're all legal
        """
        rowCount = self.table_widget.rowCount()
        if self.check_changes():
            for row in range(rowCount):
                key = self.table_widget.item(row, 0)
                value = self.table_widget.item(row, 1)
                keytext = key.text()
                BlyzerSettings().setParam(keytext, self.string_to_obj(row, value), False)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Settings Changes")
            msg.setInformativeText("Changes were successfully saved")
            msg.setWindowTitle("Message")
            msg.exec_()

    def reset_settings(self):
        """
            This method resets the table values to the values we have in config file
        """
        filename = BlyzerSettings.get_settings_filename()
        with open(filename) as mysettings:
            data = mysettings.read()
            obj = json.loads(data)
        row = 0
        for x in obj:
            if isinstance(obj[x], bool):
                c = self.table_widget.cellWidget(row, 1)
                if isinstance(c, MyQComboBox):
                    if str(obj[x]).lower() == 'false':
                        c.setCurrentIndex(0)
                    else:
                        c.setCurrentIndex(1)
            elif "color" in str(x):
                p = self.table_widget.cellWidget(row, 1)
                if isinstance(p, QPushButton):
                    color = self.get_color(str(obj[x]))
                    p.setStyleSheet("QWidget { background-color: %s}" % color.name())
            else:
                self.table_widget.setItem(row, 1, QTableWidgetItem(str(obj[x])))
            row = row + 1

    def string_to_obj(self, row, value):
        """
            This method turns a string into the value it should be saved as
            Parameters:
                row (int): the row which contains the object
                value (string): the value in that row
            output:
                True or False (boolean): if the value contains a boolean
                String (string) : if the value contains a string
                int : if the value contained an int
                list : if the string contained a list
        """
        if self.typelist[row] is "int":
            return int(value.text())
        elif self.typelist[row] is "string":
            return value.text()
        elif self.typelist[row] is "bool":
            wid = self.table_widget.cellWidget(row, 1)
            if isinstance(wid, MyQComboBox):
                if wid.currentIndex() == 0:
                    return False
                else:
                    return True
        elif self.typelist[row] is "list":
            w = self.table_widget.cellWidget(row, 1)
            if isinstance(w, QPushButton):
                color = w.palette().button().color()
                return [color.red(), color.green(), color.blue()]
            else:
                return self.string_to_list(value.text())

    def add_bool_combo_box(self, row, value):
        """
            This method adds a combo box to the table where there's a boolean object
            and sets the current selection to the given value
            Parameters:
                row (int): the row which contains the object
                value (string): the value in that row (string containing either true or false)
        """
        c = MyQComboBox()
        c.addItems(["False", "True"])
        self.table_widget.setCellWidget(row, 1, c)
        if value.lower() == 'false':
            c.setCurrentIndex(0)
        else:
            c.setCurrentIndex(1)

    def add_color_picker(self, row, value):
        """
            This method adds a color picker to the table where there's a color
            and sets the current selection to the given color
            Parameters:
                row (int): the row which contains the object
                value (string): the value in that row (string containing rbg color)
        """
        default_color = self.get_color(value)
        b = QPushButton()
        self.table_widget.setCellWidget(row, 1, b)
        b.setText("Press to Change Color")
        b.setStyleSheet("QWidget { background-color: %s}" % default_color.name())
        b.clicked.connect(partial(self.color_picker, row))

    def color_picker(self, row):
        """
            This method opens a color picker dialog and when a color is picked it colors it's
            place in the table which choosen color
            Parameters:
                row (int): the row which contains the object
        """
        selected_color = QColorDialog.getColor()
        if selected_color.isValid():
            wid = self.table_widget.cellWidget(row, 1)
            if isinstance(wid, QPushButton):
                wid.setStyleSheet("QWidget { background-color: %s}" % selected_color.name())

    def check_changes(self):
        """
            This method iterates over the table and checks if the parameters are legal
            output:
                True (boolean): if all parameters are valid
                False (boolean): if some parameters are illegal
        """
        # we'd want to color error on all wrong fields so we flag the end result
        flag = True
        rowCount = self.table_widget.rowCount()
        for row in range(rowCount):
            key = self.table_widget.item(row, 0)
            value = self.table_widget.item(row, 1)
            keytext = key.text()
            if self.typelist[row] is "string":
                # validate ip address
                if "ip" in keytext:
                    if not self.validate_ip(value.text()):
                        self.color_error(row)
                        flag = False
            if self.typelist[row] is "int":
                if not value.text().isdigit():
                    self.color_error(row)
                    flag = False
        if not flag:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText("Some information is illegal check it")
            msg.setWindowTitle("Error")
            msg.exec_()
            return False
        return True

    def get_color(self, value):
        """
            This method returns a Qcolor from the given string
            Parameters:
                value (string): a string containing an rbg color
        """
        newrgb = value.replace(']', '')
        newrgb = newrgb.replace('[', '')
        r, g, b = newrgb.split(', ')
        return QColor(int(r), int(g), int(b))

    def add_type(self, row, obj):
        """
            This method fills the typelist with type of object in config file
            Parameters:
                row (int): the row which contains the object
                obj (object): an object from config
        """
        if isinstance(obj, bool):
            self.typelist.insert(row, "bool")
        elif isinstance(obj, list):
            self.typelist.insert(row, "list")
        elif isinstance(obj, str):
            self.typelist.insert(row, "string")
        elif isinstance(obj, int):
            self.typelist.insert(row, "int")

    def string_to_list(self, string):
        """
            This methods turns string of list to list
            Parameters:
                string (string): the string which contains the list [__,__,...]
            Output:
                list
        """
        s = string.replace(']', '')
        s = s.replace('[', '')
        n = int(s)
        return [n]

    def validate_ip(self, value):
        """
            This method validates an ip string
            Parameters:
                value (string): the string we want to check if it's an ip
            Output:
                True (boolean): if value is ip
                False (boolean): if value is not ip
        """
        a = value.split('.')
        if len(a) != 4:
            return False
        for x in a:
            if not x.isdigit():
                return False
            i = int(x)
            if i < 0 or i > 255:
                return False
        return True

    def color_error(self, row):
        """
            This method changes the row's background color to red to show that we have error
            Parameters:
                row (int): the row where we want to show error
        """
        self.table_widget.item(row, 0).setBackground(QtGui.QColor(255, 204, 204))
        self.table_widget.item(row, 1).setBackground(QtGui.QColor(255, 204, 204))

    def item_clicked(self):
        """
            This method changes the row's background color back to default once it's clicked on
        """
        row = self.table_widget.currentItem().row()
        if not self.typelist[row] is "list":
            if not self.typelist[row] is "bool":
                self.table_widget.item(row, 0).setBackground(QtGui.QColor(255, 255, 255))
                self.table_widget.item(row, 1).setBackground(QtGui.QColor(255, 255, 255))


class MyQComboBox(QComboBox):
    """
    This class is of a new combobox where the scroll wheel event is "off"  so when the user is
    scrolling down in the settings widget he won't change settings by mistake
    """
    def __init__(self, *args, **kwargs):
        super(MyQComboBox, self).__init__(*args, **kwargs)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def wheelEvent(self, *args, **kwargs):
        if self.hasFocus():
            return None


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    app = SettingsWidget()
    app.show()
    qapp.exec_()
