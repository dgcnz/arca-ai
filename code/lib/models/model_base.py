from typing import List, Any
from abc import ABC, abstractmethod
from lib.types import Action, Component, Identifier, Information, Interpretation


class Model(Component, ABC):
    def __init__(self, name: str):
        super().__init__(name)

    def send(self, raw_data):
        for dest_ID in self.get_destinations_ID(raw_data):
            self.sendID(Action(self.dumpID(), dest_ID, raw_data))

    def put(self, data: Information) -> None:
        raw_actions = self.decide(data)
        for raw_action in raw_actions:
            if raw_action["data"] is not None:
                self.send(raw_action)

    @abstractmethod
    def decide(self, data: Interpretation) -> List[Any]:
        pass
