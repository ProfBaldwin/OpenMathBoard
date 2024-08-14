from ItemUndoCommand import ItemUndoCommand

from PySide6.QtCore import (
        QPointF,
        QRectF,
        )

from PySide6.QtGui import (
        QUndoStack,
        )

from PySide6.QtWidgets import (
        QGraphicsScene,
        )


class GraphicsScene(QGraphicsScene):

    def __init__(self, viewSize, parent = None):
        super().__init__(parent)

        self.viewSize = viewSize
        self._itemsBoundingRect = QRectF()

        self.itemList = []

        self.undoStack = QUndoStack()

        self.centerPt = QPointF(0, 0)


    def itemFinished(self, item, pastedItem = False):
        # Update items bounding rect
        self._itemsBoundingRect = self._itemsBoundingRect.united(item.sceneBoundingRect())

        # Update scene rect
        newSceneRect = self.sceneRect().united(
                self._itemsBoundingRect.adjusted(0, 0, self.viewSize.width(), self.viewSize.height()))
        self.setSceneRect(newSceneRect)

        # Add to item list
        self.itemList.append(item)

        # Add to undo stack
        if not pastedItem and item.undoable:
            self.undoStack.push(ItemUndoCommand(item))


    def itemsBoundingRect(self):
        return self._itemsBoundingRect


    def updateViewSize(self, viewSize):
        self.viewSize = viewSize
        
        # Update sceneRect
        viewRect = QRectF(QPointF(0, 0), viewSize)
        minSceneRect = self.itemsBoundingRect().adjusted(0, 0, viewSize.width(), viewSize.height())
        newSceneRect = viewRect.united(minSceneRect)
        self.setSceneRect(newSceneRect)

