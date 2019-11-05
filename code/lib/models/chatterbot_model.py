from typing import List, Any, Tuple, Callable
from lib.types import Interpretation, Identifier, NestedDefaultDict
from lib.utilities.helpers import rec_dict_access
from lib.models.model_base import Model
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from chatterbot.logic import LogicAdapter
from enum import Enum, auto
import arrow

# logica = [{
#     'import_path': 'chatterbot.logic.BestMatch',
#     'default_response': 'Lo siento, no entendí.',
#     'maximum_similarity_threshold': 0.90
# }]


class Command(Enum):
    MOVE = auto()
    REMIND = auto()
    SAY = auto()
    ANSWER = auto()
    CHAT = auto()
    REPEAT = auto()


class Chatterbot(Model):
    def __init__(self, name: str, agent_name: str,
                 logic_adapters: List[LogicAdapter]):
        super().__init__(name)

        self.chatbot = ChatBot(
            agent_name,
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            logic_adapters=logic_adapters,
            database_uri='sqlite:///database.db')
        self.trainer = ChatterBotCorpusTrainer(self.chatbot)
        self.memory = NestedDefaultDict()
        self.logger = self.get_logger()

    def train(self, model_corpuses: Any) -> None:
        for corpus in model_corpuses:
            (self.trainer).train(corpus)

    def parse_command(self, command: str) -> Tuple[Command, Callable]:
        if command == "recordar":
            return Command.REMIND, self.remind
        if command == "decir":
            return Command.SAY, self.say
        if command == "responder":
            return Command.ANSWER, self.answer
        if command == "conversar":
            return Command.CHAT, self.chat
        if command == "repetir":
            return Command.REPEAT, self.repeat
        else:
            return Command.CHAT, self.chat

    def chat(self, data: Any) -> str:
        ans = self.chatbot.get_response(data["text"])
        return str(ans)

    def say(self, data: Any) -> str:
        # get from memory or answer

        date = data["attr"]["datetime"]
        if date is not None and date["precision"] is not None:
            ans = []
            precision = date["precision"]
            self.logger.info("DATE: ", date)

            date_task = self.get_tasks_from_precision(date, precision)
            for (date_str, task) in date_task:
                a = arrow.get(
                    date_str,
                    "YYYY MM DD HH mm").replace(tzinfo="America/Lima")
                self.logger.info(f"DATE FROM MEMORY: {date_str}")
                print(a.humanize(locale="es"))
                print(a)
                msg = f"{a.humanize(locale='es')}: {task}"
                ans.append(msg)
            if len(ans) == 0:
                return f"No hay nada pendiente {date['text']}"
            return ", ".join(ans)

        self.logger.info("NO USEFUL DATE WAS PROVIDED.")
        return self.chat(data)

    def answer(self, data: Any) -> str:
        pass

    def repeat(self, data: Any) -> str:
        return str(data["text"])

    def remind(self, data: Any) -> None:
        if data["attr"]["datetime"] is not None:
            date = data["attr"]["datetime"]
            self.logger.info("DATE: ", date)
            print(date)
            self.remember(date["value"], data["attr"]["task"])
        else:
            self.logger.info("NO DATE WAS PROVIDED.")
        # put value into memory at date

        return None

    def remember(self, date: str, subj: str):
        # 2019-11-04T16:41:00.000-05:00
        d = arrow.get(date)
        year, month, day, hour, minute = d.format("YYYY MM DD HH mm").split(
            " ")

        try:
            self.memory[year][month][day][hour][minute].append(subj)
        except Exception:
            self.memory[year][month][day][hour][minute] = [subj]

    def get_tasks_from_precision(self, date, precision):
        precedence = ["year", "month", "day", "hour", "minute", "second"]
        index = precedence.index(precision)
        date = arrow.get(date["value"])
        ymdhm = date.format("YYYY MM DD HH mm").split(" ")

        base = ymdhm[:index + 1]
        temp = self.memory
        for i in range(index + 1):
            temp = temp[ymdhm[i]]

        return rec_dict_access(temp, " ".join(base))

    def decide(self, ir: Interpretation) -> List[Any]:
        """
        Return a list of raw actions given an Interpretation.
        """
        raw_actions: List[Any] = []

        if ir.data["text"] is None:
            return []

        cmd, fx = self.parse_command(ir.data["attr"]["command"])

        raw_actions = [{"data": fx(ir.data), "command": cmd}]

        return raw_actions

    def get_destinations_ID(self, raw_data) -> List[Identifier]:
        """Given some data, decide destination. Must handle None/empty data."""

        return [self.destinations_ID[0]]

    def pass_msg(self, msg: str) -> None:
        pass

    def dump_history(self, filename: str, data: List[Any]) -> None:
        pass
