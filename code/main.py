import time
from lib.ai import Agent
from lib.sensors.audition import Audition
from lib.interpreters.nlu import NLU
from lib.interpreters.speech_recognizer import SpeechRecognizer
from lib.models.chatterbot_model import Chatterbot
from lib.actuators.speech import Speech
from lib.observers.web import WebInterface

la = [{
    'import_path': 'chatterbot.logic.BestMatch',
    'default_response': 'Lo siento, no entendí.',
    'maximum_similarity_threshold': 0.60
}]

corpuses = [
    'chatterbot.corpus.spanish.conversations',
    'chatterbot.corpus.spanish.greetings',
    'chatterbot.corpus.spanish.trivia',
#    'chatterbot.corpus.spanish.ia',
]

ARCA = Agent("ARCA")


def main():

    # server = WebInterface("localhost", 8000)
    # server.activate()

    # ARCA.attach_observer(server)

    hearing = Audition("mic_0")
    sr = SpeechRecognizer("sr", "googlespeech")
    nlu = NLU("nlu")
    cbot = Chatterbot("chatterbot", "ARCA", la)
    cbot.train(corpuses)
    voice = Speech("speech")

    ARCA.add_sensor(hearing)
    ARCA.add_interpreter(nlu)
    ARCA.add_interpreter(sr)
    ARCA.add_model(cbot)
    ARCA.add_actuator(voice)

    ARCA.associate(hearing, sr)
    ARCA.associate(sr, nlu)
    ARCA.associate(nlu, cbot)
    ARCA.associate(cbot, voice)

    ARCA.interpreters["sr"].listen()
    ARCA.interpreters["nlu"].listen()

    ARCA.sensors["mic_0"].on()

    while True:
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        ARCA.shutdown()
