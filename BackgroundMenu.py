from GridSizeAction import GridSizeAction

from PySide6.QtCore import (
        Signal,
        )

from PySide6.QtGui import (
        QActionGroup,
        )

from PySide6.QtWidgets import (
        QMenu,
        )


class BackgroundMenu(QMenu):

    modeChanged = Signal()

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setTitle("Background")
 
        # Select whether background is light or dark
        self.lightModeAction = self.addAction("Light")
        self.darkModeAction = self.addAction("Dark")

        self.lightModeAction.setCheckable(True)
        self.darkModeAction.setCheckable(True)

        self.modeActionGroup = QActionGroup(self)
        self.modeActionGroup.addAction(self.lightModeAction)
        self.modeActionGroup.addAction(self.darkModeAction)

        self.lightModeAction.setChecked(True)
        self._prevMode = "Light"
        self.modeActionGroup.triggered.connect(self.checkModeChanged)

        # Style Size Menus
        self.addSection("Grid Size")

        self.gridSizeActionGroup = QActionGroup(self)

        for gridSize in (0, 8, 16, 24, 32, 40, 48):
            gridSizeAction = GridSizeAction(gridSize, self)
            self.addAction(gridSizeAction)
            self.gridSizeActionGroup.addAction(gridSizeAction)
            if gridSize == 24:
                gridSizeAction.setChecked(True)


    def getMode(self):
        return self.modeActionGroup.checkedAction().text()


    def setMode(self, mode):
        if mode == "Light":
            self.lightModeAction.setChecked(True)
        else:
            self.darkModeAction.setChecked(True)


    def getGridSize(self):
        return self.gridSizeActionGroup.checkedAction().gridSize


    def setGridSize(self, gridSize):
        for action in self.gridSizeActionGroup.actions():
            if gridSize == action.gridSize:
                action.setChecked(True)
                return


    def checkModeChanged(self):
        if self._prevMode != self.getMode():
            self._prevMode = self.getMode()
            self.modeChanged.emit()



