import sys
import json
from PySide6 import QtWidgets
from main_activity import MainActivity
from step import StepManager

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.step_manager = StepManager()
    with open("save.json", "r") as file:
        serialized_info = file.read()
        app.step_manager.steps = json.loads(serialized_info)["steps"]
    app.main_activity = MainActivity()
    app.main_activity.resize(800, 600)
    app.main_activity.show()

    sys.exit(app.exec())
