import json
from json import JSONEncoder


class StepManager:
    def __init__(self):
        self.steps = {}

    def __dict__(self):
        return {"steps": self.steps}

    def addStep(self, step):
        self.steps[step.id] = step
        serialized_info = json.dumps(self.__dict__(), default=lambda o: o.__dict__, indent=4)
        print('Serialized data:', serialized_info)
        with open("save.json", "w+") as file:
            file.write(serialized_info)


class Step(object):
    def __init__(self, _id, _previous=None, _next=None, picture_filename=""):
        self.id = _id
        self.picture_filename = picture_filename
