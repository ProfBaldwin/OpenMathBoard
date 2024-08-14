from PySide6.QtGui import (
        QKeySequence,
        )

from PySide6.QtWidgets import (
        QMenu,
        )


class EditMenu(QMenu):

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setTitle("Edit")

        self.undoAction = self.addAction("Undo", "Ctrl+Z")
        self.redoAction = self.addAction("Redo", "Ctrl+Shift+Z")

        self.addSeparator()

        self.cutAction = self.addAction("Cut Image", "Ctrl+X")
        self.copyAction = self.addAction("Copy Image", "Ctrl+C")
        self.pasteAction = self.addAction("Paste Image", "Ctrl+V")
        self.pasteInvertedAction = self.addAction("Paste Image with Colors Inverted", "Ctrl+Shift+V")

        self.cutAction.setEnabled(False)
        self.copyAction.setEnabled(False)

        self.addSeparator()

        self.clearAction = self.addAction("Clear Board", "Ctrl+Del")
