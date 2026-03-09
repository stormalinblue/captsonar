from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QWidget,
)

from captsonar.core.update import DroneUpdate


class DroneRecorder(QWidget):
    submitted: pyqtSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        self.sector_combo = QComboBox()
        for sector in range(1, 10):
            self.sector_combo.addItem(str(sector), sector)
        self.sector_combo.setCurrentIndex(0)
        layout.addWidget(self.sector_combo)

        self.positive_combo = QComboBox()
        for value in [True, False]:
            self.positive_combo.addItem(str(value), value)
        self.positive_combo.setCurrentIndex(0)
        layout.addWidget(self.positive_combo)

        self.submit_button = QPushButton("Submit Drone Update")
        self.submit_button.clicked.connect(self.on_submit_button_clicked)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def on_submit_button_clicked(self):
        return self.submitted.emit(
            DroneUpdate(
                self.sector_combo.currentData(), self.positive_combo.currentData()
            )
        )
