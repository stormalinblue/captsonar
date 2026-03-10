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

        self.current_x = None
        self.current_y = None
        self.current_sector = None

        self.x_combo = QComboBox()
        self.x_combo.addItem("None", None)
        for x_value in range(0, 16):
            self.x_combo.addItem(string.ascii_uppercase[x_value], x_value)
        self.x_combo.setCurrentIndex(0)
        self.x_combo.currentIndexChanged.connect(self.on_x_changed)
        layout.addWidget(self.x_combo)

        self.y_combo = QComboBox()
        self.y_combo.addItem("None", None)
        for y_display in range(1, 16):
            self.y_combo.addItem(str(y_display), 15 - y_display)
        self.y_combo.setCurrentIndex(0)
        self.y_combo.currentIndexChanged.connect(self.on_y_changed)
        layout.addWidget(self.y_combo)

        self.sector_combo = QComboBox()
        self.sector_combo.addItem("None", None)
        for sector in range(1, 10):
            self.sector_combo.addItem(str(sector), sector)
        self.sector_combo.setCurrentIndex(0)

        self.sector_combo.currentIndexChanged.connect(self.on_sector_changed)
        layout.addWidget(self.sector_combo)

        self.submit_button = QPushButton("Submit Sonar Update")
        self.submit_button.clicked.connect(self.on_submit_button_clicked)
        self.submit_button.setEnabled(False)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def can_submit(self):
        count_set = 0
        if self.current_x is not None:
            count_set += 1

        if self.current_y is not None:
            count_set += 1

        if self.current_sector is not None:
            count_set += 1

        return count_set == 2

    def on_x_changed(self, index):
        self.current_x = self.x_combo.itemData(index)

        self.submit_button.setEnabled(self.can_submit())

    def on_y_changed(self, index):
        self.current_y = self.y_combo.itemData(index)

        self.submit_button.setEnabled(self.can_submit())

    def on_sector_changed(self, index):
        self.current_sector = self.sector_combo.itemData(index)

        self.submit_button.setEnabled(self.can_submit())

    def on_submit_button_clicked(self):
        return self.submitted.emit(
            SonarUpdate(
                self.x_combo.currentData(),
                self.y_combo.currentData(),
                self.sector_combo.currentData(),
            )
        )
