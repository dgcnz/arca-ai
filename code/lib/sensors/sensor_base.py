from lib.types import Percept, Status, Entity, Identifier
from abc import ABC, abstractmethod
from threading import Thread, Event
from typing import Callable, List

TIMEOUT = 1.0


class Sensor(Entity, ABC):
    def __init__(self, name: str, sense: Callable[[None], None]):
        super().__init__(name)
        self.__perceiver = Thread(target=sense)
        self.wait_event = Event()
        self.status = Status.STOPPED

    def on(self):
        self.status = Status.RUNNING
        self.wait_event.set()
        print(f"{self.name} sensor is on.")
        self.__perceiver.start()

    def off(self):
        self.status = Status.STOPPED
        self.__perceiver.join(timeout=TIMEOUT)
        if self.__perceiver.is_alive():
            raise Exception(f"Sensor {self.name} wasn't shut down correctly.")
        print(f"{self.name} sensor is off.")

    def send(self, raw_data):
        for dest_ID in self.get_destinations_ID(raw_data):
            self.sendID(Percept(self.dumpID(), dest_ID, raw_data))

    def resume(self):
        self.wait_event.set()
        self.status = Status.RUNNING

    def pause(self):
        self.wait_event.clear()
        self.status = Status.PAUSED

    def check_status(self):
        print(f"SENSOR.IS_ALIVE(): {self.__perceiver.is_alive()}")

    @abstractmethod
    def get_destinations_ID(self, raw_data) -> List[Identifier]:
        pass

    @abstractmethod
    def pass_msg(self, msg: str) -> None:
        pass
