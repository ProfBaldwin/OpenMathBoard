from ColorButton import ColorButton
from LaserWriteItem import LaserWriteItem
from LineWidthComboBox import LineWidthComboBox
from Pen import Pen

from PySide6.QtCore import (
        Qt,
        )

from PySide6.QtGui import (
        QColor,
        )

from PySide6.QtWidgets import (
        QButtonGroup,
        QHBoxLayout,
        QLabel,
        QToolBar,
        QWidget,
        )


class LaserToolBar(QToolBar):

    numColorButtons = 4

    def __init__(self):
        super().__init__()

        self.setFloatable(False)
        self.setMovable(False)

        # Initialize Item List
        self.itemList = []

        # Color Buttons
        self.colorButtonList = (
                ColorButton("#F70000", "#EBA700", "Color (1)", self), 
                ColorButton("#6E6EFF", "#00C7C7", "Color (2)", self), 
                ColorButton("#CA21FF", "#E594FC", "Color (3)", self), 
                ColorButton("#00942E", "#14CF00", "Color (4)", self), 
                )
        self.colorButtonGroup = QButtonGroup(self)
        for i, button in enumerate(self.colorButtonList):
            self.addWidget(button)
            self.colorButtonGroup.addButton(button, i)
        self.colorButtonList[0].setChecked(True)

        self.addSeparator()

        # Line Width
        lineWidthWidget = QWidget(self)
        lineWidthLayout = QHBoxLayout(lineWidthWidget)
        lineWidthLayout.setContentsMargins(5, 0, 5, 0)
        lineWidthLayout.addWidget(QLabel("Line Width:", self))
        self.lineWidthComboBox = LineWidthComboBox(self)
        lineWidthLayout.addWidget(self.lineWidthComboBox)
        self.lineWidthComboBox.setCurrentIndex(2)
        self.addWidget(lineWidthWidget)


    def getItem(self, startPoint):

        # Clean out dead lasers
        i = 0
        for i, item in enumerate(self.itemList):
            if item.timerList[-1].isActive():
                break

        for item in self.itemList[:i]:
            item.scene().removeItem(item)
        del self.itemList[:i]

        # Get the pen
        currentColor = self.colorButtonGroup.checkedButton().currentColor
        invertedColor = self.colorButtonGroup.checkedButton().invertedColor
        widthF = self.lineWidthComboBox.getWidth()
        pen = Pen(currentColor, invertedColor, widthF)

        # Create the laser item
        newItem = LaserWriteItem(pen, startPoint)
        self.itemList.append(newItem)

        return newItem


    def invertColors(self):

        for button in self.colorButtonList:
            button.invertColor()


    def resetMode(self):
        pass
