from lib.interpreters.interpreter_base import Interpreter
from lib.types import Identifier
from lib.utilities.helpers import get_logger, get_date
from typing import List, Generator, Any
from nltk.tokenize.toktok import ToktokTokenizer
from duckling import DucklingWrapper, Language
from pattern.es import parse, split, conjugate, PRESENT, IMPERATIVE, SG
import re
import string
import unicodedata

tokenize = ToktokTokenizer().tokenize
d = DucklingWrapper(language=Language.SPANISH)
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

    ans = d.parse_time(sent)
    if len(ans) > 0:
        return {"text": ans[0]["text"], "value": ans[0]["value"]["value"]}
    else:
        return None


def syntax_analyze(sent: str):
    parsed_list = []
    commands = []
    if sent is not None:
        parsed = parse(sent, lemmata=True)
        parsed_list = parsed.split(" ")

        for s in split(parsed)[0]:
            if s.index == 0 and s.type != "VB":
                flag, fixed = is_imperative(str(s))
                if flag:
                    parsed_list[s.index] = fixed
                    commands.append(fixed.split("/")[-1])
            if s.index == 0 and s.type == "VB":
                if conjugate(str(s), PRESENT, 2, SG,
                             mood=IMPERATIVE) == str(s).lower():
                    commands.append(str(s).lower())
    if len(commands) == 0:
        commands.append("responder")

    return parsed_list, commands


class NLU(Interpreter):
    def __init__(self, name: str):
        super().__init__(name, False)
        name, cat = self.dumpID().to_tuple()
        self.logger = get_logger(f"{cat}.{name}",
                                 f"logs/{cat}/{name}/{get_date()}")

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
        syntax, commands = syntax_analyze(raw_data)
        res = {
            "text": raw_data,
            "attr": {
                "datetime": parse_date(raw_data),
                "commands": commands,
                "syntax": syntax
            }
        }
        print(res)
        yield res
        return

    def pass_msg(self, msg: str) -> None:
        pass

    def dump_history(self, filename: str, data: List[Any]) -> None:
        pass
