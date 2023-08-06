import sys
from abc import abstractmethod
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from blyzer.common.settings import BlyzerSettings
'''
This file contains classes for statistics.
Those class are later used on the GUI
'''

# TODO: remove dependency from BlyzerSettings by next steps:
# Create inherited classes for every specific project, make base class virtual
# Choose a classes by value in BlyzerSettings.


class StatisticItemWidget(QtWidgets.QWidget):
    def __init__(self, mode=BlyzerSettings().getParam("project", "Vienna").lower(), parent=None):
        super(StatisticItemWidget, self).__init__(parent)
        self._mode = mode

    @abstractmethod
    def setValue(self, value):
        pass

    @abstractmethod
    def clear(self):
        pass


class SimpleStatisticItemWidget(StatisticItemWidget):
    def __init__(self, mode=BlyzerSettings().getParam("project", "Vienna").lower(), parent=None):
        super(SimpleStatisticItemWidget, self).__init__(
            BlyzerSettings().getParam("project", "Vienna").lower(), parent)
        self._root_layout = QtWidgets.QHBoxLayout()
        self._label_value = QtWidgets.QLabel()
        self._root_layout.addWidget(self._label_value)
        self.setLayout(self._root_layout)

    @abstractmethod
    def setValue(self, value):
        self._label_value.setText(value)

    @abstractmethod
    def clear(self):
        self._label_value.clear()


class RTStatisticItemWidget(StatisticItemWidget):
    """This widget displays real-time stats using labels """
    nameChanged = pyqtSignal(str)

    def __init__(self, mode=BlyzerSettings().getParam("project", "Vienna").lower(), parent=None):
        super(RTStatisticItemWidget, self).__init__(
            BlyzerSettings().getParam("project", "Vienna").lower(), parent)
        self.id = None
        self.name = None
        # creating an HBOX and adding button elements to it

        # creating a VBOX and adding all elements to the VBOX
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()

        self._id = QtWidgets.QLabel()
        self._id.setText("ID: ")
        self.textQVBoxLayout.addWidget(self._id)

        self._pos_x = QtWidgets.QLabel()
        self._pos_x.setText("POS X: ")
        self.textQVBoxLayout.addWidget(self._pos_x)

        self._pos_y = QtWidgets.QLabel()
        self._pos_y.setText("POS Y: ")
        self.textQVBoxLayout.addWidget(self._pos_y)

        if self._mode == 'Atila'.lower():
            self._state = QtWidgets.QLabel()
            self._state.setText("STATE: ")
            self.textQVBoxLayout.addWidget(self._state)

            self.textQHBoxLayout = QtWidgets.QHBoxLayout()

            self._name_label = QtWidgets.QLabel()
            self._name_label.setText("NAME: ")
            self.textQHBoxLayout.addWidget(self._name_label)

            self._name_line_edit = QtWidgets.QLineEdit()
            self._name_button = QtWidgets.QPushButton("Set name")
            self._name_button.clicked.connect(self.nameEdit)
            self.textQHBoxLayout.addWidget(self._name_line_edit)
            self.textQHBoxLayout.addWidget(self._name_button)
            # adding the HBOX to the VBOX
            self.textQVBoxLayout.addLayout(self.textQHBoxLayout)

        self._space = QtWidgets.QLabel()
        self.textQVBoxLayout.addWidget(self._space)
        self.setLayout(self.textQVBoxLayout)

    def setStatistic(self, dog, name):
        """
        sets the labels to display the stats results

        Args:
            dog: dictionary of real-time stats normalized
            name: String of dog name

        """
        if dog:
            self.id = dog.get('id')
            coord = dog.get('coordinates')
            self._id.setText("ID: " + str(self.id))
            center_x = (coord.get('x1') + coord.get('x2')) / 2
            center_y = (coord.get('y1') + coord.get('y2')) / 2
            self._pos_x.setText(
                "POS X: " + str(round(center_x, 3)))
            self._pos_y.setText(
                "POS Y: " + str(round(center_y, 3)))

            if self._mode == 'Atila'.lower():
                self._state.setText("STATE: " + str(dog.get('state')))
                self._name_label.setText("NAME: ")
                self._name_line_edit.setText(name)
        else:
            self.id = None
            self.name = None

            self._id.setText("ID: ")
            self._pos_x.setText("POS X: ")
            self._pos_y.setText("POS Y: ")

            if self._mode == 'Atila'.lower():
                self._state.setText("STATE: ")
                self._name_label.setText("NAME: ")
                self._name_line_edit.setText("")

    def clearRtStatistic(self):
        self._id.setText("ID: ")
        self._pos_x.setText("POS X: ")
        self._pos_y.setText("POS Y: ")
        if self._mode == 'Atila'.lower():
            self._state.setText("STATE: ")
            self._name_label.setText("NAME: ")

    @pyqtSlot()
    def nameEdit(self):
        """ edits the name of the dog """

        self.name = self._name_line_edit.text()
        if self.name != "":
            self.nameChanged.emit(self.name)

    @abstractmethod
    def clear(self):
        self.clearRtStatistic()

    @abstractmethod
    def setValue(self, value):
        dog, name = value
        self.setStatistic(dog, name)
