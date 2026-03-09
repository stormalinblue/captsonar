from PyQt5.QtCore import QObject, pyqtSignal

from captsonar.core.update import Move


class HistoryModel(QObject):
    log_changed: pyqtSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.log: list[Move] = []

    def latest_log(self):
        return self.log

    def add_update(self, update: Move):
        self.log.append(update)
        self.log_changed.emit(self.log)

    def pop(self):
        if self.log:
            self.log.pop()
            self.log_changed.emit(self.log)
