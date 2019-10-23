import os
import numpy as np
import logging
import datetime


def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_date():
    return str(datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S"))


def bytes_to_np(bytes_signal):
    return np.frombuffer(bytes_signal, dtype=np.int16)


def np_to_bytes(np_signal):
    return np_signal.tobytes()


def get_logger(name: str, filename: str):
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M',
        filename=filename,
        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logging.info('Jackdaws love my big sphinx of quartz.')

    return logging.getLogger(name)
