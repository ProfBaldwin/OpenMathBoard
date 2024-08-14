from math import copysign

import Pen

from PySide6.QtCore import (
        Qt,
        QPointF,
        QRect,
        )

from PySide6.QtWidgets import (
        QApplication, 
        QGraphicsEllipseItem, 
        QGraphicsOpacityEffect,
        )

class EllipseItem(QGraphicsEllipseItem):

    undoable = True

    def __init__(self, pen, brush, startPoint, eraser = False, highlighter = False):
        super().__init__()
        
        # Initialize Ellipse Item
        self.P = startPoint
        self.setPen(pen)
        self.setBrush(brush)

        # Eraser?
        self.eraser = eraser

        # Highlighter?
        self.highlighter = highlighter
        if highlighter:
            opacityEffect = QGraphicsOpacityEffect()
            opacityEffect.setOpacity(0.2)
            self.setGraphicsEffect(opacityEffect)


    def addPoint(self, Q):

        # Modifiers
        modifiers = QApplication.queryKeyboardModifiers()
        shiftPressed = bool(modifiers & Qt.ShiftModifier)
        ctrlPressed = bool(modifiers & Qt.ControlModifier)

        if shiftPressed:
            v = Q - self.P
            max_val = max(abs(v.x()), abs(v.y()))
            v = QPointF(copysign(max_val, v.x()), 0.5*(1 + ctrlPressed)*copysign(max_val, v.y()))
            Q = self.P + v

        # Expand from Center
        if ctrlPressed:
            # Adjust Q to make circle
            v = Q - self.P
            R = self.P - v
        else:
            # Adjust Q to make circle
            R = self.P - QPointF(0, Q.y() - self.P.y())

        self.setRect(QRect.span(R.toPoint(), Q.toPoint()))


    def sceneBoundingRect(self):
        if self.eraser:
            return QRect()
        return super().sceneBoundingRect()


    def setPen(self, pen):
        self._pen = pen
        super().setPen(pen)


    def pen(self):
        return self._pen


    def getData(self):
        data = {}
        data["type"] = "ellipse item"
        data["eraser"] = self.eraser
        data["highlighter"] = self.highlighter
        data["top left"] = self.rect().topLeft().toTuple()
        data["bottom right"] = self.rect().bottomRight().toTuple()
        if self._pen != Qt.NoPen:
            data["pen"] = self._pen.getData()
        return data


def loadFromData(data, backgroundBrush):

    if "pen" in data:
        pen = Pen.loadFromData(data["pen"])
    else:
        pen = Qt.NoPen

    if data["eraser"]:
        brush = backgroundBrush
    else:
        brush = Qt.NoBrush

    topLeft = QPointF(*data["top left"])
    bottomRight = QPointF(*data["bottom right"])

    p1 = topLeft + 0.5*QPointF(0, bottomRight.y()-topLeft.y())

    item = EllipseItem(pen, brush, p1, data["eraser"], data["highlighter"])
    item.addPoint(bottomRight)

    return item

