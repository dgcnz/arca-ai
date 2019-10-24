from lib.sensors.sensor_base import Sensor
from lib.types import Identifier
from lib.utilities.helpers import bytes_to_np, np_to_bytes, get_logger, get_date
from typing import List, Any
from collections import deque
import numpy as np
import pyaudio
import audioop
import wave


class Audition(Sensor):
    def __init__(self, name: str):
        super().__init__(name, True)

        self.CHUNK = 1024 * 4
        self.RATE = 48000
        self.WIDTH = 2
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.SILENCE_FRAMES = 0
        self.SILENCE_SEC = 1.5
        self.IS_NOISE = True
        self.BIAS = 300
        self.past_window = deque(maxlen=int(self.SILENCE_SEC * self.RATE /
                                            self.CHUNK))
        name, cat = self.dumpID().to_tuple()
        self.logger = get_logger(f"{cat}.{name}",
                                 f"logs/{cat}/{name}/{get_date()}")

    def get_destinations_ID(self, raw_data) -> List[Identifier]:
        return [self.destinations_ID[0]]

    def pass_msg(self, msg: str) -> None:
        if msg == "PAUSE":
            self.pause()
        elif msg == "RESUME":
            self.resume()
        else:
            raise Exception("Unrecognized message.")

    def setup_mic(self, seconds=2):
        self.logger.info(
            "Setting up Microphone THRESHOLD. Please say something to adjust its sensitivity."
        )
        stream, p = self.get_stream()
        values = []
        num_samples = int(self.RATE / self.CHUNK * seconds)

        input("Press Enter when ready.")

        for i in range(num_samples):
            rms = audioop.rms(
                stream.read(self.CHUNK, exception_on_overflow=False),
                self.WIDTH)
            values.append(rms)
            self.logger.info(f"RMS: {rms:<5}")

        values = sorted(values, reverse=True)
        self.THRESHOLD = sum(values[:int(num_samples * 0.2)]) / int(
            num_samples * 0.2) - self.BIAS

        self.logger.info(f"Threshold set at {self.THRESHOLD}.")
        stream.close()
        p.terminate()

    def get_stream(self):
        """
        Helper function to open a pyaudio stream.

        Returns:
            stream: instance of pyaudio.Pyaudio.open()
            p: instance of pyaudio.Pyaudio
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        return stream, p

    def read_input(self) -> Any:
        """
        Reads a self.CHUNK from self.stream and returns it if its rms
        is over self.THRESHOLD. It will maintain self.past_window, a collection
        of the past chunks, and it will append it to the start of the first
        relevant data it encounters. After relevant data, self.IS_NOISE will
        still be True and data will be sent normally, but after
        self.SILENCE_SEC seconds it will send a chunk of empty data and set
        self.IS_NOISE to True. A chunck of audio is relevant if its rms exceeds
        the self.THRESHOLD.


        Returns:
           Any: data or None
        """

        # Reads from pyaudio.stream
        data = self.__stream.read(self.CHUNK, exception_on_overflow=False)
        # Takes 0.2 biggest values
        data_np = bytes_to_np(data)
        data_np = np_to_bytes(np.sort(data_np)[-int(0.2 * data_np.size):])
        # Calculates rms of sorted and sliced bytearray
        rms = audioop.rms(data_np, self.WIDTH)

        if data != b'' and rms >= self.THRESHOLD:
            self.logger.info(
                f"RMS Sorted: {rms}\t threshold: {self.THRESHOLD}\t is_valid: True"
            )
            self.SILENCE_FRAMES = 0

            if self.IS_NOISE:
                past = b''.join(self.past_window)
                self.past_window.clear()
                data = past + data

            self.IS_NOISE = False
            return data
        else:
            self.logger.info(
                f"RMS Sorted: {rms}\t threshold: {self.THRESHOLD}\t is_valid: False"
            )

            self.past_window.append(data)
            if not self.IS_NOISE:
                self.SILENCE_FRAMES += 1
                if (self.SILENCE_FRAMES * self.CHUNK /
                        self.RATE) >= self.SILENCE_SEC:
                    self.IS_NOISE = True
                    return bytes([0] * self.CHUNK * 4)
                return data
            return None

    def setup_perceiver(self) -> None:
        self.setup_mic()
        self.__stream, self.__p = self.get_stream()

    def close_perceiver(self) -> None:
        self.__stream.stop_stream()
        self.__stream.close()
        self.__p.terminate()

    def dump_history(self, filename: str, data: List[Any]) -> None:
        self.logger.info(f"Dumping history into {filename}.wav.")
        with wave.open(f"{filename}.wav", "wb") as waveFile:
            waveFile.setnchannels(self.CHANNELS)
            waveFile.setsampwidth(self.WIDTH)
            waveFile.setframerate(self.RATE)
            waveFile.writeframes(b''.join(data))
