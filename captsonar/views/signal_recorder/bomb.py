import string

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QWidget,
)

from captsonar.core.update import BombUpdate


class BombRecorder(QWidget):
    submitted: pyqtSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        self.x_combo = QComboBox()
        for x_value in range(0, 16):
            self.x_combo.addItem(string.ascii_uppercase[x_value], x_value)
        self.x_combo.setCurrentIndex(0)
        layout.addWidget(self.x_combo)

        self.y_combo = QComboBox()
        for y_display in range(1, 16):
            self.y_combo.addItem(str(y_display), 15 - y_display)
        self.y_combo.setCurrentIndex(0)
        layout.addWidget(self.y_combo)

        self.damage_combo = QComboBox()
        for damage in range(0, 3):
            self.damage_combo.addItem(str(damage), damage)
        self.damage_combo.setCurrentIndex(0)
        layout.addWidget(self.damage_combo)

        self.submit_button = QPushButton("Submit Bomb Update")
        self.submit_button.clicked.connect(self.on_submit_button_clicked)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def on_submit_button_clicked(self):
        return self.submitted.emit(
            BombUpdate(
                (self.x_combo.currentData(), self.y_combo.currentData()),
                self.damage_combo.currentData(),
            )
        )
