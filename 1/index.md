# PAROL6 Robot Manual

![PAROL6 desktop robotic arm](https://docs.source-robotics.com/PAROL-docs/1/assets/hero.webp)

<div class="doc-meta" markdown>

**Document number:** SR-1002

**PAROL6 release:** 1

**Python API (parol6):** v0.9.1

**PAROL6 commander software:** main

**Revision:** 2026.A

**Published:** 2026-11-03

**Applies to:** PAROL6 with the PAROL6 control board v2.0, PAROL6 release 1, Python API (parol6) v0.9.1, PAROL6 commander software main

*Original instructions*

</div>

[Quick start](https://docs.source-robotics.com/PAROL-docs/1/quick-start/) [About this manual](https://docs.source-robotics.com/PAROL-docs/1/about/)

Source Robotics d.o.o. publishes this document as part of the open-source PAROL6 project. It is revised as the
product changes; the document number, release, revision and date above identify the version you are reading, and
the document history on the About page says what changed. Take care that the release named under *Applies to*
matches the robot in front of you, and that the Python API version matches what `pip` installed: the version
selector in the header switches between releases. The text and the images are licensed CC BY-SA 4.0, the code
examples MIT.

<div class="arm-viewer" data-base="assets/models/parol6/" markdown="0">
  <canvas class="arm-viewer__canvas" aria-label="PAROL6 in 3D: drag to turn, scroll to zoom"></canvas>
  <div class="arm-viewer__controls">
    <div class="arm-viewer__joints"></div>
    <label class="arm-viewer__field">Gripper <select name="tool"></select></label>
    <label class="arm-viewer__field">Printed parts <span class="arm-viewer__swatches" data-target="body"></span><input type="color" name="body" value="#c9c9c6" title="Any colour"></label>
    <button type="button" name="reset" class="md-button">Reset</button>
  </div>
  <p class="arm-viewer__hint">Drag to turn the robot, scroll to zoom, move each joint with its slider, choose the gripper on the flange, try a
colour for the printed parts (the motors stay black). The model is the robot's
<a href="https://github.com/Source-Robotics/robot_descriptions/blob/main/guides/parol6.md">URDF</a>; the sliders run over its joint limits.</p>
</div>

<div class="grid cards" markdown>

-   :material-rocket-launch: **Quick start**

    ---

    [One page](https://docs.source-robotics.com/PAROL-docs/1/quick-start/) from an assembled robot to a homed one that moves: power, the commander software,
    the first jog, homing, with a link into the manual at every step.

-   :material-book-open-variant: **The robot manual**

    ---

    [Safety](https://docs.source-robotics.com/PAROL-docs/1/02-safety/), [Technical data](https://docs.source-robotics.com/PAROL-docs/1/03-technical-data/), [Installation](https://docs.source-robotics.com/PAROL-docs/1/04-installation/),
    [Operation](https://docs.source-robotics.com/PAROL-docs/1/05-operation/), [Peripherals](https://docs.source-robotics.com/PAROL-docs/1/06-peripherals/), [Maintenance](https://docs.source-robotics.com/PAROL-docs/1/07-maintenance/),
    [Troubleshooting](https://docs.source-robotics.com/PAROL-docs/1/08-troubleshooting/).

-   :material-hammer-wrench: **Build guide**

    ---

    [From the BOM to the first run](https://docs.source-robotics.com/PAROL-docs/1/build/): what to print and how, the parts to buy, the assembly manual
    and videos, the wiring, the firmware upload, the first power-on.

-   :material-chip: **Control board**

    ---

    [The board that drives the robot](https://docs.source-robotics.com/PAROL-docs/1/board/): specifications, connectors and pinout, the stepper drivers,
    the I/O and E-stop wiring, CAN, firmware upload, the test firmware, the serial protocol.

-   :material-robot-industrial: **End effectors**

    ---

    [What goes on the flange](https://docs.source-robotics.com/PAROL-docs/1/end-effectors/): the pneumatic and vacuum grippers, the [SSG-48](https://docs.source-robotics.com/PAROL-docs/1/end-effectors/ssg-48/)
    and [MSG](https://docs.source-robotics.com/PAROL-docs/1/end-effectors/msg/) electric grippers, your own tool; mounting, connections, the homing offset, driving them.

-   :material-monitor: **GUI interfaces**

    ---

    [The graphical programs](https://docs.source-robotics.com/PAROL-docs/1/gui/): the commander software, Waldo Commander in the browser, Motor GUI
    for the grippers.

-   :material-code-braces: **Programming**

    ---

    [The programming guide](https://docs.source-robotics.com/PAROL-docs/1/programming/): the interfaces, the concepts behind them, the Python API,
    RBTscript, ROS 2; and the [reference](https://docs.source-robotics.com/PAROL-docs/1/reference/), read from the API's source.

</div>
