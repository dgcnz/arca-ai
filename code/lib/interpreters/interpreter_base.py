from lib.types import Percept, Interpretation


class Interpreter:
    def __init__(self, name: str, model_names):
        self.name = name
        self.model_names = model_names

    def preprocess(self, data):
        pass

    def interpret(self, percept: Percept) -> Interpretation:
        pass
