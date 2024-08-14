from BackgroundMenu import BackgroundMenu
from EditMenu import EditMenu
from FileMenu import FileMenu
from HelpMenu import HelpMenu

from PySide6.QtWidgets import (
        QMenuBar,
        )


class MenuBar(QMenuBar):
    
    def __init__(self, parent = None):
        super().__init__(parent)

        #fileMenu = self.addMenu("File")
        self.fileMenu = FileMenu(self)
        self.addMenu(self.fileMenu)

        self.editMenu = EditMenu(self)
        self.addMenu(self.editMenu)

        self.backgroundMenu = BackgroundMenu(self)
        self.addMenu(self.backgroundMenu)

        self.helpMenu = HelpMenu(self)
        self.addMenu(self.helpMenu)
