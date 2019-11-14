from typing import List, Any
from abc import ABC, abstractmethod
from lib.types import Action, Component, Information, Interpretation
import threading


class Model(Component, ABC):
    def __init__(self, name: str):
        super().__init__(name)

    def send(self, raw_actions):
        for raw_action, dest_ID in raw_actions:
            self.sendID(Action(self.dumpID(), dest_ID, raw_action))

    def put(self, data: Information) -> None:
        raw_actions = self.decide(data)
        for raw_action in raw_actions:
            if type(raw_action) is list:
                threads = []
                for i, r in enumerate(raw_action):
                    if raw_action["data"] is not None:
                        # thread it
                        threads[i] = threading.Thread(target=self.send,
                                                      args=[raw_action])
                        threads[i].start()
                # Wait for every thread to finish
                for i in range(len(raw_action)):
                    threads[i].join()
            else:
                if raw_action["data"] is not None:
                    self.send(raw_action)

    @abstractmethod
    def decide(self, data: Interpretation) -> List[Any]:
        pass
