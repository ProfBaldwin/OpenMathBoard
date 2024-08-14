import numpy as np

import Pen

from CatmullRomSpline import catmullRomSpline

from PySide6.QtCore import (
        Qt, 
        QRectF, 
        QPointF, 
        QLineF,
        )

from PySide6.QtGui import (
        QPainterPath,
        QBrush, 
        QPen, 
        )

from PySide6.QtWidgets import (
        QApplication,
        QGraphicsPathItem,
        QGraphicsLineItem,
        QGraphicsEllipseItem,
        QGraphicsItemGroup,
        QGraphicsOpacityEffect,
        )


MAX_SEGMENTS_PER_SUBPATH = 100
CATMULL_TRIGGER_DIST_SQ = 10.0

class WriteItem(QGraphicsItemGroup):

    undoable = True

    def __init__(self, pen, startPoint, highlighter = False):
        super().__init__()

        # Pen
        self._pen = pen

        # Start Point
        self.P = startPoint

        # Point list
        self.pointList = [startPoint.toTuple()]

        # Highlighter?
        self.highlighter = highlighter
        if highlighter:
            opacityEffect = QGraphicsOpacityEffect()
            opacityEffect.setOpacity(0.2)
            self.setGraphicsEffect(opacityEffect)

        # Initialize Item Memory and the Bounding Rect
        self.currentSubpathItem = None
        self._sceneBoundingRect = QRectF()

        # Draw Start Point
        offset = 0.5*QPointF(self._pen.widthF(), self._pen.widthF())
        startRect = QRectF(startPoint - offset, startPoint + offset)
        self.startDot = QGraphicsEllipseItem(startRect)
        self.startDot.setPen(Qt.NoPen)
        self.startDot.setBrush(QBrush(self._pen.color()))
        self.addToGroup(self.startDot)

        # Initialize Memory
        self.controlPoints = np.tile([[startPoint.x()], [startPoint.y()]], 4)
        self.numSegments = 0
        self.subpathList = []

        # Shift modifier
        modifiers = QApplication.queryKeyboardModifiers()
        self.shiftPressed = bool(modifiers & Qt.ShiftModifier)


    def addPoint(self, Q):

        # Make a straight line
        if self.shiftPressed:

            # Initialize line
            if self.currentSubpathItem is None:
                self.currentSubpathItem = QGraphicsLineItem()
                self.currentSubpathItem.setPen(self._pen)
                self.addToGroup(self.currentSubpathItem)
                self.subpathList.append(self.currentSubpathItem)
                self.pointList.append((Q.x(), Q.y()))

            # Ctrl modifier
            modifiers = QApplication.queryKeyboardModifiers()
            ctrlPressed = bool(modifiers & Qt.ControlModifier)

            # Snap to nearest 15 degrees (pi/12 radians)
            if ctrlPressed:
                d = Q - self.P
                dMag = np.sqrt(QPointF.dotProduct(d, d))
                trueAngle = np.arctan2(d.y(), d.x())
                for n in range(-11, 13):
                    if trueAngle <= n*np.pi/12:
                        break
                if (trueAngle - (n-1)*np.pi/12) < (n*np.pi/12 - trueAngle):
                    snapAngle = (n-1)*np.pi/12
                else:
                    snapAngle = n*np.pi/12
                R = dMag * QPointF(np.cos(snapAngle), np.sin(snapAngle)) + self.P
                self.currentSubpathItem.setLine(QLineF(self.P, R))
                self.pointList[1] = R.toTuple()
            # Do not snap
            else:
                self.currentSubpathItem.setLine(QLineF(self.P, Q))
                self.pointList[1] = Q.toTuple()

        # Draw a path that follows the input
        else:
            # If the subpath is too long, start a new subpath
            if self.numSegments % MAX_SEGMENTS_PER_SUBPATH == 0:
                self.subpath = QPainterPath()
                self.subpath.moveTo(QPointF(self.controlPoints[0, 1], self.controlPoints[1, 1]))
                self.currentSubpathItem = QGraphicsPathItem(self.subpath)
                self.currentSubpathItem.setPen(self._pen)
                self.addToGroup(self.currentSubpathItem)
                self.subpathList.append(self.currentSubpathItem)

            # Add new point to list
            npQ = np.array([Q.x(), Q.y()])
            if (self.controlPoints[:, 3] == npQ).all():
                return
            self.pointList.append(Q.toTuple())
            self.controlPoints[:, :-1] = self.controlPoints[:, 1:]
            self.controlPoints[:, 3] = npQ
            self.numSegments += 1

            # Plot points
            if self.numSegments >= 4:
                # Smooth with Catmull Rom Splines if needed
                diff = self.controlPoints[:, 2] - self.controlPoints[:, 1]
                if np.dot(diff, diff) > CATMULL_TRIGGER_DIST_SQ:
                    points = catmullRomSpline(self.controlPoints)
                    for point in points.T:
                        self.subpath.lineTo(QPointF(*point))
                # Just add the penultimate point if no smoothing required
                else:
                    self.subpath.lineTo(QPointF(*self.controlPoints[:, 2]))

            else:
                # Just add the penultimate point if the path is just starting
                self.subpath.lineTo(QPointF(*self.controlPoints[:, 2]))

            # Update path
            self.currentSubpathItem.setPath(self.subpath)

        # Update bounding rect
        self._sceneBoundingRect = self._sceneBoundingRect.united(self.currentSubpathItem.sceneBoundingRect())


    def sceneBoundingRect(self):
        return self._sceneBoundingRect


    def pen(self):
        return self._pen


    def setPen(self, pen):
        self.startDot.setBrush(pen.color())
        for subpathItem in self.subpathList:
            subpathItem.setPen(pen)


    def getData(self):
        data = {}
        data["type"] = "write item"
        data["highlighter"] = self.highlighter
        data["point list"] = self.pointList
        data["shift pressed"] = self.shiftPressed
        data["pen"] = self._pen.getData()
        return data


def loadFromData(data):
    pen = Pen.loadFromData(data["pen"])
    pointList = data["point list"]
    item = WriteItem(pen, QPointF(*pointList[0]), data["highlighter"])
    item.shiftPressed = data["shift pressed"]
    for point in pointList[1:]:
        item.addPoint(QPointF(*point))
    return item
