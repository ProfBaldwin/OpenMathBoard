from AltStyleComboBox import AltStyleComboBox
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
        QPen,
        )

from PySide6.QtWidgets import (
        QApplication,
        QButtonGroup,
        QHBoxLayout,
        QLabel,
        QToolBar,
        QToolButton,
        QWidget,
        )


class PenToolBar(QToolBar):

    numColorButtons = 5

    def __init__(self):
        super().__init__()

        self.setFloatable(False)
        self.setMovable(False)

        # Initialize Item List
        self.itemList = []

        # Color Buttons
        self.colorButtonList = (
                ColorButton("#393939", "#E5E5E5", "Color (1)", self), # Contrast ~ 90
                ColorButton("#3838FF", "#00E3E3", "Color (2)", self), # Contrast ~ 75
                ColorButton("#B80000", "#FFC41F", "Color (3)", self), # Contrast ~ 75
                ColorButton("#00942E", "#14CF00", "Color (4)", self), # Contrast ~ 60
                ColorButton("#CA21FF", "#E594FC", "Color (5)", self), # Contrast ~ 75
                )
        self.colorButtonGroup = QButtonGroup(self)
        for button in self.colorButtonList:
            self.addWidget(button)
            self.colorButtonGroup.addButton(button)
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
        self.lineWidthComboBox.setCurrentIndex(2)
        self.addWidget(lineWidthWidget)

        # Alt Style
        altStyleWidget = QWidget(self)
        altStyleLayout = QHBoxLayout(altStyleWidget)
        altStyleLayout.setContentsMargins(5, 0, 5, 0)
        altStyleLayout.addWidget(QLabel("Alt Style:", self))
        self.altStyleComboBox = AltStyleComboBox(self)
        altStyleLayout.addWidget(self.altStyleComboBox)
        self.addWidget(altStyleWidget)

    
    def getItem(self, startPoint):

        # Modifiers
        modifiers = QApplication.queryKeyboardModifiers()
        altPressed = bool(modifiers & Qt.AltModifier)

        # Get the pen
        currentColor = self.colorButtonGroup.checkedButton().currentColor
        invertedColor = self.colorButtonGroup.checkedButton().invertedColor
        widthF = self.lineWidthComboBox.getWidth()
        pen = Pen(currentColor, invertedColor, widthF)
        if altPressed:
            pen.setStyle(self.altStyleComboBox.getStyle())
            pen.styleIndex = self.altStyleComboBox.currentIndex()

        match self.modeButtonGroup.checkedButton():
            case self.writeModeButton:
                newItem = WriteItem(pen, startPoint)
            case self.ellipseModeButton:
                newItem = EllipseItem(pen, Qt.NoBrush, startPoint)
            case self.rectModeButton:
                newItem = RectItem(pen, Qt.NoBrush, startPoint)

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




        
