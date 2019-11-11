from pattern.es import parse, split, conjugate, PRESENT, IMPERATIVE, SG
from lib.interpreters.interpreter_base import Interpreter
from nltk.tokenize.toktok import ToktokTokenizer
from typing import List, Generator, Any, Tuple
from lib.types import Identifier
import unicodedata
import requests
import string
import re
import os

tokenize = ToktokTokenizer().tokenize
pron_refl = ["me", "te", "se", "nos", "os"]
pron_dobj = ["lo", "los", "la", "las"]
enclitic_pat = re.compile(
    f".*(?={'|'.join(pron_refl)})(?={'|'.join(pron_dobj)})?")
DUCKLING_HOST = os.getenv("DUCKLING_HOST")
DUCKLING_PORT = os.getenv("DUCKLING_PORT")
print(DUCKLING_HOST, DUCKLING_PORT)
DUCKLING_URL = f"{DUCKLING_HOST}:{DUCKLING_PORT}"


def untokenize(tokens):
    return ("".join([
        " " + token if not (token.startswith("'")
                            or tokens[i - 1] in ['¿', '¡'] or token == "...")
        and token not in string.punctuation else token
        for i, token in enumerate(tokens)
    ]).strip())


def normalize(string: str):
    res = unicodedata.normalize('NFKD',
                                string).encode('ascii',
                                               'ignore').decode('utf-8')
    return res


def parse_date(sent: str):
    r = requests.get(DUCKLING_URL, params={'sent': sent})
    if r.status_code == 200:
        return r.json()
    raise Exception(f"DUCKLING server is not responding. {DUCKLING_URL}")


def is_imperative(word: str):
    base = enclitic_pat.match(word)
    if base:
        txt = base.group()
        txt = normalize(txt)
        ans = parse(txt, lemmata=True).split('/')
        return True, '/'.join([word] + ans[1:])
    return False, None


def syntax_analyze(sent: str) -> Tuple[List, str]:
    parsed_list = []
    command = None
    if sent is not None:
        parsed = parse(sent, lemmata=True)
        parsed_list = parsed.split(" ")
        for s in split(parsed)[0]:
            if s.index == 0 and s.type != "VB":
                flag, fixed = is_imperative(str(s))
                if flag:
                    parsed_list[s.index] = fixed
                    command = fixed.split("/")[-1]
            if s.index == 0 and s.type == "VB":
                if conjugate(str(s), PRESENT, 2, SG,
                             mood=IMPERATIVE) == str(s).lower():
                    command = str(s).lower()
    if command is None:
        command = "conversar"
    return parsed_list, command


def get_type_sentence(sent: str) -> str:
    tokens = tokenize(sent)
    pass


class NLP(Interpreter):
    def __init__(self, name: str):
        super().__init__(name, False)
        name, cat = self.dumpID().to_tuple()
        self.logger = self.get_logger()

    def get_destinations_ID(self, raw_data) -> List[Identifier]:
        return [self.destinations_ID[0]]

    def preprocess(self, raw_data):
        if raw_data is None:
            return None
        # Remove all non-ascii characters
        res = normalize(raw_data)

        # tokenize
        tokens = tokenize(res)

        # Remove all non-alohanumerical tokens and lowercase them
        tokens = [word.lower() for word in tokens if word.isalnum()]

        # Put tokens together
        res = untokenize(tokens)
        return res

    def process(self, raw_data) -> Generator:
        yield True
        syntax, command, date, task = [None, None, None, None]

        if raw_data is not None:
            syntax, command = syntax_analyze(raw_data)
            date = parse_date(raw_data)
            try:
                task = raw_data.replace("" if date is None else date["text"],
                                        "")
                task = task.split(" ",
                                  1)[1] if command != "conversar" else task
            except Exception:
                pass

        res = {
            "text": raw_data,
            "attr": {
                "datetime": date,
                "command": command,
                "syntax": syntax,
                "task": task
            }
        }
        self.logger.info(res)
        yield res
        return

    def pass_msg(self, msg: str) -> None:
        pass

    def dump_history(self, filename: str, data: List[Any]) -> None:
        pass
