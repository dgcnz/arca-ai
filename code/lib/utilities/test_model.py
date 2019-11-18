
import os
import sys
sys.path.append(os.getcwd())

from lib.utilities import settings
from lib.models.chatterbot_model import Language

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

def test_model():
    while True:
        x = input("> ")
        if x == "stop":
            break
        data = {"text": x}
        ans = lang.chat(data)
        print(ans)

    return

if __name__ == "__main__":
    test_model()
