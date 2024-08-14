from ItemUndoCommand import ItemUndoCommand
import ast

from PySide6.QtCore import (
        Qt,
        QBuffer,
        QByteArray,
        QIODevice,
        )

from PySide6.QtGui import (
        QPixmap,
        )

from PySide6.QtWidgets import (
        QGraphicsItem,
        QGraphicsPixmapItem,
        )


class PixmapItem(QGraphicsPixmapItem):

    undoable = True

    def __init__(self, image = None, scene = None, fromData = False):
        super().__init__()

        if image is not None:

            self.setPixmap(QPixmap(image))

            if not fromData:
                self.setFlag(QGraphicsItem.ItemIsMovable)
                self.setFlag(QGraphicsItem.ItemIsSelectable)
                self.setCursor(Qt.SizeAllCursor)
                self.setSelected(True)

        if scene is not None:
            self.scene = scene
            scene.addItem(self)
            scene.undoStack.push(ItemUndoCommand(self))


    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedHasChanged and not self.isSelected():

            self.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.setFlag(QGraphicsItem.ItemIsSelectable, False)
            self.unsetCursor()

            self.scene.itemFinished(self, True)

        return value


    def getData(self):
        data = {}
        data["type"] = "pixmap item"
        data["offset"] = self.offset().toTuple()
        data["position"] = self.pos().toTuple()

        byteArray = QByteArray()
        buffer = QBuffer(byteArray)
        buffer.open(QIODevice.WriteOnly)
        self.pixmap().save(buffer, "PNG")
        buffer.close()

        data["byte array"] = repr(byteArray.data())

        return data


def loadFromData(data, scene):

    byteArray = QByteArray(ast.literal_eval(data["byte array"]))
    pixmap = QPixmap()
    pixmap.loadFromData(byteArray)

    item = PixmapItem(pixmap, scene, fromData = True)
    item.setOffset(*data["offset"])
    item.setPos(*data["position"])

    return item
    


