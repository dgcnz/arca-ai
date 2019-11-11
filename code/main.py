import settings
import time
import signal
import sys
from lib.ai import Agent
from lib.sensors.audition import Audition
from lib.interpreters.nlp import NLP
from lib.interpreters.speech_recognizer import SpeechRecognizer
from lib.models.chatterbot_model import Language
from lib.actuators.speech import Speech
# from lib.observers.web import WebInterface

la = [{
    'import_path': 'chatterbot.logic.BestMatch',
    'default_response': 'Lo siento, no entendí.',
    'maximum_similarity_threshold': 0.70,
    "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance"
}]

corpuses = [
    './resources/corpuses/spanish/',
]

ARCA = Agent("ARCA")


def test_model():
    lang = Language("language", "ARCA", la)
    lang.train(corpuses)

    while True:
        x = input("> ")
        if x == "stop":
            break
        data = {"text": x}
        ans = lang.chat(data)
        print(ans)

    return


def signal_handler(sig, frame):
    print('CTRL-C.')
    ARCA.shutdown()
    sys.exit(0)


def main():
    # test_model()
    # server = WebInterface("localhost", 8000)
    # server.activate()

    # ARCA.attach_observer(server)
    signal.signal(signal.SIGINT, signal_handler)

    hearing = Audition("mic_0")
    sr = SpeechRecognizer("sr", "googlespeech")
    nlp = NLP("nlp")
    lang = Language("language", "ARCA", la)
    # lang.train(corpuses)
    voice = Speech("speech")

    ARCA.add_component(hearing)
    ARCA.add_component(nlp)
    ARCA.add_component(sr)
    ARCA.add_component(lang)
    ARCA.add_component(voice)

    ARCA.associate(hearing, sr)
    ARCA.associate(sr, nlp)
    ARCA.associate(nlp, lang)
    ARCA.associate(lang, voice)

    ARCA.interpreters["sr"].listen()
    ARCA.interpreters["nlp"].listen()

    ARCA.sensors["mic_0"].on()
    while True:
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
