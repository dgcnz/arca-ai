from typing import List
from lib.types import Interpretation, Action
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
        super().__init__(name, "rule")

        self.chatbot = ChatBot(
            agent_name,
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            logic_adapters=logic_adapters,
            database_uri='sqlite:///database.db')

        self.trainer = ChatterBotCorpusTrainer(self.chatbot)

    def train(self, model_corpuses):

        for corpus in model_corpuses:
            (self.trainer).train(corpus)

    def decide(self, ir: Interpretation) -> List[Action]:
        # TODO: Model need to know possible actuators
        ans = self.chatbot.get_response(ir.data)
        return [Action("speech", str(ans))]
