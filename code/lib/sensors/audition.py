from lib.sensors.sensor_base import Sensor
from lib.types import Status, Identifier
from typing import List
import pyaudio


class Audition(Sensor):
    def __init__(self, name: str):
        super().__init__(name, self.perceiver)

        self.CHUNK = 1024 * 4
        self.RATE = 48000
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1

    def get_destinations_ID(self, raw_data) -> List[Identifier]:
        return [self.destinations_ID[0]]

    def pass_msg(self, msg: str) -> None:
        if msg == "PAUSE":
            self.pause()
        elif msg == "RESUME":
            self.resume()
        else:
            raise Exception("Unrecognized message.")

    def perceiver(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK)

        stream.start_stream()

        while True:
            if self.status == Status.STOPPED:
                break
            self.wait_event.wait()

            data = stream.read(self.CHUNK, exception_on_overflow=False)

            if data != b'':
                self.send(data)

        stream.stop_stream()
        stream.close()
        p.terminate()
