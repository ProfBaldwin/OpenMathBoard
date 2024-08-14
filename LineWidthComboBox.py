from PySide6.QtCore import (
        Qt, 
        QSize,
        )

from PySide6.QtGui import (
        QIcon, 
        QPixmap, 
        QPainter, 
        QPen,
        )

from PySide6.QtWidgets import (
        QComboBox,
        )


WIDTHS = (1, 2, 3, 4, 6, 8, 10, 13, 16)


class LineWidthComboBox(QComboBox):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setToolTip("Line Width")

        self.setIconSize(QSize(70, 16))
        for width in WIDTHS:
            self.addItem(self._generateIconWithWidth(width), "")


    def _generateIconWithWidth(self, width):
        pix = QPixmap(70, 16)
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.black)
        pen.setWidthF(width)
        #pen.setCapStyle(Qt.RoundCap)

        painter.setPen(pen)
        painter.drawLine(2, 8, 68, 8)
        painter.end()
        
        styleIcon = QIcon()
        styleIcon.addPixmap(pix)

        return styleIcon


    def getWidth(self):
        return WIDTHS[self.currentIndex()]


    def setToPrevIndex(self):
        if self.currentIndex() > 0:
            self.setCurrentIndex(self.currentIndex() - 1)


    def setToNextIndex(self):
        if self.currentIndex() < self.count() - 1:
            self.setCurrentIndex(self.currentIndex() + 1)
