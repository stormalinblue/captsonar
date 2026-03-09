import string

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QWidget,
)

from captsonar.core.update import SonarUpdate


class SonarRecorder(QWidget):
    submitted: pyqtSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        self.x_combo = QComboBox()
        self.x_combo.addItem("None", None)
        for x_value in range(0, 16):
            self.x_combo.addItem(string.ascii_uppercase[x_value], x_value)
        self.x_combo.setCurrentIndex(0)
        layout.addWidget(self.x_combo)

        self.y_combo = QComboBox()
        self.y_combo.addItem("None", None)
        for y_display in range(1, 16):
            self.y_combo.addItem(str(y_display), 15 - y_display)
        self.y_combo.setCurrentIndex(0)
        layout.addWidget(self.y_combo)

        self.sector_combo = QComboBox()
        self.sector_combo.addItem("None", None)
        for sector in range(1, 10):
            self.sector_combo.addItem(str(sector), sector)
        self.sector_combo.setCurrentIndex(0)
        layout.addWidget(self.sector_combo)

        self.submit_button = QPushButton("Submit Sonar Update")
        self.submit_button.clicked.connect(self.on_submit_button_clicked)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def on_submit_button_clicked(self):
        return self.submitted.emit(
            SonarUpdate(
                self.x_combo.currentData(),
                self.y_combo.currentData(),
                self.sector_combo.currentData(),
            )
        )
