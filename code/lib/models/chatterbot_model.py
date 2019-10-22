from typing import List, Any
from lib.types import Interpretation, Identifier
from lib.models.model_base import Model
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from chatterbot.logic import LogicAdapter

# logica = [{
#     'import_path': 'chatterbot.logic.BestMatch',
#     'default_response': 'Lo siento, no entendí.',
#     'maximum_similarity_threshold': 0.90
# }]


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

    def train(self, model_corpuses):
        for corpus in model_corpuses:
            (self.trainer).train(corpus)

    def decide(self, ir: Interpretation) -> List[Any]:
        if ir.data is None:
            return []
        ans = self.chatbot.get_response(ir.data)
        return [str(ans)]

    def get_destinations_ID(self, raw_data) -> List[Identifier]:
        """Given some data, decide destination. Must handle None/empty data."""
        return [self.destinations_ID[0]]

    def pass_msg(self, msg: str) -> None:
        pass

    def dump_history(self, filename: str, data: List[Any]) -> None:
        pass
