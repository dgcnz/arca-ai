from lib.types import Percept
from typing import Callable


class Sensor:
    def __init__(self, name: str, interpreter_name: str,
                 percept_callback: Callable[[Percept], None]):
        self.name: str = name
        self.interpreter_name: str = interpreter_name
        self.status: bool = False
        self.percept_callback = percept_callback

    def on(self):
        self.status = True
        print(f"{self.name} sensor is on.")

    def off(self):
        self.status = False
        print(f"{self.name} sensor is off.")
