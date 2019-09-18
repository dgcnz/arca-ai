from lib.actuators.actuator_base import Actuator
from lib.types import Action


class Speech(Actuator):
    def __init__(self, name: str):
        super().__init__(name)

    def do(self, action: Action):
        pass
