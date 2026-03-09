import sys

import numpy as np
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QWidget,
)

from captsonar.models.history import HistoryModel
from captsonar.models.tracker import TrackerModel
from captsonar.views.map import MapWidget
from captsonar.views.signal_recorder import SignalRecorder
from captsonar.views.sub_log import SubLogWidget

from .grid_gen import get_generator, get_grid


class MainWindow(QWidget):
    def __init__(self, gen):
        super().__init__()

        p = self.palette()
        p.setColor(QPalette.Window, QColor("#012f54"))
        self.setAutoFillBackground(True)
        self.setPalette(p)

        self.setWindowTitle("Captain Sonar Tracker")

        layout = QHBoxLayout()

        self.gen = gen
        sub_log = HistoryModel()

        self.signal_recorder = SignalRecorder(sub_log)
        self.sub_log_widget = SubLogWidget(sub_log)

        layout.addWidget(self.signal_recorder)
        layout.addWidget(self.sub_log_widget)

        grid = get_grid(self.gen)
        tracker = TrackerModel(grid)
        sub_log.log_changed.connect(tracker.on_log_changed)
        self.geo_widget = MapWidget(grid, tracker)
        layout.addWidget(self.geo_widget)

        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    gen = get_generator()
    window = MainWindow(gen)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
