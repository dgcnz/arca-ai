from lib.types import Percept, Interpretation, Action
from lib.sensors.sensor_base import Sensor
from lib.interpreters.interpreter_base import Interpreter
from lib.models.model_base import Model
from lib.actuators.actuator_base import Actuator
from typing import Dict, List


class Agent:
    """Class to generalize Agents.

    Keyword arguments:
    name -- name of the agent
    is_on -- true if Agent is listening in background (default false)
    actuators -- dict of instances of subclasses of the Actuator class.
    sensors -- dict of instances of subclasses of the Sensor class.
    interpreters -- dict of instances of subclasses of the Interpreter class.
    models -- dict of instances of subclasses of the Model class.
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

    def add_interpreter(self, i: Interpreter) -> None:
        self.interpreters[i.name] = i

    def add_model(self, m: Model) -> None:
        self.models[m.name] = m

    def add_actuator(self, a: Actuator) -> None:
        self.actuators[a.name] = a

    def list_sensors(self) -> None:
        for s_name, sensor in self.sensors.items():
            print(f"{s_name}: {'ON' if sensor.status is True else 'OFF'}")

    def list_interpreters(self) -> None:
        for i_name, interpreter in self.interpreters.items():
            print(f"{i_name}")

    def list_models(self) -> None:
        for m_name, model in self.models.items():
            print(f"{m_name}: {model.kind}")

    def list_actuators(self) -> None:
        for a_name, actuator in self.actuators.items():
            print(f"{a_name}")

    def list_all(self) -> None:
        self.list_sensors()
        self.list_interpreters()
        self.list_models()
        self.list_actuators()

    def update_state(self, percept: Percept):
        pass

    def decide(self, ir: Interpretation) -> Action:
        return self.models[ir.model_name].decide(ir)

    def interpret(self, percept: Percept) -> Interpretation:
        return self.interpreters[percept.interpreter_name].interpret(percept)

    def percept_callback(self, percept: Percept):
        # Commments:
        # - Percept callback shouldn't have control over all the functionality
        #   of the Agent
        if percept.data is None:
            print("Empty percept.")
            return

        print(f"PERCEPT: {percept.sensor_name} -> {percept.data}")
        ir: Interpretation = self.interpret(percept)

        # internal representation taken by rule-based or reasoning thinking
        actions: List[Action] = self.decide(ir)

        for action in actions:
            print(f"ACTION: {action.actuator_name} -> {action.data}")
            self.actuators[action.actuator_name].do(action)
