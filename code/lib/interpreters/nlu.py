from lib.interpreters.interpreter_base import Interpreter
from lib.types import Identifier
from typing import List, Generator, Any
from nltk.tokenize.toktok import ToktokTokenizer
import string
import unicodedata

tokenize = ToktokTokenizer().tokenize


def untokenize(tokens):
    return ("".join([
        " " + token if not (token.startswith("'")
                            or tokens[i - 1] in ['¿', '¡'] or token == "...")
        and token not in string.punctuation else token
        for i, token in enumerate(tokens)
    ]).strip())


class NLU(Interpreter):
    def __init__(self, name: str):
        super().__init__(name, False)

    def get_destinations_ID(self, raw_data) -> List[Identifier]:
        return [self.destinations_ID[0]]

    def preprocess(self, raw_data):
        if raw_data is None:
            return None
        # Remove all non-ascii characters
        res = unicodedata.normalize('NFKD',
                                    raw_data).encode('ascii',
                                                     'ignore').decode('utf-8')

        # tokenize
        tokens = tokenize(res)

        # Remove all non-alohanumerical tokens and lowercase them
        tokens = [word.lower() for word in tokens if word.isalnum()]

        # Put tokens together
        res = untokenize(tokens)
        return res

    def process(self, raw_data) -> Generator:
        yield True
        yield raw_data
        return

    def pass_msg(self, msg: str) -> None:
        pass

    def dump_history(self, filename: str, data: List[Any]) -> None:
        pass
