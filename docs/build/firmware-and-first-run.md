# Firmware and first run

## 1. The test firmware

A control board from the shop ships with the test firmware. Use it, with the base open and the arm connected, to
check every driver, every switch and sensor, and the I/O from a serial terminal. At power-on it prints a report on
each driver (`joint N Connection is: GOOD` or `BAD`) and turns every motor slowly; `#LIMIT` then shows the
switches and `#IO` the E-stop, the inputs and the supply voltage. [The test firmware](../board/09-test-firmware.md)
has the commands and what good output looks like.

!!! danger
    The test firmware turns all six motors slowly from the moment it boots until the power is switched off; no
    command stops them. Use it with the arm unmounted or free to move, never on a robot standing on the table with
    its arm folded against a stop.

!!! success "Check"
    Six `Connection is: GOOD` lines in the report; `#LIMIT` names each switch while you press it; `#IO` follows
    the E-stop and the inputs and shows the supply near 24000 mV. If not:
    [Control board troubleshooting](../board/11-troubleshooting.md).

## 2. Upload the main firmware

The main firmware is in the repository under `PAROL6 control board main software`; it is a PlatformIO project
for VS Code. Install VS Code and the PlatformIO extension, open the folder, and upload with an ST-Link through the
programming adapter, with the 24 V supply disconnected: [Firmware](../board/08-firmware.md) has the procedure and
the warnings.

!!! success "Check"
    PlatformIO ends the upload with `SUCCESS`. If not: [Control board troubleshooting](../board/11-troubleshooting.md).

## 3. First power-on

Unplug the programming adapter, plug in the supply, hold the forearm and press the button. Six clicks, and the
arm holds. Start the commander software, connect, and open the joint jog menu.

!!! success "Check"
    Six clicks, the fan runs, the arm holds itself, and the commander shows the robot's data. If not:
    [First power-on: if nothing happens](../04-installation/first-power-on.md#if-nothing-happens).

## 4. A joint turns the wrong way { #a-joint-turns-the-wrong-way }

Press each joint's **left** arrow briefly. The joint must turn in its positive direction, as in the figure
([Joint limits and directions](../03-technical-data/joint-limits.md)).

![Each joint turned 30 degrees in its positive direction, in colour, over the pose in grey](../assets/kinematics/parol6_joint_directions.webp#only-light){ width="900" }
![Each joint turned 30 degrees in its positive direction, in colour, over the pose in grey](../assets/kinematics/parol6_joint_directions_dark.webp#only-dark){ width="900" }

A joint that turns the other way is the most common first-run problem, and it is fixed in the firmware, not by
rewiring:

```cpp
// motor_init.cpp, in Init_Joint_N: switch between 0 and 1
Joint__->direction_reversed = 1;
```

Upload again and check again. Swapping one motor phase's wires has the same effect, if you prefer to open the
base.

!!! success "Check"
    Every joint's left arrow turns it in its positive direction.

## 5. Home

With every direction right, press **Home** and stay at the E-stop. The sequence is on [Homing](../05-operation/homing.md);
if a joint grinds at a stop, press the E-stop and see [Homing failures](../08-troubleshooting/homing-failures.md).

!!! success "Check"
    Homing finishes, the simulator matches the robot, and the witness marks agree.

## The commander's terminal output

While it runs, the commander prints the robot's data to its terminal: the positions, the homed and I/O bytes,
the errors, the gripper data, and `Time between 2 commands in ms`, which should be near 0.010. Watch it for a few
minutes while jogging: if it is often much higher, the PC is too slow ([Communication](../08-troubleshooting/communication.md)).
