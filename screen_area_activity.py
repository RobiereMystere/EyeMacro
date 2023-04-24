import os

from PySide6 import QtCore, QtWidgets, QtGui
import pyscreenshot
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import QApplication, QLabel, QPushButton

from screenshot import ScreenArea, ScreenshotTaker
from step import Step


class ScreenAreaLabel(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        screenshot = pyscreenshot.grab()
        screenshot.save("screen.png")
        self.app = QApplication.instance()
        self.selected_screen = 0  # Select the desired monitor/screen

        self.screens_available = self.app.screens()
        self.screen = self.screens_available[self.selected_screen]
        self.screen_width = self.screen.size().width()
        self.screen_height = self.screen.size().height()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        self.setWindowTitle('Screen Area Selector')
        self.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.pixmap = QPixmap(self.screen_width, self.screen_height)
        self.pixmap.load("screen.png")
        self.setPixmap(self.pixmap)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.ok_button = QPushButton("Ok", self)
        self.ok_button.clicked.connect(self.onOk)
        self.ok_button.setVisible(False)
        self.show()

    def onOk(self):
        picture_filename = str(len(self.app.step_manager.steps)) + '.png'
        os.rename("temp.png", picture_filename)
        step = Step(len(self.app.step_manager.steps), picture_filename=picture_filename)
        self.app.step_manager.addStep(step)
        self.app.main_activity.initSteps()
        self.close()

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.ok_button.setVisible(False)
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        # self.begin = event.pos()
        self.end = event.pos()
        x1, y1, x2, y2 = self.begin.x(), self.begin.y(), self.end.x(), self.end.y()
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        if x1 == x2:
            x2 = x1 + 1
        if y1 == y2:
            y2 = y1 + 1
        area = ScreenArea(x1, y1, x2, y2)
        screenshot = ScreenshotTaker()
        pic = screenshot.take(area)
        pic.save("temp.png")
        if (True):
            self.addOkButton((x1 + x2) / 2, (y1 + y2) / 2)
        self.update()

    # draw 4 transparent rectangles around the selected area
    def paintEvent(self, event):
        x1, y1, x2, y2 = self.begin.x(), self.begin.y(), self.end.x(), self.end.y()
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        if x1 == x2:
            x2 = x1 + 1
        if y1 == y2:
            y2 = y1 + 1
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 110))
        painter.setBrush(brush)

        painter.drawRect(QtCore.QRect(
            QtCore.QPoint(0, 0), QtCore.QPoint(self.screen_width, y1)))
        painter.drawRect(QtCore.QRect(
            QtCore.QPoint(0, y2 + 1), QtCore.QPoint(self.screen_width, self.screen_height)))
        painter.drawRect(QtCore.QRect(
            QtCore.QPoint(0, y1 + 1), QtCore.QPoint(QtCore.QPoint(x1, y2))))
        painter.drawRect(QtCore.QRect(
            QtCore.QPoint(x2, y1 + 1), QtCore.QPoint(QtCore.QPoint(self.screen_width, y2))))

    def addOkButton(self, x, y):
        self.ok_button.setVisible(True)
        self.ok_button.move(x - self.ok_button.width() / 2, y - self.ok_button.height() / 2)
