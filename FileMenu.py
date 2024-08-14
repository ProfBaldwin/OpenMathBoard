from PySide6.QtGui import (
        QKeySequence,
        )

from PySide6.QtWidgets import (
        QMenu,
        )


class FileMenu(QMenu):

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setTitle("File")

        self.newAction = self.addAction("New", "Ctrl+N")
        self.openAction = self.addAction("Open...", "Ctrl+O")

        self.addSeparator()

        self.saveAction = self.addAction("Save", "Ctrl+S")
        self.saveAsAction = self.addAction("Save As...", "Ctrl+Shift+S")
        self.exportAction = self.addAction("Export to PDF")

        self.addSeparator()

        self.quitAction = self.addAction("Quit", "Ctrl+Q")
