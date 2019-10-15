from lib.types import Interpretation, Identifier, Entity, Information
from typing import List, Any, Callable, Generator
from abc import ABC, abstractmethod
from queue import Queue
from threading import Thread, Event
import time


def threaded(fx):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fx, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


class Interpreter(Entity, ABC):
    def __init__(self, name: str, waitable: bool):
        super().__init__(name)
        self.percept_buffer = []
        self.queue = Queue()
        self.e = Event()
        self.waitable = waitable

    def put(self, data: Information) -> None:
        self.queue.put(data)

    def send(self, raw_data):
        for dest_ID in self.get_destinations_ID(raw_data):
            self.sendID(Interpretation(self.dumpID(), dest_ID, raw_data))

    @threaded
    def listen(self):
        cur_proc_data = None
        while True:
            # Queue is suspended until there is something to read from the queu
            raw_data = self.queue.get()
            data = self.preprocess(raw_data.data)
            gen = self.process(data, cur_proc_data)
            stop = next(gen)
            print(f"STOP: {stop}")
            if stop:
                self.sendID("PAUSE", raw_data.src)
                cur_proc_data = next(gen)
                self.send(cur_proc_data)
                if self.waitable:
                    self.e.wait()
                self.e.clear()
                print("FINISHED WAITING, RESUMING SENSOR")
                self.sendID("RESUME", raw_data.src)
                with self.queue.mutex:
                    self.queue.queue.clear()

    @abstractmethod
    def get_destinations_ID(self, raw_data) -> List[Identifier]:
        """Given some data, decide destination. Must handle None/empty data."""
        pass

    @abstractmethod
    def preprocess(self, raw_data):
        pass

    @abstractmethod
    def process(self, raw_data, processed_data) -> Generator:
        pass

    @abstractmethod
    def pass_msg(self, msg: str) -> None:
        pass
