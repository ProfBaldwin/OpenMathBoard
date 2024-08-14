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


STYLES = (Qt.DashLine, Qt.DotLine, Qt.DashDotLine, Qt.DashDotDotLine)


class AltStyleComboBox(QComboBox):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setToolTip("Alternate Line Style")

        self.setIconSize(QSize(70, 16))
        for style in STYLES:
            self.addItem(self._generateIconWithStyle(style), "")


    def _generateIconWithStyle(self, style):
        pix = QPixmap(70, 16)
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.black)
        pen.setWidthF(3.0)
        pen.setCapStyle(Qt.RoundCap)
        pen.setStyle(style)

        painter.setPen(pen)
        painter.drawLine(2, 8, 68, 8)
        painter.end()
        
        styleIcon = QIcon()
        styleIcon.addPixmap(pix)

        return styleIcon


    def getStyle(self):
        return STYLES[self.currentIndex()]

