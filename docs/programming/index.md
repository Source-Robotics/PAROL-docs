---
hide:
  - toc
---

# PAROL6 Programming Guide

<!-- doc-meta: programming -->

This guide is for everyone who makes PAROL6 do something: from a first RBTscript program in the commander
software to a Python application on the API, a ROS 2 pipeline, or a program that an AI agent writes. It starts
with the interfaces and how to choose, walks through the Python API and the commander software, and ends with
ROS 2 and the other interfaces. The ideas the software is built on, the units, the frames, the kinematics, the
configurations, the motion profiles, are in the [Theory corner](../theory/index.md), a tab of their own. The [API reference](../reference/index.md)
is where every method and command is listed, read from the API's source at the version named above.

<div class="grid cards" markdown>

-   :material-compass:{ .lg .middle } **Start here**

    ---

    [The interfaces at a glance](01-interfaces.md): which program for which job, and what they have in common.

-   :material-school:{ .lg .middle } **Theory corner**

    ---

    [Units](../theory/units.md), [joints and poses](../theory/joints-and-poses.md),
    [frames](../theory/reference-frames.md), [kinematics](../theory/kinematics.md),
    [singularities](../theory/configurations-and-singularities.md), [motion profiles](../theory/motion-profiles.md),
    [blending](../theory/blending.md), [control ownership](../theory/control-ownership.md), and more.

-   :material-language-python:{ .lg .middle } **The Python API**

    ---

    [Installation](02-python-api/installation.md), [the controller](02-python-api/controller.md),
    [clients](02-python-api/clients.md), [motion](02-python-api/motion.md), [jogging and servoing](02-python-api/streaming.md),
    [tools](02-python-api/tools-and-tcp.md), [status](02-python-api/status-and-waiting.md), [errors](02-python-api/errors.md),
    [examples](02-python-api/examples.md).

-   :material-script-text:{ .lg .middle } **RBTscript**

    ---

    [RBTscript](03-commander/rbtscript.md), the commander software's program language, and [examples](03-commander/examples.md);
    the commander itself is in the [GUI Guide](../gui/index.md).

-   :material-robot:{ .lg .middle } **ROS 2 and others**

    ---

    [ROS 2 and MoveIt](04-ros2.md), [other interfaces](05-other-interfaces.md): the serial protocol directly, the
    legacy API, AI agents.

-   :material-book-search:{ .lg .middle } **API reference**

    ---

    [Every Python method](../reference/python/index.md), [RBTscript](../reference/rbtscript.md),
    [the serial protocol](../reference/serial-protocol.md), [firmware parameters](../reference/firmware-parameters.md).

</div>
