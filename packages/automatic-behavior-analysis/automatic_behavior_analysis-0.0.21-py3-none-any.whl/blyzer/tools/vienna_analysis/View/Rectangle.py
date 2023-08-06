from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsItem


class Rectangle(QGraphicsRectItem):

    def __init__(self, x, y, w, h):
        super(Rectangle, self).__init__(0, 0, w, h)
        super().setPen(QPen(Qt.red, 2))
        super().setFlag(QGraphicsItem.ItemIsSelectable)
        super().setFlag(QGraphicsItem.ItemIsMovable)
        super().setFlag(QGraphicsItem.ItemIsFocusable)
        super().setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        super().setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        super().setPos(QPointF(x, y))

    def mouseMoveEvent(self, e):
        x = e.pos().x()
        y = e.pos().y()
        if e.buttons() == Qt.LeftButton:
            super().mouseMoveEvent(e)
        if e.buttons() == Qt.RightButton:
            super().setRect(QRectF(0, 0, x, y))

    def itemChange(self, change, val):
        if change == QGraphicsItem.ItemPositionChange:
            return QPointF(val.x(), val.y())
        return val