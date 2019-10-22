from lib.types import Entity, Information, Identifier, NestedDefaultDict
from lib.sensors.sensor_base import Sensor
from lib.interpreters.interpreter_base import Interpreter
from lib.models.model_base import Model
from lib.actuators.actuator_base import Actuator
from lib.observers.observer_base import Subject, Observer
from typing import Dict, List, Union, Optional
from lib.utilities.helpers import create_path
import logging
import datetime
import pprint
pp = pprint.PrettyPrinter(indent=4)


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
    history = NestedDefaultDict()

    def __init__(self, name: str):
        self.name = name

    def shutdown(self):
        print(f"Shutting down {self.name}")
        self.dump_history()
        for s_name, sensor in self.sensors.items():
            sensor.off()
        print(f"Done.")

    def add_entity(self, e: Entity) -> None:
        fwdlist = {
            "Sensor": self.sensors,
            "Interpreter": self.interpreters,
            "Model": self.models,
            "Actuator": self.actuators
        }
        print(f"Adding entity {e.dumpID().category}:{e.dumpID().name}.")
        fwdlist[e.dumpID().category][e.dumpID().name] = e

    def attach_observer(self, observer: Observer) -> None:
        self.observers.append(observer)

    def detach_observer(self, observer: Observer) -> None:
        self.observers.remove(observer)

    def notify_observers(self, keyword: str) -> None:
        for obs in self.observers:
            obs.update(self, keyword)

    def sendID(self,
               msg: Union[Information, str],
               rcv: Optional[Entity] = None) -> None:
        """
        Callback function that is executed in an Entity to pass a msg (can be Information or just a string) to another Entity.

        Args:
            msg (Union[Information, str]): message can be a Percept, Interpretation, Action or string.
            rcv (Optional[Entity]): receiver might be optional, since Information already contains such data.

        Returns:
            None
        """

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
            self.history[msg.src.category][msg.src.name][msg.dest.category][
                msg.dest.name].append(msg.data)
        elif isinstance(msg, str):
            if rcv is None:
                raise Exception(
                    "If message is a string, a receiver must be specified.")
            print(f"MESSAGE {msg} was passed to {rcv.name}.")
            fwdlist[rcv.category][rcv.name].pass_msg(msg)

    def status(self):
        pp.pprint(self.history)

    def associate(self, src: Entity, dest: Entity) -> None:
        """
        Adds dest destination to src Entity and defines src's sendID() with Agent's sendID().
        """
        print(
            f"{self.name} >> Associating {src.dumpID().category}:{src.dumpID().name} with {dest.dumpID().category}:{dest.dumpID().name}"
        )
        src.add_destination_ID(dest.dumpID())
        src.sendID = self.sendID
        self.history[src.dumpID().category][src.dumpID().name][
            dest.dumpID().category][dest.dumpID().name] = []

    def dump_history(self):
        fwdlist = {
            "Sensor": self.sensors,
            "Interpreter": self.interpreters,
            "Model": self.models,
            "Actuator": self.actuators
        }
        for src_cat, src_catv in self.history.items():
            for src_name, src_namev in src_catv.items():
                for dest_cat, dest_catv in src_namev.items():
                    for dest_name, data in dest_catv.items():
                        path = f"logs/{src_cat}/{src_name}/{dest_cat}/{dest_name}"
                        create_path(path)
                        timestamp = str(datetime.datetime.now().strftime(
                            "%y-%m-%d-%H-%M-%S"))
                        fwdlist[src_cat][src_name].dump_history(
                            f"{path}/{timestamp}", data)
