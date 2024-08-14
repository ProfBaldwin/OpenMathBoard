from AltStyleComboBox import STYLES

from PySide6.QtCore import (
        Qt,
        )

from PySide6.QtGui import (
        QPen, 
        QColor,
        )


class Pen(QPen):

    def __init__(self, currentColor, invertedColor, widthF):
        super().__init__()

        self.setCapStyle(Qt.RoundCap)
        self.setJoinStyle(Qt.RoundJoin)

        self.setColor(currentColor)
        self.setWidthF(widthF)

        self.currentColor = QColor(currentColor)
        self.invertedColor = QColor(invertedColor)

        self.styleIndex = -1

        
    def invertColor(self):
        self.currentColor, self.invertedColor = self.invertedColor, self.currentColor
        self.setColor(self.currentColor)


    def getData(self):
        data = {}
        data["style index"] = self.styleIndex
        data["width"] = self.widthF()
        data["current color"] = self.currentColor.getRgb()
        data["inverted color"] = self.invertedColor.getRgb()
        return data


def loadFromData(data):

    currentColor = QColor(*data["current color"])
    invertedColor = QColor(*data["inverted color"])
    pen = Pen(currentColor, invertedColor, data["width"])

    if data["style index"] != -1:
        pen.setStyle(STYLES[data["style index"]])

    return pen

