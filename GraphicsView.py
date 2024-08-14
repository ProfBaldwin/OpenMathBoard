import json

from AltStyleComboBox import STYLES
from EllipseItem import EllipseItem
from GraphicsScene import GraphicsScene
from Pen import Pen
from PixmapItem import PixmapItem
from RectItem import RectItem
from WriteItem import WriteItem

from PySide6.QtCore import (
        Qt,
        QEvent,
        QMarginsF,
        QPointF,
        QRectF,
        QSize,
        )

from PySide6.QtGui import (
        QBrush,
        QColor,
        QPageSize,
        QPainter,
        QPdfWriter,
        QPixmap,
        )

from PySide6.QtWidgets import (
        QFrame,
        QGraphicsItem,
        QGraphicsView,
        )


PRESSURE_DEADZONE = 0.05
PDF_DPI = 200

LIGHT_BG = "#F5F5F5"
LIGHT_FG = "#393939"
DARK_BG = "#1A1A1A"
DARK_FG = "#393939"

SCROLL_SPEED = 0.2

class GraphicsView(QGraphicsView):

    def __init__(self, parent):
        super().__init__(parent)

        self.setFrameStyle(QFrame.NoFrame)

        self.setRenderHint(QPainter.Antialiasing)
        self.centerOn(0, 0)

        self.sceneList = []
        self._currentSceneIndex = -1
        self.brush = QBrush()
        self.addScene()

        self.setCursor(Qt.CrossCursor)

        self.item = None
        self.selectedItem = PixmapItem()

        self.copySelectionInProgress = False

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # Set style sheet for scrollbars
        self.styleSheetStr = (
                "QScrollBar:vertical {{"              
                "    background: {bgcolor};"
                "    width: 2px;    "
                "}}"
                "QScrollBar::handle:vertical {{"
                "    background: {fgcolor};"
                "    min-height: 2px;"
                "}}"
                "QScrollBar::add-page:vertical {{"
                "    background: {bgcolor};"
                "}}"
                "QScrollBar::sub-page:vertical {{"
                "    background: {bgcolor};"
                "}}"
                "QScrollBar::add-line:vertical{{"
                "    height: 0px;"
                "}}"
                "QScrollBar::sub-line:vertical {{"
                "    height: 0px;"
                "}}"
                
                "QScrollBar:horizontal {{"
                "    background: {bgcolor};"
                "    height: 2px;"
                "}}"
                "QScrollBar::handle:horizontal {{"
                "    background: {fgcolor};"
                "    min-width: 2px;"
                "}}"
                "QScrollBar::add-page:horizontal {{"
                "    background: {bgcolor};"
                "}}"
                "QScrollBar::sub-page:horizontal {{"
                "    background: {bgcolor};"
                "}}"
                "QScrollBar::add-line:horizontal {{"
                "    width: 0px;"
                "}}"
                "QScrollBar::sub-line:horizontal {{"
                "    width: 0px;"
                "}}"
                
                "QAbstractScrollArea::corner {{"
                "    background: {bgcolor};"
                "}}"
                )

        self.currentColors = (LIGHT_BG, LIGHT_FG)
        self.invertedColors = (DARK_BG, DARK_FG)
        self.setStyleSheet(self.styleSheetStr.format(bgcolor = self.currentColors[0], 
                                                     fgcolor = self.currentColors[1]))
        if self.parentWidget().menuBar().backgroundMenu.getMode() == "Dark":
            self.invertColors()


    # Tablet event for drawing
    def tabletEvent(self, event):

        event.accept()

        # Map the event position to scene, adjusting for the ribbon if necessary
        pos = self.mapToScene(0, 0) + event.position()

        # If pressure is too low, don't draw and finish up and current drawing
        if (event.pressure() < PRESSURE_DEADZONE or self.selectedItem.isSelected()) and self.item is not None:
            self.item.addPoint(pos)
            self.scene().itemFinished(self.item)
            self.item.update()
            self.item = None
            self.parentWidget().secondaryToolBar.resetMode()
        else:
            if event.type() == QEvent.TabletMove:
                # Create a new graphics item based on currently selected tool
                if self.item is None:
                    self.item = self.parentWidget().secondaryToolBar.getItem(pos)
                    self.scene().addItem(self.item)
                    self.selectedItem.setSelected(False)
                    if self.parentWidget().secondaryToolBar != self.parentWidget().laserToolBar:
                        self.parentWidget().setWindowModified(True)
                # Add new point to item if drawing in progress
                else:
                    self.item.addPoint(pos)
                    self.item.update()


    # Mouse events for selection
    def mousePressEvent(self, event):

        if self.selectedItem.flags() & QGraphicsItem.ItemIsMovable:
            super().mousePressEvent(event)
            return

        pos = self.mapToScene(0, 0) + event.position()
        self.selectedItem = RectItem(Qt.NoPen, Qt.NoBrush, pos,
                                     editMenu = self.parentWidget().menuBar().editMenu)
        self.selectedItem.setFlag(QGraphicsItem.ItemIsSelectable)
        self.selectedItem.setSelected(True)
        self.scene().addItem(self.selectedItem)
        self.copySelectionInProgress = True


    def mouseMoveEvent(self, event):

        if self.selectedItem.flags() & QGraphicsItem.ItemIsMovable:
            super().mouseMoveEvent(event)
            return

        if self.copySelectionInProgress:
            pos = self.mapToScene(0, 0) + event.position()
            self.selectedItem.addPoint(pos)
            self.selectedItem.update()


    def mouseReleaseEvent(self, event):

        if self.selectedItem.flags() & QGraphicsItem.ItemIsMovable:
            super().mouseReleaseEvent(event)
            return

        if self.copySelectionInProgress:

            pos = self.mapToScene(0, 0) + event.position()
            self.selectedItem.addPoint(pos)
            self.selectedItem.update()

            self.selectedItem.setFlag(QGraphicsItem.ItemIsMovable)
            self.selectedItem.setCursor(Qt.SizeAllCursor)
            self.parentWidget().menuBar().editMenu.cutAction.setEnabled(True)
            self.parentWidget().menuBar().editMenu.copyAction.setEnabled(True)
            self.copySelectionInProgress = False


    def cut(self):
        self.copy()

        rect = self.selectedItem.rect().adjusted(1, 1, -1, -1)
        rectItem = self.parentWidget().eraserToolBar.eraseRect(rect, getModifiers = False)
        self.scene().addItem(rectItem)
        self.scene().itemFinished(rectItem)
        self.selectedItem.setSelected(False)

        self.parentWidget().setWindowModified(True)


    def copy(self):
        rect = self.selectedItem.rect().adjusted(1, 1, -1, -1)
        pixmap = QPixmap(rect.width(), rect.height())

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        self.scene().render(painter, QRectF(0, 0, rect.width(), rect.height()), rect)
        painter.end()

        self.parentWidget().clipboard.setPixmap(pixmap)


    def paste(self, inverted = False):

        # Deselect any currently selected item
        self.selectedItem.setSelected(False)

        # Grab and prepare the image from clipboard
        image = self.parentWidget().clipboard.image()
        if image.width() > self.width() - 50:
            image = image.scaledToWidth(self.width() - 50, mode = Qt.SmoothTransformation)
        if image.height() > self.height() - 50:
            image = image.scaledToHeight(self.height() - 50, mode = Qt.SmoothTransformation)
        if inverted:
            image.invertPixels()

        # Create a place the pasted image
        self.selectedItem = PixmapItem(image, self.scene())
        offsetPos = self.mapToScene(
                *(0.5 * (self.size() - self.selectedItem.pixmap().size())).toTuple()
                )
        self.selectedItem.setOffset(offsetPos)

        self.parentWidget().setWindowModified(True)


    def resizeEvent(self, event):
        self.scene().updateViewSize(self.size())


    def addScene(self):
        if self.scene() is not None:
            self.scene().centerPt = QRectF(self.mapToScene(0, 0), self.size()).center()
        self._currentSceneIndex += 1
        self.sceneList.append(GraphicsScene(self.size(), self))
        self.setScene(self.sceneList[-1])
        self.scene().setBackgroundBrush(self.brush)
        self.scene().updateViewSize(self.size())

        self.parentWidget().setWindowModified(True)


    def prevScene(self):
        self.scene().centerPt = QRectF(self.mapToScene(0, 0), self.size()).center()
        self._currentSceneIndex -= 1
        self.setScene(self.sceneList[self._currentSceneIndex])
        self.scene().updateViewSize(self.size())
        self.centerOn(self.scene().centerPt)


    def nextScene(self):
        self.scene().centerPt = QRectF(self.mapToScene(0, 0), self.size()).center()
        self._currentSceneIndex += 1
        self.setScene(self.sceneList[self._currentSceneIndex])
        self.scene().updateViewSize(self.size())
        self.centerOn(self.scene().centerPt)


    def setSceneIndex(self, index):
        self.scene().centerPt = QRectF(self.mapToScene(0, 0), self.size()).center()
        self._currentSceneIndex = index
        self.setScene(self.sceneList[self._currentSceneIndex])
        self.scene().updateViewSize(self.size())
        self.centerOn(self.scene().centerPt)

    
    def sceneCount(self):
        return len(self.sceneList)


    def currentSceneIndex(self):
        return self._currentSceneIndex


    def setBackground(self, brush):
        self.brush = brush
        for scene in self.sceneList:
            scene.setBackgroundBrush(brush)


    def save(self, fileName):

        # Collect save data
        data = {}
        data["mode"] = self.parentWidget().menuBar().backgroundMenu.getMode()
        data["scene data list"] = []
        for scene in self.sceneList:
            sceneData = []
            for item in scene.itemList:
                if item.isVisible():
                    itemData = item.getData()
                    if itemData is not None:
                        sceneData.append(itemData)
            data["scene data list"].append(sceneData)

        # Save to json
        with open(fileName, "w") as f:
            json.dump(data, f)


    def export(self, filename):
        pdfDoc = QPdfWriter(filename)
        pdfDoc.setResolution(PDF_DPI)
        pdfDoc.setPageMargins(QMarginsF(0, 0, 0, 0))
        
        for i, scene in enumerate(self.sceneList):
            sceneCopyRect = scene.itemsBoundingRect().adjusted(-50, -50, 50, 50)
            pagePasteRect = QRectF(QPointF(0, 0), sceneCopyRect.size())
            pageSize = QPageSize(1/PDF_DPI * pagePasteRect.size(), QPageSize.Inch, matchPolicy = QPageSize.ExactMatch)
            pdfDoc.setPageSize(pageSize)
            if i == 0:
                painter = QPainter(pdfDoc)
                painter.setRenderHint(QPainter.Antialiasing)
            else:
                pdfDoc.newPage()
            scene.render(painter, pagePasteRect, sceneCopyRect)
        painter.end()

    
    def stepUp(self):
        stepSize = SCROLL_SPEED*self.size().height()
        self.verticalScrollBar().setValue(self.verticalScrollBar().value() - stepSize)


    def stepDown(self):
        stepSize = SCROLL_SPEED*self.size().height()
        self.verticalScrollBar().setValue(self.verticalScrollBar().value() + stepSize)


    def stepLeft(self):
        stepSize = SCROLL_SPEED*self.size().width()
        self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - stepSize)


    def stepRight(self):
        stepSize = SCROLL_SPEED*self.size().width()
        self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + stepSize)


    def invertColors(self):
        self.currentColors, self.invertedColors = self.invertedColors, self.currentColors
        self.setStyleSheet(self.styleSheetStr.format(bgcolor = self.currentColors[0], 
                                                     fgcolor = self.currentColors[1]))


