from lib.interpreters.interpreter_base import Interpreter
from lib.types import Identifier
from typing import List, Generator, Any, Tuple
from nltk.tokenize.toktok import ToktokTokenizer
from duckling import DucklingWrapper, Language
from pattern.es import parse, split, conjugate, PRESENT, IMPERATIVE, SG
import re
import string
import unicodedata

tokenize = ToktokTokenizer().tokenize
duck = DucklingWrapper(language=Language.SPANISH)
pron_refl = ["me", "te", "se", "nos", "os"]
pron_dobj = ["lo", "los", "la", "las"]
enclitic_pat = re.compile(
    f".*(?={'|'.join(pron_refl)})(?={'|'.join(pron_dobj)})?")


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


def is_imperative(word: str):
    base = enclitic_pat.match(word)
    if base:
        txt = base.group()
        txt = normalize(txt)
        ans = parse(txt, lemmata=True).split('/')
        return True, '/'.join([word] + ans[1:])
    return False, None


def parse_date(sent: str):
    if sent is None:
        return None
    ans = duck.parse_time(sent)
    precedence = ["year", "month", "day", "hour", "minute", "second"]

    if len(ans) > 0:
        text = ans[0]["text"]
        val = ans[0]["value"]["value"]
        if "grain" in ans[0]["value"]:
            precision = precedence[precedence.index(ans[0]["value"]["grain"]) -
                                   1]
        else:
            precision = None

        if "to" in val:
            return {"text": text, "value": val["to"], "precision": precision}
        else:
            return {"text": text, "value": val, "precision": precision}
    else:
        return None


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


class NLU(Interpreter):
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
