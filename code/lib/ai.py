from lib.types import Action, Percept
from lib.actuators.actuator_base import Actuator
from lib.sensors.sensor_base import Sensor
from lib.interpreters.interpreter_base import Interpreter
from lib.models.model_base import Model
from lib.types import Percept, Interpretation, Action
from typing import Dict
import time


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
        # Commments:
        # - Percept callback shouldn't have control over all the functionality of the Agent

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
