import os
import sys
sys.path.append(os.getcwd())

from lib.utilities import settings
from lib.models.chatterbot_model import Language
from chatterbot.trainers import ListTrainer

la = [{
    'import_path':
    'chatterbot.logic.BestMatch',
    'default_response':
    'Lo siento, no entendí.',
    'maximum_similarity_threshold':
    0.70,
    "statement_comparison_function":
    "chatterbot.comparisons.levenshtein_distance"
}]

lang = Language("language", "ARCA", la)
trainer = ListTrainer(lang.chatbot)


def train_model(corpus: str = None):
    sentences = []

    if corpus is not None and os.path.exists(corpus):
        lang.train(corpus)
    else:
        while True:
            line = input(">> ")
            if line == "/exit":
                break
            ans = lang.chat({"data": line})
            sentences.append(line)

    trainer.train(sentences)
    
