# Quick start

From the PAROL6 you have built to one that is homed and moves on command, on one page. It begins where the
[Build guide](build/index.md) ends: the robot assembled and wired, the control board in the base with the main
firmware on it. Every step ends with a link to the chapter that explains it. Follow the link when a step is not
clear or something fails.

!!! danger "Read first"
    PAROL6 has no brakes: when the power goes, the arm falls. It has pinch points, it moves fast, and it moves by
    itself while homing. Anchor it to the table, keep the E-stop within reach, keep hands out of the arm's path, and
    read the [Safety](02-safety/index.md) chapter: it is five minutes long.

## 1. What you need

| | Where to get it |
|---|---|
| **Your PAROL6**, built and wired, with the control board inside the base | the [Build guide](build/index.md); the parts in the [BOM](build/bill-of-materials.md), or as kits from [the shop](https://source-robotics.com/) |
| **The main firmware** on the control board | [Firmware and first run](build/firmware-and-first-run.md): a board from the shop comes with the test firmware |
| **A 24 V power supply**, 5 A | the [BOM](build/bill-of-materials.md) names one; any 24 V 5 A supply works |
| **An E-stop**, a normally closed button on the base | the [BOM](build/bill-of-materials.md) names one; any NC switch works |
| **A USB cable**, type B, to the PC | |
| **A PC** with Python 3.10 or 3.11 and the [commander software](gui/commander/installation.md), or Python 3.11 and the [Python API](programming/02-python-api/installation.md) | see the [minimum PC](01-overview/what-you-need.md#the-pc) |

Read in more detail: [What you need](01-overview/what-you-need.md).

## 2. Anchor the robot

Bolt the base to the table through its six holes, or clamp it to the edge. A free-standing PAROL6 tips over when
it extends.

!!! success "Check"
    Push the top of the base sideways, firmly: it must not lift or slide.

Read in more detail: [Mounting the robot](04-installation/mounting.md).

## 3. Connect

1. The E-stop to the two E-stop terminals on the base. Without it the robot will not run.
2. The USB cable to the PC.
3. The 24 V supply to the power connector. Nothing happens yet: the board is off until the button is pressed.

Read in more detail: [Connecting](04-installation/connecting.md).

## 4. Switch on

Hold the arm by the forearm and press the power button on the base. The motors energise, you hear six clicks,
and the arm holds its position. Let go.

!!! warning "The main firmware first"
    A control board from the shop comes with the test firmware, which turns all six motors as soon as the board
    starts. Upload the main firmware before you switch on the assembled robot
    ([Firmware and first run](build/firmware-and-first-run.md)).

Read in more detail: [First power-on](04-installation/first-power-on.md) · [Switching on and off](05-operation/switching-on-off.md).

!!! success "Check"
    Six drivers initialise and the arm supports itself before you let go. If it does not, use
    [First power-on: if nothing happens](04-installation/first-power-on.md#if-nothing-happens).

## 5. Start the software

=== "Commander software"
    Run `Serial_sender_good_latest.py`. Two windows open: the commander and the simulator. At the bottom of the
    commander enter the serial port (`COM5` on Windows, `ttyACM0` on Linux) and press **Connect**, more than once
    if the first try fails. The response log shows the robot's data when it is connected.

=== "Python API"
    ```
    parol6-server --serial COM5     # Linux: --serial /dev/ttyACM0
    ```
    In a second terminal:
    ```python
    from parol6 import RobotClient
    rbt = RobotClient()
    print(rbt.ping())               # hardware_connected=1
    ```

Read in more detail: [The commander software](gui/commander/index.md) · [The Python API](programming/02-python-api/index.md).

!!! success "Check"
    The commander shows incoming robot data, or `ping()` reports `hardware_connected=1`. If it does not,
    use [Communication troubleshooting](08-troubleshooting/communication.md).

## 6. Jog each joint

Before homing, check that every joint turns the way the software thinks it does. In the commander's **Joint jog**
menu press each joint's left arrow briefly: the joint must turn in its positive direction, as in the figure on
[Joint limits and directions](03-technical-data/joint-limits.md). A joint that turns the wrong way is fixed in the
firmware, not by trial: [Firmware and first run](build/firmware-and-first-run.md#a-joint-turns-the-wrong-way).

=== "Python API"
    ```python
    rbt.jog_j(0, speed=0.2, duration=0.5)     # joint 1, positive, half a second
    ```

Read in more detail: [Jogging](05-operation/jogging.md).

!!! success "Check"
    Every joint turned the way the figure shows. If one did not, fix it before you home:
    [A joint turns the wrong way](build/firmware-and-first-run.md#a-joint-turns-the-wrong-way).

## 7. Home

Press **Home** (commander) or call `rbt.home(wait=True)`. Joints 1, 2 and 3 move to their limit switches together,
then 4, then 6, then 5, and the arm ends in the standby pose with joint 1 turned 90°. Stay at the E-stop: a joint
that grinds at its end stop has a switch that does not trigger.

Read in more detail: [Homing](05-operation/homing.md) · [Homing failures](08-troubleshooting/homing-failures.md).

!!! success "Check"
    Homing finishes, the physical arm matches the simulator, and the witness marks agree. If a joint
    keeps travelling or the pose is wrong, stop and use [Homing failures](08-troubleshooting/homing-failures.md).

## 8. Move it

The simulator now matches the robot and the positions on screen are right. Jog in Cartesian space, write a
three-line RBTscript program, or run a Python move:

```python
rbt.move_j([90, -90, 180, 0, 0, 180], speed=0.3)
rbt.move_l([0, 263, 242, 90, 0, 90], speed=0.3)
```

## 9. Switch off

Hold the forearm, then press the power button. The arm goes limp the moment the motors lose power.

## 10. Where to go next

| You want to | Read |
|---|---|
| attach a gripper | [End effectors](end-effectors/index.md) |
| write programs | [Programming](programming/index.md), [RBTscript](programming/03-commander/rbtscript.md), [The Python API](programming/02-python-api/index.md) |
| use inputs, outputs, pneumatics | [Peripherals](06-peripherals/index.md) |
| understand what the robot does and does not protect against | [Safety functions](02-safety/safety-functions.md) |
| fix something | [Troubleshooting](08-troubleshooting/index.md) |
| look up a command | [API reference](reference/index.md) |
