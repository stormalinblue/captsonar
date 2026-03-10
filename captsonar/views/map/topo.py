import numpy as np
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import (
    QWidget,
)

OCEAN_COLOR = QColor("#92c3e0")
OBSTACLE_COLOR = QColor("#54747e")
BOUNDARY_COLOR = QColor(0, 0, 0)


class TopoWidget(QWidget):
    def __init__(self, grid, parent=None):
        super().__init__(parent=parent)
        self.grid = grid

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)
        painter.translate(0, self.height())
        painter.scale(1, -1)

        w_rad = self.width() / 15
        h_rad = self.height() / 15

        for x, y in np.ndindex(self.grid.shape):
            if self.grid[x, y]:
                painter.setBrush(OBSTACLE_COLOR)
            else:
                painter.setBrush(OCEAN_COLOR)
            painter.drawRect(QRectF(x * w_rad, y * h_rad, w_rad, h_rad))
