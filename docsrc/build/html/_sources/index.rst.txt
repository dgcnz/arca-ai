.. ARCA documentation master file, created by
   sphinx-quickstart on Thu Oct 24 06:07:03 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


An Overview
================================

One of the main objectives of this project was to devise a way to organize and segment the code such that it made sense 1) *conceptually* and 2) *programatically*.

For the first condition, such architecture was and had to be inspired by what we knew or the intuition we had from the workings of the brain. We're not claiming, by any means, that such an ambition was reached, but that it exercised the thought of this matter.

For the latter, it had to be implementable, obviously, but also maintainable and even efficient. Threading, Events, Message Passing and other techniques were used to achieve these goals in a modular fashion. Class Inheritance allowed the immediate interfaces (i.e. the Audition sensor) to be fairly simple and restrained to their unique properties while hiding the aforementioned details (Threading, etc.) in the parent classes (i.e. the Sensor base class). On top of that, the Agent class encompassed a collection of Sensors, Interpreters, Models and Actuators (we'll call the Components) and allowed non-redundant and centralized message passing between them (this aided debugging too).

In the following picture, the path of Information is shown.

.. image:: ../figures/infopath.png

The basic idea is that Sensors read Percepts from the external world (via hardware) and pass them to the Interpreters so that they can transform them into something that is "usable". Sensors should not make any preprocessing or complex decisions about the raw data. Interpreters, on the other hand, have to receive Percepts (or Interpretations) continuously, decide when such sequence is a relevant unit of perception, process it and send it to another Interpreter if it still needs to be decoded or to a Model if it's ready to be transformed to an Action. Models take Interpretations and decide what to do with such information, returning if necessary a sequence of Actions.


.. toctree::
   :maxdepth: 2
   :caption: Contents:


Agent
===================

The Agent class serves to englobe, centralize and simplify inter-component communication to ensure its validity. It also provides a comprehensive and unified interface that Observers can use to query and interact with Agent's components and Developers can use to easily set up a component network for their AI.

.. automodule:: lib.ai
   :members:



Types
===================

An `Entity` is a class that defines the general behavior of Sensors, Interpreters, Models and Actuators. It implements two simple methods (`add_destination_ID()` and `dumpID()`), defines an abstract function `dump_history()` and "declares" three variables (`name`, `destinations_ID`, `sendID`). 

.. automodule:: lib.types
   :members:




Sensor
===================
.. automodule:: lib.sensors.sensor_base
   :members:

Interpreter
===================
.. automodule:: lib.interpreters.interpreter_base
   :members:

Model
===================
.. automodule:: lib.models.model_base
   :members:

Actuator
===================
.. automodule:: lib.actuators.actuator_base
   :members:

Audition Sensor
===================
.. automodule:: lib.sensors.audition
   :members:

Speech Recognizer Interpreter
===================
.. automodule:: lib.interpreters.speech_recognizer
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
