import numpy as np
from Pen import Pen

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
        QGraphicsPolygonItem,
        QGraphicsEllipseItem,
        QGraphicsItemGroup,
        )


MIN_WIDTH = 4.0
MAX_WIDTH = 48.0
WIDTH_DIST = 20.0


class EraserWriteItem(QGraphicsItemGroup):

    undoable = True

    def __init__(self, brush, startPoint):
        super().__init__()

        # Pen
        self.brush = brush

        # Point list
        self.pointList = [startPoint.toTuple()]

        # Draw Start Point
        offset = 0.5*QPointF(MIN_WIDTH, MIN_WIDTH)
        startRect = QRectF(startPoint - offset, startPoint + offset)
        self.startDot = QGraphicsEllipseItem(startRect)
        self.startDot.setPen(Qt.NoPen)
        self.startDot.setBrush(self.brush)
        self.addToGroup(self.startDot)

        # Initialize memory
        self.prevPrevWidth = MIN_WIDTH
        self.prevWidth = MIN_WIDTH
        self.prevPoint = startPoint
        self.strokeList = []


    def addPoint(self, newPoint):

        self.pointList.append(newPoint.toTuple())

        # Draw
        dist = QLineF(self.prevPoint, newPoint).length()
        newWidth = (MAX_WIDTH-MIN_WIDTH)/WIDTH_DIST * dist + MIN_WIDTH
        newWidth = (newWidth + self.prevWidth + self.prevPrevWidth)/3.0
        newWidth = np.clip(newWidth, MIN_WIDTH, MAX_WIDTH)
        self.drawStroke(self.prevPoint, newPoint, self.prevWidth, newWidth)

        # Save data
        self.prevPrevWidth = self.prevWidth
        self.prevWidth = newWidth
        self.prevPoint = newPoint


    def drawStroke(
            self,
            p1: QPointF,
            p2: QPointF,
            width1: float,
            width2: float):

        stroke = QGraphicsPolygonItem(self.lineToPolygon(p1, p2, width1, width2))
        stroke.setPen(Qt.NoPen)
        stroke.setBrush(self.brush)
        self.addToGroup(stroke)
        self.strokeList.append(stroke)


    def lineToPolygon(
            self, 
            p1: QPointF, 
            p2: QPointF, 
            width1: float, 
            width2: float):

        # Get unit vector perpendicular to the line through p1, p2
        line_vec = p2 - p1
        norm = np.sqrt( QPointF.dotProduct(line_vec, line_vec) )
        perp_vec = QPointF(-line_vec.y(), line_vec.x()) / norm

        # Find vertices of polygon
        p1a = p1 + 0.5*width1*perp_vec
        p1b = p1 - 0.5*width1*perp_vec
        
        p2a = p2 + 0.5*width2*perp_vec
        p2b = p2 - 0.5*width2*perp_vec

        # Find angle of perpendicular vector
        theta = QLineF(p1a, p1b).angle()

        # Construct path
        painterPath = QPainterPath()
        painterPath.moveTo(p1a)
        painterPath.arcTo(p1.x() + 0.5*width1, p1.y() + 0.5*width1, -width1, -width1, theta, -180.0)
        painterPath.lineTo(p2b)
        painterPath.arcTo(p2.x() - 0.5*width2, p2.y() - 0.5*width2, width2, width2, theta, -180.0)
        painterPath.lineTo(p1a)
        painterPath.closeSubpath()

        return painterPath.toFillPolygon()


    def setBrush(self, brush):
        self.startDot.setBrush(brush)
        for stroke in self.strokeList:
            stroke.setBrush(brush)


    def sceneBoundingRect(self):
        return QRectF()


    def getData(self):
        data = {}
        data["type"] = "eraser write item"
        data["point list"] = self.pointList
        return data


def loadFromData(data, backgroundBrush):
    pointList = data["point list"]
    item = EraserWriteItem(backgroundBrush, QPointF(*pointList[0]))
    for point in pointList[1:]:
        item.addPoint(QPointF(*point))
    return item
