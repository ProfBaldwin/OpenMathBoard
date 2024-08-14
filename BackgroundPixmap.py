from PySide6.QtCore import (
        Qt,
        )

from PySide6.QtGui import (
        QBrush,
        QColor,
        QPainter,
        QPixmap,
        )


LIGHT_BG = "#F5F5F5"
LIGHT_GRID = "#CCCCCC"
DARK_BG = "#1A1A1A"
DARK_GRID = "#393939"


class BackgroundPixmap(QPixmap):

    def __init__(self, mode, gridSize):
        if gridSize == 0:
            gridSize = 8
            grid = False
        else:
            grid = True
        super().__init__(gridSize, gridSize)

        if mode == "Dark":
            self.fill(QColor(DARK_BG))
        else:
            self.fill(QColor(LIGHT_BG))

        if grid:
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            if mode == "Dark":
                painter.setBrush(QBrush(DARK_GRID))
            else:
                painter.setBrush(QBrush(LIGHT_GRID))
            painter.drawRect(gridSize-2, gridSize-2, 2, 2)
            painter.end()

            




