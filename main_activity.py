from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QPixmap

from commander import Commander
from screen_area_activity import ScreenAreaLabel


class MainActivity(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication.instance()
        # Buttons
        self.step_button = QtWidgets.QPushButton("add step")
        self.run_button = QtWidgets.QPushButton("Run")
        # Buttons Actions
        self.step_button.clicked.connect(self.openCapture)
        self.run_button.clicked.connect(self.clearSteps)
        # Layouts
        self.h_layout = QtWidgets.QHBoxLayout(self)
        self.v_layout = QtWidgets.QVBoxLayout(self)
        self.steps_layout = QtWidgets.QVBoxLayout(self)
        # ScrollArea
        self.scroll = QtWidgets.QScrollArea(self)
        self.scrollContent = QtWidgets.QWidget(self.scroll)
        self.initScrollArea()

        # Layouts Settings
        self.setLayout(self.h_layout)
        self.v_layout.addWidget(self.run_button)
        self.v_layout.addWidget(self.step_button)
        self.h_layout.addLayout(self.steps_layout)
        self.h_layout.addLayout(self.v_layout)
        self.screen_area_label = ScreenAreaLabel()
        self.screen_area_label.setVisible(False)
        self.initSteps()

    def resizeEvent(self, event):
        self.scroll.resize(self.width(), int(self.height() / 3))

    def initScrollArea(self):
        self.steps_layout.addWidget(self.scroll)
        self.scroll.setWidgetResizable(True)
        self.steps_layout = QtWidgets.QVBoxLayout(self.scrollContent)
        self.scroll.setWidget(self.scrollContent)
        self.scrollContent.setLayout(self.steps_layout)
        self.scroll.resize(self.width(), int(self.height() / 3))

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

    def onRun(self):
        commander = Commander()


class StepWidget(QtWidgets.QWidget):
    def __init__(self, step):
        super().__init__()
        self.textLabel = QtWidgets.QLabel()
        self.pictureLabel = QtWidgets.QLabel()
        self.textLabel.setText(str(step["id"]))
        self.pictureLabel.setPixmap(QPixmap(step["picture_filename"]))
        self.h_layout = QtWidgets.QHBoxLayout(self)
        self.h_layout.addWidget(self.pictureLabel)
        self.h_layout.addWidget(self.textLabel)
