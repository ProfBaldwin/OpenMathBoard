from EllipseItem import EllipseItem
from EraserWriteItem import EraserWriteItem
from RectItem import RectItem
from ToolButton import ToolButton

from PySide6.QtCore import (
        Qt,
        )

from PySide6.QtWidgets import (
        QButtonGroup,
        QToolBar,
        )


class EraserToolBar(QToolBar):

    numColorButtons = 0

    def __init__(self):
        super().__init__()

        self.setFloatable(False)
        self.setMovable(False)

        # Initialize item list
        self.itemList = []

        # Mode
        self.writeModeButton = ToolButton("Write Mode (W)", self, "./Resources/writeModeIcon.svg")
        self.ellipseModeButton = ToolButton("Eraser Mode (E)", self, "./Resources/ellipseEraseModeIcon.svg")
        self.rectModeButton = ToolButton("Rectangle Mode (R)", self, "./Resources/rectEraseModeIcon.svg")

        self.addWidget(self.writeModeButton)
        self.addWidget(self.ellipseModeButton)
        self.addWidget(self.rectModeButton)

        self.modeButtonGroup = QButtonGroup()
        self.modeButtonGroup.addButton(self.writeModeButton)
        self.modeButtonGroup.addButton(self.ellipseModeButton)
        self.modeButtonGroup.addButton(self.rectModeButton)

        self.writeModeButton.setChecked(True)


    def getItem(self, startPoint):
        match self.modeButtonGroup.checkedButton():
            case self.writeModeButton:
                item = EraserWriteItem(self.backgroundBrush, startPoint)
            case self.ellipseModeButton:
                item = EllipseItem(Qt.NoPen, self.backgroundBrush, startPoint, eraser = True)
            case self.rectModeButton:
                item = RectItem(Qt.NoPen, self.backgroundBrush, startPoint, eraser = True)
        self.itemList.append(item)
        return item


    def eraseRect(self, rectF, getModifiers = True):
        rectItem = RectItem(Qt.NoPen, self.backgroundBrush, rectF.topLeft(), eraser = True)
        rectItem.addPoint(rectF.bottomRight(), getModifiers)
        self.itemList.append(rectItem)
        return rectItem


    def updateBackground(self, backgroundBrush):
        self.backgroundBrush = backgroundBrush
        for item in self.itemList:
            item.setBrush(backgroundBrush)
            item.update()


    def resetMode(self):
        self.writeModeButton.setChecked(True)
