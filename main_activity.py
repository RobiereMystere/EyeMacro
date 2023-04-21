import random
from PySide6 import QtCore, QtWidgets

from screen_area_activity import ScreenAreaLabel


class MainActivity(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication.instance()
        self.step_button = QtWidgets.QPushButton("add step")
        self.open_file_button = QtWidgets.QPushButton("Open File")
        self.run_button = QtWidgets.QPushButton("Run")

        self.h_layout = QtWidgets.QHBoxLayout(self)

        self.v_layout = QtWidgets.QVBoxLayout(self)
        self.v_layout.addWidget(self.open_file_button)
        self.v_layout.addWidget(self.step_button)
        self.h_layout.addLayout(self.v_layout)
        self.screen_area_label = ScreenAreaLabel()
        self.screen_area_label.setVisible(False)
        self.step_button.clicked.connect(self.openCapture)

    def openCapture(self):
        self.screen_area_label = ScreenAreaLabel()
        self.screen_area_label.setVisible(True)
        # self.setVisible(False)
        self.screen_area_label.show()
