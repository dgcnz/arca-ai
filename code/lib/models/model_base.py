from typing import List, Any
from abc import ABC, abstractmethod
from lib.types import Action, Entity, Identifier, Information, Interpretation


class Model(Entity, ABC):
    def __init__(self, name: str):
        super().__init__(name)

    def send(self, raw_data):
        for dest_ID in self.get_destinations_ID(raw_data):
            self.sendID(Action(self.dumpID(), dest_ID, raw_data))

    def put(self, data: Information) -> None:
        raw_actions = self.decide(data)
        for raw_action in raw_actions:
            self.send(raw_action)

    @abstractmethod
    def get_destinations_ID(self, raw_data) -> List[Identifier]:
        """Given some data, decide destination. Must handle None/empty data."""
        pass

    @abstractmethod
    def decide(self, data: Interpretation) -> List[Any]:
        pass

    @abstractmethod
    def pass_msg(self, msg: str) -> None:
        pass
