import pyautogui


class Commander:

    @staticmethod
    def click(args):
        pyautogui.click(args)

    def __init__(self):
        self.cmds = {
            "click": self.click
        }

    def run(self, cmd, args):
        self.cmds[cmd](*args)
