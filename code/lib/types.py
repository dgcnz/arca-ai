class Percept:
    def __init__(self, sensor_name: str, interpreter_name: str, data):
        self.sensor_name = sensor_name
        self.interpreter_name = interpreter_name
        self.data = data


class Interpretation:
    def __init__(self, kind: str, data):
        self.kind = kind
        self.data = data


class Action:
    def __init__(self, actuator_name: str, data):
        self.actuator_name = actuator_name
        self.data = data
