from lib.actuators.actuator_base import Actuator
from lib.types import Action
from subprocess import call
import os


class Speech(Actuator):
    def __init__(self, name: str):
        super().__init__(name)

    def do(self, action: Action):
        call(["python", "lib/utilities/speak.py", action.data])
