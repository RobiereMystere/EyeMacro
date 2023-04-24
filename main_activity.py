from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QPixmap

from screen_area_activity import ScreenAreaLabel


class MainActivity(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication.instance()
        self.step_button = QtWidgets.QPushButton("add step")
        self.refresh_button = QtWidgets.QPushButton("Refresh")
        self.run_button = QtWidgets.QPushButton("Run")
        self.h_layout = QtWidgets.QHBoxLayout(self)
        self.steps_layout = QtWidgets.QVBoxLayout(self)
        self.initSteps()
        self.setLayout(self.h_layout)
        self.scroll =  QtWidgets.QScrollArea(self)
        self.steps_layout.addWidget(self.scroll)
        self.scroll.setWidgetResizable(True)
        self.scrollContent =  QtWidgets.QWidget(self.scroll)
        self.steps_layout =  QtWidgets.QVBoxLayout(self.scrollContent)
        self.scrollContent.setLayout(self.steps_layout)
        self.scroll.setWidget(self.scrollContent)
        self.v_layout = QtWidgets.QVBoxLayout(self)
        self.v_layout.addWidget(self.refresh_button)
        self.v_layout.addWidget(self.step_button)
        self.h_layout.addLayout(self.steps_layout)
        self.h_layout.addLayout(self.v_layout)
        self.screen_area_label = ScreenAreaLabel()
        self.screen_area_label.setVisible(False)
        self.step_button.clicked.connect(self.openCapture)
        self.refresh_button.clicked.connect(self.clearSteps)

    def openCapture(self):
        self.screen_area_label = ScreenAreaLabel()
        self.screen_area_label.setVisible(True)
        # self.setVisible(False)
        # self.screen_area_label.show()

    def update(self) -> None:
        self.initSteps()
        super().update()

    def initSteps(self):
        print(self.app.step_manager.steps)
        self.clearSteps()
        for key, value in self.app.step_manager.steps.items():
            step_widget = StepWidget(value)
            self.steps_layout.addWidget(step_widget)

    def clearSteps(self):
        children = []
        for i in range(self.steps_layout.count()):
            child = self.steps_layout.itemAt(i).widget()
            if child:
                children.append(child)
        for child in children:
            child.deleteLater()


class StepWidget(QtWidgets.QWidget):
    def __init__(self, step):
        super().__init__()
        self.textLabel = QtWidgets.QLabel()
        self.pictureLabel = QtWidgets.QLabel()
        self.textLabel.setText(str(step["id"]))
        self.pictureLabel.setPixmap(QPixmap(step["picture_filename"]))
        self.h_layout = QtWidgets.QHBoxLayout(self)
        self.h_layout.addWidget(self.textLabel)
        self.h_layout.addWidget(self.pictureLabel)
