from lib.types import Percept, Status, Entity, Identifier
from abc import ABC, abstractmethod
from threading import Thread, Event
from typing import List, Any

TIMEOUT = 1.0


class Sensor(Entity, ABC):
    def __init__(self, name: str, waitable: bool):
        super().__init__(name)
        self.__perceiver = Thread(target=self.perceiver)
        self.wait_event = Event()
        self.status = Status.STOPPED
        self.waitable = waitable

    def on(self) -> None:
        """
        Sets wait_event to allow processing and
        starts sense function in another thread.
        """
        self.status = Status.RUNNING
        self.wait_event.set()
        print(f"{self.name} sensor is on.")
        self.__perceiver.start()

    def off(self) -> None:
        """
        Sets wait_event to allow processing and
        starts sense function in another thread.
        """
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

    def perceiver(self):
        """
        Reads and sends input. Waits if wait() method was called.
        """
        self.setup_perceiver()
        while True:
            if self.status == Status.STOPPED:
                break
            if self.waitable:
                self.wait_event.wait()

            data = self.read_input()
            if data is not None:
                self.send(data)
        self.close_perceiver()

    @abstractmethod
    def get_destinations_ID(self, raw_data) -> List[Identifier]:
        pass

    @abstractmethod
    def pass_msg(self, msg: str) -> None:
        pass

    @abstractmethod
    def read_input(self) -> Any:
        pass

    @abstractmethod
    def setup_perceiver(self) -> None:
        pass

    @abstractmethod
    def close_perceiver(self) -> None:
        pass
