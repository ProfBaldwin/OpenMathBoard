import numpy as np

from CatmullRomSpline import catmullRomSpline
from LaserTimer import LaserTimer

from PySide6.QtCore import (
        Qt, 
        QRectF, 
        QPointF, 
        QLineF,
        QTimer,
        )

from PySide6.QtGui import (
        QPainterPath,
        QBrush, 
        QPen, 
        )

from PySide6.QtWidgets import (
        QApplication,
        QGraphicsBlurEffect,
        QGraphicsPathItem,
        QGraphicsLineItem,
        QGraphicsEllipseItem,
        QGraphicsItem,
        QGraphicsItemGroup,
        )


LASER_TIMEOUT = 750
MAX_SEGMENTS_PER_SUBPATH = 100
CATMULL_TRIGGER_DIST_SQ = 10.0


class LaserWriteItem(QGraphicsItemGroup):

    undoable = False

    def __init__(self, pen, startPoint):
        super().__init__()

        # Pen
        self._pen = pen

        # Start Point
        self.P = startPoint

        # Set Z level so laser is always on top
        self.setZValue(1000)

        # Blur effect
        blurEffect = QGraphicsBlurEffect()
        blurEffect.setBlurRadius(2.5)
        self.setGraphicsEffect(blurEffect)

        # Initialize Item Memory and the Bounding Rect
        self.currentSubpathItem = None

        # Initialize Memory
        self.controlPoints = np.tile([[startPoint.x()], [startPoint.y()]], 4)
        self.numSegments = 0
        self.itemList = []
        self.timerList = []

        # Draw Start Point
        offset = 0.5*QPointF(self._pen.widthF(), self._pen.widthF())
        startRect = QRectF(startPoint - offset, startPoint + offset)
        self.startDot = QGraphicsEllipseItem(startRect)
        self.startDot.setPen(Qt.NoPen)
        self.startDot.setBrush(QBrush(self._pen.color()))
        self.addToGroup(self.startDot)
        self.itemList.append(self.startDot)
        self.timerList.append(LaserTimer(LASER_TIMEOUT, self.startDot.hide))


    def addPoint(self, Q):

        # Initialize a new subpath
        self.subpath = QPainterPath()
        self.subpath.moveTo(QPointF(self.controlPoints[0, 1], self.controlPoints[1, 1]))

        # Add new point to list
        npQ = np.array([Q.x(), Q.y()])
        if (self.controlPoints[:, 3] == npQ).all():
            return
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
                    self.subpath.lineTo(QPointF(point[0], point[1]))
            # Just add the penultimate point if no smoothing required
            else:
                self.subpath.lineTo(QPointF(self.controlPoints[0, 2],
                    self.controlPoints[1, 2]))

        else:
            # Just add the penultimate point if the path is just starting
            self.subpath.lineTo(QPointF(self.controlPoints[0, 2],
                self.controlPoints[1, 2]))

        # Add subpath to scene
        self.currentSubpathItem = QGraphicsPathItem(self.subpath)
        self.currentSubpathItem.setPen(self._pen)
        self.addToGroup(self.currentSubpathItem)
        self.itemList.append(self.currentSubpathItem)
        self.timerList.append(LaserTimer(LASER_TIMEOUT, self.currentSubpathItem.hide))


    def sceneBoundingRect(self):
        return QRectF()


    def pen(self):
        return self._pen


    def setPen(self, pen):
        self.startDot.setBrush(pen.color())
        for item in self.itemList:
            item.setPen(pen)


    def getData(self):
        return None
