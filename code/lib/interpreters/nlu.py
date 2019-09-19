from lib.interpreters.interpreter_base import Interpreter
from lib.types import Percept, Interpretation


class NLU(Interpreter):
    def __init__(self, name: str, model_names):
        super().__init__(name, model_names)

    def preprocess(self, data):
        return data

    def interpret(self, percept: Percept) -> Interpretation:
        # Preprocessing stage
        data = self.preprocess(percept.data)

        return Interpretation(self.name, "chatterbot", "rule", data)
