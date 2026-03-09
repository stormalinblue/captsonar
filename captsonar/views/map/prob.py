import numpy as np
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import (
    QWidget,
)

from captsonar.models.tracker import TrackerModel


class ProbWidget(QWidget):
    def __init__(self, tracker: TrackerModel, parent: None | QWidget = None):
        super().__init__(parent=parent)
        self.tracker = tracker

        self.tracker.prob_changed.connect(self.on_prob_changed)
        self.probs = self.tracker.latest_probs()
        self.setAttribute(Qt.WA_TranslucentBackground)

    def on_prob_changed(self, new_probs):
        self.probs = new_probs
        self.update()

    def paintEvent(self, a0):
        if self.probs is None:
            return

        max_prob = np.max(self.probs)

        if max_prob == 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        # Example: draw a red rectangle

        rad = self.width() // 15

        for x, y in np.ndindex(self.probs.shape):
            # rect = QRectF(x * rad, self.height() - (y + 1) * rad, rad, rad)
            painter.setBrush(
                QColor(255, 0, 0, int((self.probs[x, y] / max_prob) * 200))
            )
            painter.drawRect(x * rad, self.height() - (y + 1) * rad, rad, rad)
            # painter.drawText(rect, Qt.AlignCenter, f"{self.probs[x, y]:.3f}")
