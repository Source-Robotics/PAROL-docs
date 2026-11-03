# PAROL6 Programming Guide

<div class="doc-meta" markdown>

**Document number:** SR-4004

**PAROL6 release:** 1

**Python API (parol6):** v0.9.1

**PAROL6 commander software:** main

**Revision:** 2026.A (draft)

**Published:** —

**Applies to:** PAROL6 release 1, Python API (parol6) v0.9.1, PAROL6 commander software main

*Original instructions*

</div>

This guide is for everyone who makes PAROL6 do something: from a first RBTscript program in the commander
software to a Python application on the API, a ROS 2 pipeline, or a program that an AI agent writes. It starts
with the interfaces and how to choose, walks through the Python API and the commander software, and ends with
ROS 2 and the other interfaces. The ideas the software is built on, the units, the frames, the kinematics, the
configurations, the motion profiles, are in the [Theory corner](https://docs.source-robotics.com/PAROL-docs/1/theory/), a tab of their own. The [API reference](https://docs.source-robotics.com/PAROL-docs/1/reference/)
is where every method and command is listed, read from the API's source at the version named above.

<div class="grid cards" markdown>

-   :material-compass: **Start here**

    ---

    [The interfaces at a glance](https://docs.source-robotics.com/PAROL-docs/1/programming/01-interfaces/): which program for which job, and what they have in common.

-   :material-school: **Theory corner**

    ---

    [Units](https://docs.source-robotics.com/PAROL-docs/1/theory/units/), [joints and poses](https://docs.source-robotics.com/PAROL-docs/1/theory/joints-and-poses/),
    [frames](https://docs.source-robotics.com/PAROL-docs/1/theory/reference-frames/), [kinematics](https://docs.source-robotics.com/PAROL-docs/1/theory/kinematics/),
    [singularities](https://docs.source-robotics.com/PAROL-docs/1/theory/configurations-and-singularities/), [motion profiles](https://docs.source-robotics.com/PAROL-docs/1/theory/motion-profiles/),
    [blending](https://docs.source-robotics.com/PAROL-docs/1/theory/blending/), [control ownership](https://docs.source-robotics.com/PAROL-docs/1/theory/control-ownership/), and more.

-   :material-language-python: **The Python API**

    ---

    [Installation](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/installation/), [the controller](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/controller/),
    [clients](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/clients/), [motion](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/motion/), [jogging and servoing](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/streaming/),
    [tools](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/tools-and-tcp/), [status](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/status-and-waiting/), [errors](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/errors/),
    [examples](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/examples/).

-   :material-script-text: **RBTscript**

    ---

    [RBTscript](https://docs.source-robotics.com/PAROL-docs/1/programming/03-commander/rbtscript/), the commander software's program language, and [examples](https://docs.source-robotics.com/PAROL-docs/1/programming/03-commander/examples/);
    the commander itself is in the [GUI Guide](https://docs.source-robotics.com/PAROL-docs/1/gui/).

-   :material-robot: **ROS 2 and others**

    ---

    [ROS 2 and MoveIt](https://docs.source-robotics.com/PAROL-docs/1/programming/04-ros2/), [other interfaces](https://docs.source-robotics.com/PAROL-docs/1/programming/05-other-interfaces/): the serial protocol directly, the
    legacy API, AI agents.

-   :material-book-search: **API reference**

    ---

    [Every Python method](https://docs.source-robotics.com/PAROL-docs/1/reference/python/), [RBTscript](https://docs.source-robotics.com/PAROL-docs/1/reference/rbtscript/),
    [the serial protocol](https://docs.source-robotics.com/PAROL-docs/1/reference/serial-protocol/), [firmware parameters](https://docs.source-robotics.com/PAROL-docs/1/reference/firmware-parameters/).

</div>
