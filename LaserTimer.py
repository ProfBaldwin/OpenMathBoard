from PySide6.QtCore import (
        Qt,
        QTimer,
        )


class LaserTimer(QTimer):

    def __init__(self, msec, slot):
        super().__init__()

        self.setTimerType(Qt.PreciseTimer)
        self.setSingleShot(True)
        self.timeout.connect(slot)
        self.start(msec)
