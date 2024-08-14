from PySide6.QtGui import (
        QAction,
        )


class GridSizeAction(QAction):

    def __init__(self, gridSize, parent = None):
        text = "{} pixels".format(gridSize) if gridSize > 0 else "No Grid"
        super().__init__(text, parent)

        self.gridSize = gridSize
        self.setCheckable(True)
