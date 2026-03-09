import functools

from PyQt5.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from captsonar.core.update import Direction, Move, SilenceUpdate, SurfaceUpdate
from captsonar.models.history import HistoryModel

from .bomb import BombRecorder
from .drone import DroneRecorder
from .sonar import SonarRecorder


class SignalRecorder(QWidget):
    sub_log: HistoryModel

    def __init__(self, sub_log: HistoryModel):
        super().__init__()

        self.sub_log = sub_log

        layout = QVBoxLayout()

        for dir_enum in Direction:
            button = QPushButton(dir_enum.value)
            button.clicked.connect(
                functools.partial(lambda x: self.on_update(x), dir_enum)
            )
            layout.addWidget(button)

        self.silence_button = QPushButton("Silence")
        self.silence_button.clicked.connect(lambda: self.on_surface(SilenceUpdate()))
        layout.addWidget(self.silence_button)

        self.surface_button = QPushButton("Surface")
        self.surface_button.clicked.connect(lambda: self.on_surface(SurfaceUpdate()))
        layout.addWidget(self.surface_button)

        self.drone_recorder = DroneRecorder()
        self.drone_recorder.submitted.connect(self.on_update)
        layout.addWidget(self.drone_recorder)

        self.sonar_recorder = SonarRecorder()
        self.sonar_recorder.submitted.connect(self.on_update)
        layout.addWidget(self.sonar_recorder)

        self.bomb_recorder = BombRecorder()
        self.bomb_recorder.submitted.connect(self.on_update)
        layout.addWidget(self.bomb_recorder)

        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.on_erase_last_direction)
        layout.addWidget(self.undo_button)

        self.setLayout(layout)

    def on_erase_last_direction(self):
        self.sub_log.pop()

    def on_update(self, update: Move):
        self.sub_log.add_update(update)
