from lib.sensors.sensor_base import Sensor
from lib.types import Percept
from typing import Callable
import speech_recognition as sr


class Audition(Sensor):
    def __init__(self, name: str, interpreter_name: str,
                 percept_callback: Callable[[Percept], None]):
        super().__init__(name, interpreter_name, percept_callback)

        self.r = sr.Recognizer()
        self.m = sr.Microphone()

        with self.m as source:
            (self.r).adjust_for_ambient_noise(source)

    def on(self):
        super().on()
        (self.r).listen_in_background(self.m, self.callback)

    def off(self):
        super().off()

    def callback(self, recognizer, audio):
        if self.status is True:
            try:
                data = recognizer.recognize_google(audio, language='es_PE')
                self.percept_callback(
                    Percept(self.name, self.interpreter_name, data))
            except (LookupError, sr.UnknownValueError):
                self.percept_callback(
                    Percept(self.name, self.interpreter_name, None))
            except sr.RequestError as e:
                print(f"Could not request results from GSR service: {e}")
        else:
            print("Status was OFF.")
            return
