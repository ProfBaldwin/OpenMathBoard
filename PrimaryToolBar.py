from ToolButton import ToolButton

from PySide6.QtCore import (
        Qt,
        )

from PySide6.QtGui import (
        QAction,
        QFont,
        QKeySequence,
        )

from PySide6.QtWidgets import (
        QButtonGroup,
        QHBoxLayout,
        QLabel,
        QSizePolicy,
        QToolBar,
        QWidget,
        )


class PrimaryToolBar(QToolBar):

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setFloatable(False)
        self.setMovable(False)

        # Tools
        self.penButton = ToolButton("Pen (F1)", self, "./Resources/penIcon.svg")
        self.eraserButton = ToolButton("Erase (F2)", self, "./Resources/eraserIcon.svg")
        self.laserButton = ToolButton("Laser (F3)", self, "./Resources/laserIcon.svg")
        self.highlighterButton = ToolButton("Highlighter (F4)", self, "./Resources/highlighterIcon.svg")

        self.toolButtonGroup = QButtonGroup(self)
        self.toolButtonGroup.addButton(self.penButton)
        self.toolButtonGroup.addButton(self.eraserButton)
        self.toolButtonGroup.addButton(self.laserButton)
        self.toolButtonGroup.addButton(self.highlighterButton)

        self.addWidget(self.penButton)
        self.addWidget(self.eraserButton)
        self.addWidget(self.laserButton)
        self.addWidget(self.highlighterButton)

        self.penButton.setChecked(True)

        # Horizontal spacer
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addWidget(spacer)

        # Slide/scene navigation
        sceneNavigationWidget = QWidget(self)
        layout = QHBoxLayout(sceneNavigationWidget)
        layout.setContentsMargins(0, 0, 0, 0)

        prevSceneShortcut = QKeySequence(Qt.CTRL | Qt.SHIFT | Qt.Key_Tab).toString()
        self.prevSceneButton = ToolButton("Previous Board ({})".format(prevSceneShortcut), 
                                          self, "./Resources/prevIcon.svg")
        self.prevSceneButton.setCheckable(False)
        self.prevSceneButton.setDisabled(True)
        layout.addWidget(self.prevSceneButton)

        self.sceneCountLabel = QLabel("1/1", self)
        layout.addWidget(self.sceneCountLabel)

        nextSceneShortcut = QKeySequence(Qt.CTRL | Qt.Key_Tab).toString()
        self.nextSceneButton = ToolButton("Next Board ({})".format(nextSceneShortcut), 
                                          self, "./Resources/nextIcon.svg")
        self.nextSceneButton.setCheckable(False)
        layout.addWidget(self.nextSceneButton)

        self.addWidget(sceneNavigationWidget)


    def updateSceneCountLabel(self, sceneNum, totalScenes):
        self.sceneCountLabel.setText("{}/{}".format(sceneNum, totalScenes))
