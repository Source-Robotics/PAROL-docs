---
hide:
  - toc
comments: false
---

# PAROL6 Robot Manual

![PAROL6 desktop robotic arm](assets/hero.webp){ .hero }

<!-- doc-meta: parol6 -->

[Quick start](quick-start.md){ .md-button .md-button--primary } [About this manual](about.md){ .md-button }

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
    <label class="arm-viewer__field">Printed parts <span class="arm-viewer__swatches" data-target="body"></span><input type="color" name="body" value="#c9c9c6" title="Any colour"></label>
    <button type="button" name="reset" class="md-button">Reset</button>
  </div>
  <p class="arm-viewer__hint">Drag to turn the robot, scroll to zoom, move each joint with its slider, try a colour for the printed parts. The model is the
robot's <a href="https://github.com/Source-Robotics/robot_descriptions/blob/main/guides/parol6.md">URDF</a>; the sliders run over its joint limits.</p>
</div>

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Quick start**

    ---

    [One page](quick-start.md) from an assembled robot to a homed one that moves: power, the commander software,
    the first jog, homing, with a link into the manual at every step.

-   :material-book-open-variant:{ .lg .middle } **The robot manual**

    ---

    [Safety](02-safety/index.md), [Technical data](03-technical-data/index.md), [Installation](04-installation/index.md),
    [Operation](05-operation/index.md), [Peripherals](06-peripherals/index.md), [Maintenance](07-maintenance/index.md),
    [Troubleshooting](08-troubleshooting/index.md).

-   :material-hammer-wrench:{ .lg .middle } **Build guide**

    ---

    [From the BOM to the first run](build/index.md): what to print and how, the parts to buy, the assembly manual
    and videos, the wiring, the firmware upload, the first power-on.

-   :material-chip:{ .lg .middle } **Control board**

    ---

    [The board that drives the robot](board/index.md): specifications, connectors and pinout, the stepper drivers,
    the I/O and E-stop wiring, CAN, firmware upload, the test firmware, the serial protocol.

-   :material-robot-industrial:{ .lg .middle } **End effectors**

    ---

    [What goes on the flange](end-effectors/index.md): the pneumatic and vacuum grippers, the [SSG-48](end-effectors/ssg-48.md)
    and [MSG](end-effectors/msg.md) electric grippers, your own tool; mounting, connections, the homing offset, driving them.

-   :material-monitor:{ .lg .middle } **GUI interfaces**

    ---

    [The graphical programs](gui/index.md): the commander software, Waldo Commander in the browser, Motor GUI
    for the grippers.

-   :material-code-braces:{ .lg .middle } **Programming**

    ---

    [The programming guide](programming/index.md): the interfaces, the concepts behind them, the Python API,
    RBTscript, ROS 2; and the [reference](reference/index.md), read from the API's source.

</div>
