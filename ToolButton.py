from PySide6.QtGui import (
        QIcon,
        )

from PySide6.QtWidgets import (
        QToolButton,
        )


class ToolButton(QToolButton):

    def __init__(self, text = "", parent = None, iconFileName = None):
        super().__init__(parent)
        self.setText(text)
        self.setToolTip(text)

        if iconFileName is not None:
            icon = QIcon(iconFileName)
            self.setIcon(icon)

        self.setCheckable(True)


