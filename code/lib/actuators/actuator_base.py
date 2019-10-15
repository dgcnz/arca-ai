from lib.types import Action, Entity
from abc import ABC, abstractmethod


class Actuator(Entity, ABC):
    def __init__(self, name):
        super().__init__(name)

    def put(self, action: Action) -> None:
        self.do(action)

    @abstractmethod
    def do(self, action: Action) -> None:
        pass

    @abstractmethod
    def pass_msg(self, msg: str) -> None:
        pass
