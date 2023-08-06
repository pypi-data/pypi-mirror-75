from abc import abstractmethod
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from statistic_item_widget import StatisticItemWidget, SimpleStatisticItemWidget, RTStatisticItemWidget


class StatisticWidget(QListWidget):
    on_set_object_name = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._statistic_items = []

    def addStatItem(self, item: StatisticItemWidget):
        self._statistic_items.append(item)  # create real-time stats object
        # create a list to contain real-time widget item
        myQListWidgetItem = QListWidgetItem(self)
        myQListWidgetItem.setSizeHint(item.sizeHint())  # update the size
        self.addItem(myQListWidgetItem)  # add the the widget to the list
        # connecting item to the object
        self.setItemWidget(myQListWidgetItem, item)
        self._connect_item_callbacks(item)

    def deleteItem(self, index):
        item = self._statistic_items[index]
        try:
            item.nameChanged.disconnect()
        except:
            pass
        self.removeItemWidget(self.item(index))
        c_index = index if index >= 0 else len(self._statistic_items)-1
        self.takeItem(c_index)
        self._statistic_items.remove(item)

    def _setItemCount(self, number):
        while len(self._statistic_items) < number:
            self.addStatItem(self._get_new_item())

        while len(self._statistic_items) > number:
            self.deleteItem(-1)

    def set_objects_statistic(self, objects):
        self._setItemCount(len(objects))

        for ind, obj in enumerate(objects):
            #obj_id = obj.get('id')
            name = obj.get('name', None)
            self._statistic_items[ind].setStatistic(obj, name)

    def deleteAll(self):
        while len(self._statistic_items) > 0:
            self.deleteItem(-1)
        # self.clear()

    @pyqtSlot(str)
    def nameChanged(self, name):
        sender = self.sender()
        if sender.id != None:
            self.on_set_object_name.emit(sender.id, name)

    @abstractmethod
    def _get_new_item(self):
        return RTStatisticItemWidget()

    @abstractmethod
    def _connect_item_callbacks(self, item):
        item.nameChanged.connect(self.nameChanged)


class SummaryStatisticWidget(StatisticWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setSummaryStatistic(self, summary: dict):
        """
        Update summary
        summary -- dict with pairs of Name -- value
        """
        self._setItemCount(len(summary))

        for i, key in enumerate(summary.keys()):
            self._statistic_items[i].setValue(
                "{key}: {value}".format(key=key, value=summary[key]))

    @abstractmethod
    def _get_new_item(self):
        return SimpleStatisticItemWidget()

    @abstractmethod
    def _connect_item_callbacks(self, item):
        pass
