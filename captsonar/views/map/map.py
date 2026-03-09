import string
import typing

from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QWidget

from .grid import GridWidget
from .overlay import OverlayWidget
from .prob import ProbWidget


class MapWidget(QWidget):
    def __init__(self, grid, tracker, parent=None):
        super().__init__(parent=parent)

        self.grid = GridWidget(grid)
        self.prob = ProbWidget(tracker)
        self.overlay = OverlayWidget()

        self.setFixedSize(448, 448)

        self.grid.setParent(self)
        self.prob.setParent(self)
        self.overlay.setParent(self)

    def resizeEvent(self, a0: typing.Optional[QtGui.QResizeEvent]) -> None:
        rad = self.width() // 16
        grid_size = self.width() - rad
        grid_rect = QRect(rad, 0, grid_size, grid_size)

        self.grid.setGeometry(grid_rect)
        self.prob.setGeometry(grid_rect)
        self.overlay.setGeometry(grid_rect)
        self.overlay.raise_()

    def paintEvent(self, a0: typing.Optional[QtGui.QPaintEvent]) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        painter.setPen(QPen(QColor(255, 255, 255)))

        rad = self.width() // 16
        grid_size = self.width() - rad

        for index, letter in enumerate(string.ascii_uppercase[:15]):
            painter.drawText(
                QRect(rad * (index + 1), grid_size, rad, rad), Qt.AlignCenter, letter
            )

        for index in range(15):
            painter.drawText(
                QRect(0, rad * index, rad, rad), Qt.AlignCenter, str(index + 1)
            )
