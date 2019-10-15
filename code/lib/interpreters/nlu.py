from lib.interpreters.interpreter_base import Interpreter
from lib.types import Identifier
from typing import List, Generator


class NLU(Interpreter):
    def __init__(self, name: str):
        super().__init__(name, False)

    def get_destinations_ID(self, raw_data) -> List[Identifier]:
        return [self.destinations_ID[0]]

    def preprocess(self, raw_data):
        return raw_data

    def process(self, raw_data, processed_data) -> Generator:
        yield True
        yield raw_data
        return

    def pass_msg(self, msg: str) -> None:
        pass
