import pyscreenshot


class ScreenArea:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1

        self.x2 = x2
        self.y2 = y2


class ScreenshotTaker:
    def __init__(self):
        print()

    def take(self, area):
        screenshot = pyscreenshot.grab(bbox=(area.x1, area.y1, area.x2, area.y2))
        return screenshot
