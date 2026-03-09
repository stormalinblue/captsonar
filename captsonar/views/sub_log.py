from PyQt5.QtWidgets import QListWidget, QVBoxLayout, QWidget

from captsonar.core.update import Move
from captsonar.models.history import HistoryModel


class SubLogWidget(QWidget):
    def __init__(self, sub_log: HistoryModel):
        super().__init__()

        self.sub_log = sub_log

        self.sub_log.log_changed.connect(self.on_log_changed)

        self.scroll_list = QListWidget()

        self.scroll_list.addItems([str(d) for d in self.sub_log.latest_log()])

        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll_list)

        self.setLayout(layout)

    def on_log_changed(self, new_history: list[Move]):
        self.scroll_list.clear()
        self.scroll_list.addItems([str(d) for d in new_history])

        self.update()
