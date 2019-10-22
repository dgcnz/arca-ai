import os
import numpy as np


def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def bytes_to_np(bytes_signal):
    return np.frombuffer(bytes_signal, dtype=np.int16)


def np_to_bytes(np_signal):
    return np_signal.tobytes()
