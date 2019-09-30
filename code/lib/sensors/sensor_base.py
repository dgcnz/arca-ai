from lib.types import Percept, Status
from threading import Thread
from typing import Callable

TIMEOUT = 1.0


class Sensor:
    def __init__(self, name: str, interpreter_name: str,
                 percept_callback: Callable[[Percept], None],
                 sense: Callable[[None], None]):
        self.name: str = name
        self.interpreter_name: str = interpreter_name
        self.status: Status = Status.STOPPED
        self.__perceiver = Thread(target=sense)
        self.percept_callback = percept_callback

    def on(self):
        self.status = Status.RUNNING
        print(f"{self.name} sensor is on.")
        self.__perceiver.start()

    def off(self):
        self.status = Status.STOPPED
        self.__perceiver.join(timeout=TIMEOUT)
        if self.__perceiver.is_alive():
            raise Exception(f"Sensor {self.name} wasn't shut down correctly.")
        print(f"{self.name} sensor is off.")

    def resume(self):
        self.status = Status.RUNNING

    def pause(self):
        self.status = Status.PAUSED

    def check_status(self):
        print(f"SENSOR.IS_ALIVE(): {self.__perceiver.is_alive()}")
