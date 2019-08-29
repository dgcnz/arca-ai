import time
import random
import pyttsx3
import speech_recognition as sr
from threading import Thread
from subprocess import call

# engine = pyttsx3.init()
# """
# Voice:
#  - ID: com.apple.speech.synthesis.voice.monica
#  - Name: Monica
#  - Languages: ['es_ES']
#  - Gender: VoiceGenderFemale
#  - Age: 35
# """
#
# ES_VOICE_ID = "com.apple.speech.synthesis.voice.monica"
# engine.setProperty('voice', ES_VOICE_ID)

r = sr.Recognizer()
m = sr.Microphone()

with m as source:
    r.adjust_for_ambient_noise(
        source)  # we only need to calibrate once, before we start listening


class Speaker:
    """
    Class for handling ARCA's speech.
    @params:
        - name: str = Name of the Speaker.
    """

    # TODO: generic Speaker, pass engines as parameters.

    def __init__(self, name):
        """
        ARCA could have a activate method or a listen on command method.
        """
        self.name = name
        r.listen_in_background(m, self.callback)

    def callback(self, recognizer, audio):
        try:
            msg = recognizer.recognize_google(audio, language='es_PE')
            print(f">> {msg}")
            self.answer(msg)
        except (LookupError, sr.UnknownValueError):
            self.fallback()
        except sr.RequestError as e:
            print(
                f"Could not request results from Google Speech Recognition service; {e}"
            )

    def fallback(self):
        fb_msgs = [
            "Disculpe, no entendí.", "¿Podría repetirlo?",
            "No entendí, ¿podría hablar más claro?"
        ]
        msg = random.choice(fb_msgs)
        self.say(msg)

    def answer(self, msg: str):
        """
        Process msg and provides answer. Calls say(ans).
        """
        ans: str = msg  # TODO: process text
        self.say(ans)

    def say(self, msg: str):
        # engine.say(msg)
        # engine.runAndWait()

        call(["python", "speak.py", msg])


def main():

    ARCA = Speaker(name="arca")

    while (True):
        time.sleep(1)


if __name__ == "__main__":
    main()
