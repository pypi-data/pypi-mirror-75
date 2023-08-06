import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy


class Canvas(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()
        self.canvas = QtGui.QPixmap("frame0.png")
        self.setPixmap(self.canvas)
        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor('red')

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def mouseMoveEvent(self, e):
        if self.last_x is None:  # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return  # Ignore the first time.

        self.setPixmap(self.canvas)
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setColor(self.pen_color)
        painter.setPen(p)

        print(self.last_x, self.last_y, e.x(), e.y())
        painter.drawRect(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setCentralWidget(Canvas())

        self.last_x, self.last_y = None, None



app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
