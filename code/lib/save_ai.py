from typing import Callable, Dict
import speech_recognition as sr
import time

# from os import system


class Interpretation:
    def __init__(self, kind: str, data):
        self.kind = kind
        self.data = data


class Intrepreter:
    def __init__(self, name: str):
        self.name = name


class NLU:
    def __init__(self, name: str):
        super().__init__(name)


class Percept:
    def __init__(self, sensor_name: str, interpreter_name: str, data):
        self.sensor_name = sensor_name
        self.interpreter_name = interpreter_name
        self.data = data


class Action:
    def __init__(self, actuator_name: str, data):
        self.actuator_name = actuator_name
        self.data = data


class Actuator:
    def __init__(self, name):
        self.name = name

    def do(self, action: Action):
        pass


class Sensor:
    def __init__(self, name: str, interpreter_name: str,
                 percept_callback: Callable[[Percept], None]):
        self.name: str = name
        self.interpreter_name: str = interpreter_name
        self.status: bool = False
        self.percept_callback = percept_callback

    def on(self):
        self.status = True
        print(f"{self.name} sensor is on.")

    def off(self):
        self.status = False
        print(f"{self.name} sensor is off.")


class Speech(Actuator):
    def __init__(self, name: str):
        super().__init__(name)

    def do(self, action: Action):
        pass


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
            print("status was OFF.")
            return


class Agent:
    """Class to generalize Agents.

    Keyword arguments:
    name -- name of the agent
    is_on -- true if Agent is listening in background (default false)
    actuators -- dict of instances of subclasses of the Actuator class.
    sensors -- dict of instances of subclasses of the Sensor class.
    """

    name: str = ""
    is_on: bool = False
    actuators: Dict[str, Actuator] = {}
    sensors: Dict[str, Sensor] = {}
    interpreters: Dict[str, Interpreter] = {}
    models: Dict[str, Model] = {}

    def __init__(self, name: str):
        self.name = name

    def add_sensor(self, s: Sensor) -> None:
        self.sensors[s.name] = s

    def list_sensors(self) -> None:
        for s_name, sensor in self.sensors.items():
            print(f"{s_name}: {'ON' if sensor.status is True else 'OFF'}")

    def update_state(self, percept: Percept):
        pass

    def decide(self, ir: Interpretation) -> Action:
        return self.models[ir.kind].decide(ir)

    def interpret(self, percept: Percept) -> Interpretation:
        pass

    def percept_callback(self, percept: Percept):
        print(f"PERCEPT: {percept.sensor_name} -> {percept.data}")
        ir = self.interpret(percept)

        # internal representation taken by rule-based or reasoning thinking
        a: Action = self.decide(ir)

        action = self.decide(percept)

        print(f"ACTION: {action.actuator_name} -> {action.data}")

        self.actuators[action.actuator_name].do(action)


if __name__ == "__main__":
    ARCA = Agent("ARCA")
    nlu = NLU("nlu")
    hearing = Audition("mic_0", "nlu", ARCA.percept_callback)
    ARCA.add_sensor(hearing)
    ARCA.sensors["mic_0"].on()
    ARCA.list_sensors()
    while True:
        time.sleep(0.1)
