from typing import List
from lib.types import Interpretation, Action


class Model:
    def __init__(self, name: str, kind: str):
        self.name = name
        self.kind = kind

    def decide(self, ir: Interpretation) -> List[Action]:
        pass
