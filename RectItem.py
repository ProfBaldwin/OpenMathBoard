from math import copysign

import Pen

from PySide6.QtCore import (
        Qt,
        QPointF,
        QRect,
        )

from PySide6.QtWidgets import (
        QApplication, 
        QGraphicsItem,
        QGraphicsRectItem, 
        QGraphicsOpacityEffect,
        )

class RectItem(QGraphicsRectItem):

    undoable = True

    def __init__(self, pen, brush, startPoint, eraser = False, highlighter = False, editMenu = None):
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

        # Edit Menu? (For selection box changes)
        self.editMenu = editMenu


    def addPoint(self, Q, getModifiers = True):

        # Modifiers
        if getModifiers:
            modifiers = QApplication.queryKeyboardModifiers()
            shiftPressed = bool(modifiers & Qt.ShiftModifier)
            ctrlPressed = bool(modifiers & Qt.ControlModifier)
        else:
            shiftPressed = False
            ctrlPressed = False

        # Adjust Q to make circle
        if shiftPressed:
            v = Q - self.P
            max_val = max(abs(v.x()), abs(v.y()))
            v = QPointF(copysign(max_val, v.x()), copysign(max_val, v.y()))
            Q = self.P + v

        # Expand from Center
        if ctrlPressed:
            v = Q - self.P
            R = self.P - v
            self.setRect(QRect.span(R.toPoint(), Q.toPoint()))
        else:
            self.setRect(QRect.span(self.P.toPoint(), Q.toPoint()))


    def sceneBoundingRect(self):
        if self.eraser:
            return QRect()
        return super().sceneBoundingRect()


    def setPen(self, pen):
        self._pen = pen
        super().setPen(pen)


    def pen(self):
        return self._pen


    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedHasChanged and not self.isSelected():

            self.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.setFlag(QGraphicsItem.ItemIsSelectable, False)
            self.unsetCursor()

            self.editMenu.cutAction.setEnabled(False)
            self.editMenu.copyAction.setEnabled(False)

        return value


    def getData(self):
        if self.editMenu is not None:
            return None
        data = {}
        data["type"] = "rect item"
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

    item = RectItem(pen, brush, topLeft, data["eraser"], data["highlighter"])
    item.addPoint(bottomRight)

    return item
