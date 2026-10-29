# Quick start

From an assembled robot to one that is homed and moves on command, on one page. Every step ends with a link to
the chapter that explains it. Follow the link when a step is not clear or something fails. If you are still
building the robot, start with the [Build guide](build/index.md); this page begins where it ends.

!!! danger "Read first"
    PAROL6 has no brakes: when the power goes, the arm falls. It has pinch points, it moves fast, and it moves by
    itself while homing. Anchor it to the table, keep the E-stop within reach, keep hands out of the arm's path, and
    read the [Safety](02-safety/index.md) chapter: it is five minutes long.

## 1. What you need

| | Where to get it |
|---|---|
| **A PAROL6**, assembled, with the control board inside the base | [the shop](https://source-robotics.com/), or [build your own](build/index.md) |
| **A 24 V power supply**, 5 A | in the kit, or any 24 V 5 A supply (the [BOM](build/bill-of-materials.md) names one) |
| **An E-stop**, a normally closed button on the base | in the kit; any NC switch works |
| **A USB cable**, type B, to the PC | |
| **A PC** with Python 3.10 or 3.11 and the [commander software](gui/commander/installation.md), or Python 3.11 and the [Python API](programming/03-python-api/installation.md) | see the [minimum PC](01-overview/what-you-need.md#the-pc) |

Read in more detail: [What you need](01-overview/what-you-need.md).

## 2. Anchor the robot

Bolt the base to the table through its six holes, or clamp it to the edge. A free-standing PAROL6 tips over when
it extends.

Read in more detail: [Mounting the robot](04-installation/mounting.md).

## 3. Connect

1. The E-stop to the two E-stop terminals on the base. Without it the robot will not run.
2. The USB cable to the PC.
3. The 24 V supply to the power connector. Nothing happens yet: the board is off until the button is pressed.

Read in more detail: [Connecting](04-installation/connecting.md).

## 4. Switch on

Hold the arm by the forearm and press the power button on the base. The motors energise, you hear six clicks,
and the arm holds its position. Let go.

The control board ships with the main firmware if it came with a robot. A board bought on its own has the test
firmware: upload the main firmware first ([Firmware](board/08-firmware.md)).

Read in more detail: [First power-on](04-installation/first-power-on.md) · [Switching on and off](05-operation/switching-on-off.md).

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

Read in more detail: [The commander software](gui/commander/index.md) · [The Python API](programming/03-python-api/index.md).

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

## 7. Home

Press **Home** (commander) or call `rbt.home(wait=True)`. Joints 1, 2 and 3 move to their limit switches together,
then 4, then 6, then 5, and the arm ends in the standby pose with joint 1 turned 90°. Stay at the E-stop: a joint
that grinds at its end stop has a switch that does not trigger.

Read in more detail: [Homing](05-operation/homing.md) · [Homing failures](08-troubleshooting/homing-failures.md).

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
| write programs | [Programming](programming/index.md), [RBTscript](programming/04-commander/rbtscript.md), [The Python API](programming/03-python-api/index.md) |
| use inputs, outputs, pneumatics | [Peripherals](06-peripherals/index.md) |
| understand what the robot does and does not protect against | [Safety functions](02-safety/safety-functions.md) |
| fix something | [Troubleshooting](08-troubleshooting/index.md) |
| look up a command | [API reference](reference/index.md) |
