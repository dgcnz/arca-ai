from enum import Enum, auto


class Status(Enum):
    RUNNING = auto()
    PAUSED = auto()
    STOPPED = auto()


class Percept:
    def __init__(self, sensor_name: str, interpreter_name: str, data):
        self.sensor_name = sensor_name
        self.interpreter_name = interpreter_name
        self.data = data


class Interpretation:
    def __init__(self, interpreter_name: str, model_name: str, kind: str,
                 data):
        self.interpreter_name = interpreter_name
        self.model_name = model_name
        self.kind = kind
        self.data = data


class Action:
    def __init__(self, actuator_name: str, data):
        self.actuator_name = actuator_name
        self.data = data
