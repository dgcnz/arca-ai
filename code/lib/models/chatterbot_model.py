from typing import List, Any, Tuple, Callable
from lib.types import Interpretation, Identifier, NestedDefaultDict
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
        ans = []

        for k, v in self.memory.items():
            msg = f"{arrow.get(k).humanize(locale='es')}: {v}"
            ans.append(msg)

        return ans[0]

    def answer(self, data: Any) -> str:
        pass

    def repeat(self, data: Any) -> str:
        return str(data["text"])

    def remind(self, data: Any) -> None:
        try:
            date = data["attr"]["datetime"]["value"]
        except:
            print("NO DATE WAS PROVIDED.")
        # put value into memory at date

        self.memory[date] = data["text"]
        return None

    def decide(self, ir: Interpretation) -> List[Any]:
        """
        Return a list of raw actions given an Interpretation.
        """
        cmds_fx: List[Command] = []
        raw_actions: List[Any] = []

        if ir.data["text"] is None or len(ir.data["attr"]["commands"]) == 0:
            return []

        cmds_fx = [self.parse_command(x) for x in ir.data["attr"]["commands"]]

        raw_actions = [{
            "data": fx(ir.data),
            "command": cmd
        } for cmd, fx in cmds_fx]

        return raw_actions

    def get_destinations_ID(self, raw_data) -> List[Identifier]:
        """Given some data, decide destination. Must handle None/empty data."""

        return [self.destinations_ID[0]]

    def pass_msg(self, msg: str) -> None:
        pass

    def dump_history(self, filename: str, data: List[Any]) -> None:
        pass
