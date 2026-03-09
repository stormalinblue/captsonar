from PyQt5.QtCore import QObject, pyqtSignal

from captsonar.core.tracker import Tracker
from captsonar.core.update import (
    BombUpdate,
    Direction,
    DroneUpdate,
    Move,
    SilenceUpdate,
    SonarUpdate,
    SurfaceUpdate,
)


class TrackerModel(QObject):
    prob_changed: pyqtSignal = pyqtSignal(object)

    def __init__(self, grid):
        super().__init__()
        self.log: list[Direction] = []
        self.grid = grid
        self.probs = Tracker(grid).cell_probs()

    def latest_probs(self):
        return self.probs

    def on_log_changed(self, new_history: list[Move]):
        tracker = Tracker(self.grid)
        for update in new_history:
            match update:
                case Direction():
                    tracker.update_with_dir(update)
                case SilenceUpdate():
                    tracker.update_with_silence()
                case DroneUpdate():
                    tracker.update_with_drone(update)
                case SonarUpdate():
                    tracker.update_with_sonar(update)
                case BombUpdate():
                    tracker.update_with_bomb(update)
                case SurfaceUpdate():
                    tracker.update_with_surface()

        self.probs = tracker.cell_probs()
        self.prob_changed.emit(self.probs)
