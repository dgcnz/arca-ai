from lib.types import Percept, Interpretation, Action, Entity, Information
from lib.sensors.sensor_base import Sensor
from lib.interpreters.interpreter_base import Interpreter
from lib.models.model_base import Model
from lib.actuators.actuator_base import Actuator
from lib.observers.observer_base import Subject, Observer
from typing import Dict, List, Union, Optional


class Agent(Subject):
    """Class to generalize Agents.

    Keyword arguments:
    name -- name of the agent
    actuators -- dict of instances of subclasses of the Actuator class.
    sensors -- dict of instances of subclasses of the Sensor class.
    interpreters -- dict of instances of subclasses of the Interpreter class.
    models -- dict of instances of subclasses of the Model class.
    """

    name: str = ""
    actuators: Dict[str, Actuator] = {}
    sensors: Dict[str, Sensor] = {}
    interpreters: Dict[str, Interpreter] = {}
    models: Dict[str, Model] = {}
    observers: List[Observer] = []

    def __init__(self, name: str):
        self.name = name

    def shutdown(self):
        print(f"Shutting down {self.name}")
        for s_name, sensor in self.sensors.items():
            sensor.off()
        print(f"Done.")

    def add_sensor(self, s: Sensor) -> None:
        self.sensors[s.name] = s

    def add_interpreter(self, i: Interpreter) -> None:
        self.interpreters[i.name] = i

    def add_model(self, m: Model) -> None:
        self.models[m.name] = m

    def add_actuator(self, a: Actuator) -> None:
        self.actuators[a.name] = a

    def attach_observer(self, observer: Observer) -> None:
        self.observers.append(observer)

    def detach_observer(self, observer: Observer) -> None:
        self.observers.remove(observer)

    def notify_observers(self, keyword: str) -> None:
        for obs in self.observers:
            obs.update(self, keyword)

    def sendID(self,
               msg: Union[Information, str],
               rcv: Optional[Entity] = None):

        fwdlist = {
            "Sensor": self.sensors,
            "Interpreter": self.interpreters,
            "Model": self.models,
            "Actuator": self.actuators
        }
        if isinstance(msg, Information):
            print(
                f"Information is passed from {msg.src.name} to {msg.dest.name}."
            )
            fwdlist[msg.dest.category][msg.dest.name].put(msg)
        elif isinstance(msg, str):
            if rcv is None:
                raise Exception(
                    "If message is a string, a receiver must be specified.")
            print(f"MESSAGE {msg} was passed to {rcv.name}.")
            fwdlist[rcv.category][rcv.name].pass_msg(msg)

    def associate(self, src: Entity, dest: Entity):
        print(f"{self.name} >> Associating {src.dumpID().category}:{src.dumpID().name} with {dest.dumpID().category}:{dest.dumpID().name}")
        src.add_destination_ID(dest.dumpID())
        src.sendID = self.sendID
