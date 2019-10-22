from lib.sensors.sensor_base import Sensor
from lib.types import Identifier
from lib.utilities.helpers import bytes_to_np, np_to_bytes
from typing import List, Any
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
        self.SILENCE_SEC = 0.5
        self.is_noise = True
        self.BIAS = 500

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
        print("Calculating rms' from noise.")
        stream, p = self.get_stream()
        values = []
        num_samples = int(self.RATE / self.CHUNK * seconds)

        
        for i in range(num_samples):
            rms = audioop.rms(stream.read(self.CHUNK), self.WIDTH)
            values.append(rms)
            print(f"RMS: {rms:<5}")

        values = sorted(values, reverse=True)
        self.THRESHOLD = sum(values[:int(num_samples * 0.2)]) / int(
            num_samples * 0.2) + self.BIAS

        print(f"Threshold set at {self.THRESHOLD}")
        stream.close()
        p.terminate()

    def get_stream(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        return stream, p

    def read_input(self) -> Any:
        """
        Reads a self.CHUNK from self.stream and returns it.

        Returns:
           Any: data or None
        """
        data = self.__stream.read(self.CHUNK, exception_on_overflow=False)
        data_np = bytes_to_np(data)
        data_np = np_to_bytes(np.sort(data_np)[-int(0.2 * data_np.size):])
        rms = audioop.rms(data_np, self.WIDTH)
        if data != b'' and rms >= self.THRESHOLD:
            print(
                f"RMS Sorted: {rms}\t threshold: {self.THRESHOLD}\t is_valid: True"
            )
            self.SILENCE_FRAMES = 0
            self.is_noise = False
            return data
        else:
            print(
                f"RMS Sorted: {rms}\t threshold: {self.THRESHOLD}\t is_valid: False"
            )
            if not self.is_noise:
                self.SILENCE_FRAMES += 1
                if (self.SILENCE_FRAMES * self.CHUNK /
                        self.RATE) >= self.SILENCE_SEC:
                    self.is_noise = True
                    return bytes([0] * self.CHUNK * 5)
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
        with wave.open(f"{filename}.wav", "wb") as waveFile:
            waveFile.setnchannels(self.CHANNELS)
            waveFile.setsampwidth(self.WIDTH)
            waveFile.setframerate(self.RATE)
            waveFile.writeframes(b''.join(data))
