from enum import Enum, auto
from typing import Callable, List


class Status(Enum):
    RUNNING = auto()
    PAUSED = auto()
    STOPPED = auto()


class Identifier:
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category


class Entity:
    def __init__(self, name):
        self.name: str = name
        self.destinations_ID: List[Identifier] = []
        self.sendID: Callable[[Identifier], None]

    def add_destination_ID(self, dest_ID: Identifier):
        self.destinations_ID.append(dest_ID)

    def dumpID(self) -> Identifier:
        base_class = self.__class__.__bases__[0].__name__
        return Identifier(self.name, base_class)


class Information:
    pass


class Percept(Information):
    def __init__(self, src: Identifier, dest: Identifier, data):
        self.src = src
        self.dest = dest
        self.data = data


class Interpretation(Information):
    def __init__(self, src: Identifier, dest: Identifier, data):
        self.src = src
        self.dest = dest
        self.data = data


class Action(Information):
    def __init__(self, src: Identifier, dest: Identifier, data):
        self.src = src
        self.dest = dest
        self.data = data
