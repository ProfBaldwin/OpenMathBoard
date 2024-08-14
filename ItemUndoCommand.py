from PySide6.QtGui import (
        QUndoCommand,
        )


class ItemUndoCommand(QUndoCommand):

    def __init__(self, item):
        super().__init__()
        self.item = item

    def undo(self):
        self.item.hide()

    def redo(self):
        self.item.show()
