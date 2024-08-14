from ColorButton import ColorButton
from EllipseItem import EllipseItem
from LineWidthComboBox import LineWidthComboBox
from Pen import Pen
from RectItem import RectItem
from ToolButton import ToolButton
from WriteItem import WriteItem

from PySide6.QtCore import (
        Qt,
        )

from PySide6.QtGui import (
        QColor,
        )

from PySide6.QtWidgets import (
        QApplication,
        QButtonGroup,
        QHBoxLayout,
        QLabel,
        QToolBar,
        QWidget,
        )


class HighlighterToolBar(QToolBar):

    numColorButtons = 4

    def __init__(self):
        super().__init__()

        self.setFloatable(False)
        self.setMovable(False)

        # Initialize Item List
        self.itemList = []

        # Color Buttons
        self.colorButtonList = (
                ColorButton("#FFC41F", "#B80000", "Color (1)", self), 
                ColorButton("#00E3E3", "#3838FF", "Color (2)", self), 
                ColorButton("#E594FC", "#CA21FF", "Color (3)", self), 
                ColorButton("#14CF00", "#00942E", "Color (4)", self), 
                )
        self.colorButtonGroup = QButtonGroup(self)
        for i, button in enumerate(self.colorButtonList):
            self.addWidget(button)
            self.colorButtonGroup.addButton(button, i)
        self.colorButtonList[0].setChecked(True)

        self.addSeparator()

        # Mode
        self.writeModeButton = ToolButton("Write Mode (W)", self, "./Resources/writeModeIcon.svg")
        self.ellipseModeButton = ToolButton("Ellipse Mode (E)", self, "./Resources/ellipseModeIcon.svg")
        self.rectModeButton = ToolButton("Rectangle Mode (R)", self, "./Resources/rectModeIcon.svg")

        self.addWidget(self.writeModeButton)
        self.addWidget(self.ellipseModeButton)
        self.addWidget(self.rectModeButton)

        self.modeButtonGroup = QButtonGroup()
        self.modeButtonGroup.addButton(self.writeModeButton)
        self.modeButtonGroup.addButton(self.ellipseModeButton)
        self.modeButtonGroup.addButton(self.rectModeButton)

        self.writeModeButton.setChecked(True)

        self.addSeparator()

        # Line Width
        lineWidthWidget = QWidget(self)
        lineWidthLayout = QHBoxLayout(lineWidthWidget)
        lineWidthLayout.setContentsMargins(5, 0, 5, 0)
        lineWidthLayout.addWidget(QLabel("Line Width:", self))
        self.lineWidthComboBox = LineWidthComboBox(self)
        lineWidthLayout.addWidget(self.lineWidthComboBox)
        self.lineWidthComboBox.setCurrentIndex(4)
        self.addWidget(lineWidthWidget)


    def getItem(self, startPoint):

        # Modifiers
        modifiers = QApplication.queryKeyboardModifiers()
        altPressed = bool(modifiers & Qt.AltModifier)

        # Get the pen
        currentColor = self.colorButtonGroup.checkedButton().currentColor
        invertedColor = self.colorButtonGroup.checkedButton().invertedColor
        widthF = self.lineWidthComboBox.getWidth()
        pen = Pen(currentColor, invertedColor, 3*widthF)

        match self.modeButtonGroup.checkedButton():
            case self.writeModeButton:
                newItem = WriteItem(pen, startPoint, highlighter = True)
            case self.ellipseModeButton:
                newItem = EllipseItem(pen, Qt.NoBrush, startPoint, highlighter = True)
            case self.rectModeButton:
                newItem = RectItem(pen, Qt.NoBrush, startPoint, highlighter = True)

        self.itemList.append(newItem)
        return newItem


    def invertColors(self):

        for button in self.colorButtonList:
            button.invertColor()

        for item in self.itemList:
            pen = item.pen()
            pen.invertColor()
            item.setPen(pen)


    def resetMode(self):
        self.writeModeButton.setChecked(True)
