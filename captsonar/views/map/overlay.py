import typing

from PyQt5.QtCore import QLineF, Qt
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import (
    QWidget,
)
from PyQt5.sip import array


class OverlayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        rad = w / 15
        dashed_pen = QPen(QColor(255, 255, 255))
        dashed_pen.setStyle(Qt.DashLine)
        painter.setPen(dashed_pen)

        painter.drawLines(
            typing.cast(
                array,
                [
                    QLineF(rad * index, 0, rad * index, h)
                    for index in range(1, 15)
                    if index % 5 != 0
                ],
            )
        )

        painter.drawLines(
            typing.cast(
                array,
                [
                    QLineF(0, rad * index, w, rad * index)
                    for index in range(1, 15)
                    if index % 5 != 0
                ],
            )
        )

        pen = QPen(QColor(255, 255, 255), 4)
        painter.setPen(pen)
        painter.drawLines(
            typing.cast(
                array,
                [QLineF(rad * index, 0, rad * index, h) for index in range(5, 15, 5)],
            )
        )

        painter.drawLines(
            typing.cast(
                array,
                [QLineF(0, rad * index, w, rad * index) for index in range(5, 15, 5)],
            )
        )
