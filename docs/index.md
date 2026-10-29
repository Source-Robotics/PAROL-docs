---
hide:
  - toc
---

# PAROL6 Robot Manual

![PAROL6 desktop robotic arm](assets/hero.png){ .hero }

<!-- doc-meta: parol6 -->

[Quick start](quick-start.md){ .md-button .md-button--primary } [About this manual](about.md){ .md-button }

Source Robotics d.o.o. publishes this document as part of the open-source PAROL6 project. It is revised as the
product changes; the document number, release, revision and date above identify the version you are reading, and
the document history on the About page says what changed. Take care that the release named under *Applies to*
matches the robot in front of you, and that the Python API version matches what `pip` installed: the version
selector in the header switches between releases. The text and the images are licensed CC BY-SA 4.0, the code
examples MIT.

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Quick start**

    ---

    [One page](quick-start.md) from an assembled robot to a homed one that moves: power, the commander software,
    the first jog, homing, with a link into the manual at every step.

-   :material-book-open-variant:{ .lg .middle } **The robot manual**

    ---

    [Safety](02-safety/index.md), [Technical data](03-technical-data/index.md), [Installation](04-installation/index.md),
    [Operation](05-operation/index.md), [Tools and grippers](06-tools/index.md), [Peripherals](07-peripherals/index.md),
    [Maintenance](08-maintenance/index.md), [Troubleshooting](09-troubleshooting/index.md).

-   :material-hammer-wrench:{ .lg .middle } **Build guide**

    ---

    [From the BOM to the first run](build/index.md): what to print and how, the parts to buy, the assembly manual
    and videos, the wiring, the firmware upload, the first power-on.

-   :material-chip:{ .lg .middle } **Control board**

    ---

    [The board that drives the robot](board/index.md): specifications, connectors and pinout, the stepper drivers,
    the I/O and E-stop wiring, CAN, firmware upload, the test firmware, the serial protocol.

-   :material-code-braces:{ .lg .middle } **Programming**

    ---

    [The programming guide](programming/index.md): the interfaces, the concepts behind them, the Python API, the
    commander software and RBTscript, ROS 2; and the [API reference](reference/index.md), read from the API's source.

-   :material-robot-industrial:{ .lg .middle } **Grippers**

    ---

    The [SSG-48](https://docs.source-robotics.com/SSG48-gripper-docs/) and [MSG](https://docs.source-robotics.com/MSG-gripper-docs/)
    electric grippers have their own manuals; [this manual](06-tools/electric-grippers.md) says how they attach to
    PAROL6 and how the robot drives them.

</div>
