from lib.sensors.sensor_base import Sensor
from lib.types import Percept, Status
from typing import Callable
from os import path
from pocketsphinx.pocketsphinx import Decoder
from pocketsphinx import get_model_path
import pyaudio


class Audition(Sensor):
    def __init__(self, name: str, interpreter_name: str,
                 percept_callback: Callable[[Percept], None]):
        super().__init__(name, interpreter_name, percept_callback,
                         self.perceiver)

        self.MODELDIR = get_model_path()
        self.CHUNK = 1024 * 4
        self.RATE = 44100
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1

        config = Decoder.default_config()

        config.set_string('-hmm', path.join(self.MODELDIR, 'es-es'))
        config.set_string('-lm', path.join(self.MODELDIR, 'es-es.lm'))
        config.set_string('-dict', path.join(self.MODELDIR, 'es.dict'))

        self.decoder = Decoder(config)

    def on(self):
        super().on()

    def off(self):
        super().off()

    def resume(self):
        super().resume()

    def pause(self):
        super().pause()

    def filter(self, buf):
        # TODO: Filter background noise
        return buf

    def perceiver(self):
        p = pyaudio.PyAudio()
        self.stream = p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            # output=True,
            frames_per_buffer=self.CHUNK)

        in_speech_bf = False

        self.stream.start_stream()

        print("PERCEIVER ON")
        self.decoder.start_utt()
        print("Started utterance")
        while True:
            buf = self.stream.read(self.CHUNK, exception_on_overflow=False)
            if self.status == Status.PAUSED:
                continue
            elif self.status == Status.STOPPED:
                break

            # self.stream.write(buf, self.CHUNK)
            print(self.decoder.get_in_speech())
            if buf:
                buf = self.filter(buf)
                self.decoder.process_raw(buf, False, False)
                if self.decoder.get_in_speech() != in_speech_bf:
                    in_speech_bf = self.decoder.get_in_speech()
                    if not in_speech_bf:
                        self.pause()

                        self.decoder.end_utt()

                        if self.decoder.hyp() is not None:
                            data = self.decoder.hyp().hypstr
                            if data == "":
                                data = None
                            print(f'Result: {data}')
                            self.percept_callback(
                                Percept(self.name, self.interpreter_name,
                                        data))
                        self.decoder.start_utt()
            else:
                break
        self.decoder.end_utt()
