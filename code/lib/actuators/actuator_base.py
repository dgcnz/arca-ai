from lib.types import Action


class Actuator:
    def __init__(self, name):
        self.name = name

    def do(self, action: Action):
        pass
