from PySide6.QtCore import (
        Qt,
        QPointF,
        QSize,
        )

from PySide6.QtGui import (
        QBrush,
        QColor,
        QIcon,
        QPainter,
        QPen,
        QPixmap,
        )

from PySide6.QtWidgets import (
        QColorDialog,
        QToolButton,
        )


class ColorButton(QToolButton):

    def __init__(self, lightModeColor, darkModeColor, text = None, parent = None):
        super().__init__(parent)

        if text is not None:
            self.setText(text)
            self.setToolTip(text)

        self.currentColor = QColor(lightModeColor)
        self.invertedColor = QColor(darkModeColor)

        self.setCheckable(True)
        self.setIconSize(QSize(20, 20))
        self.updateIcon()



    #def mouseDoubleClickEvent(self, event):
    #    colorDialog = QColorDialog(self)
    #    colorDialog.setCurrentColor(self.color)
    #    colorDialog.colorSelected.connect(self.setColor)
    #    colorDialog.open()


    def updateIcon(self):

        # Create the Icon
        iconPixmap = QPixmap(20, 20)
        iconPixmap.fill(QColor(0, 0, 0, 0))

        painter = QPainter(iconPixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen()
        pen.setColor(QColor(0, 0, 0))
        pen.setWidthF(1.5)
        painter.setPen(pen)

        brush = QBrush()
        brush.setColor(self.currentColor)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        painter.drawEllipse(QPointF(10, 10), 9.0, 9.0)

        painter.end()

        icon = QIcon()
        icon.addPixmap(iconPixmap)
        self.setIcon(icon)


    def invertColor(self):
        self.currentColor, self.invertedColor = self.invertedColor, self.currentColor
        self.updateIcon()




