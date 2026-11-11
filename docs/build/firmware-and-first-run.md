# Firmware and first run

Five parts, in order: check the board with the test firmware, upload the main firmware, switch on, fix any joint
that turns the wrong way, and home.

## 1. The test firmware

A control board from the shop ships with the test firmware. Use it with the base open and the motors not yet
driving the arm: on the bench, before the arm is assembled, as in
[Electronics and wiring](electronics-and-wiring.md#test-before-you-close-the-base).

!!! danger
    The test firmware turns all six motors slowly from the moment it boots until the power is switched off; no
    command stops them. On an assembled arm joints 1 to 5 reach their blockers within about a minute and keep
    pushing. Use it with the motors free to turn, never on an assembled robot.

At power-on it prints a report on each driver (`joint N Connection is: GOOD` or `BAD`) and turns every motor
slowly. `#LIMIT` then shows the switches, and `#IO` the E-stop, the inputs and the supply voltage.

[The test firmware](../board/09-test-firmware.md) has the commands and what good output looks like.

!!! success "Check"
    Six `Connection is: GOOD` lines in the report; `#LIMIT` names each switch while you press it; `#IO` follows
    the E-stop and the inputs and shows the supply near 24000 mV. If not:
    [Control board troubleshooting](../board/11-troubleshooting.md).

## 2. Upload the main firmware

The main firmware is in the repository under `PAROL6 control board main software`. It is a PlatformIO project for
VS Code.

1. Install VS Code and the PlatformIO extension.
2. Open the folder.
3. Disconnect the 24 V supply.
4. Upload with an ST-Link through the programming adapter.

[Firmware](../board/08-firmware.md) has the procedure and the warnings.

!!! success "Check"
    PlatformIO ends the upload with `SUCCESS`. If not: [Control board troubleshooting](../board/11-troubleshooting.md).

## 3. First power-on

1. Unplug the programming adapter.
2. Plug in the supply.
3. Hold the forearm and press the button. Six clicks, and the arm holds.
4. Start the commander software, connect, and open the joint jog menu.

!!! success "Check"
    Six clicks, the fan runs, the arm holds itself, and the commander shows the robot's data. If not:
    [First power-on: if nothing happens](../04-installation/first-power-on.md#if-nothing-happens).

## 4. A joint turns the wrong way { #a-joint-turns-the-wrong-way }

Jog each joint briefly. The joint must turn as in the figure, which shows each joint's positive direction
([Joint limits and directions](../03-technical-data/joint-limits.md)).

![Each joint turned 30 degrees in its positive direction, in colour, over the pose in grey](../assets/kinematics/parol6_joint_directions.webp#only-light){ width="900" }
![Each joint turned 30 degrees in its positive direction, in colour, over the pose in grey](../assets/kinematics/parol6_joint_directions_dark.webp#only-dark){ width="900" }

- **Joint 2**: press its **right** arrow (negative). It must turn opposite to the figure; its left arrow does
  nothing until the robot is homed.
- **Joints 1, 3, 4, 5 and 6**: press the **left** arrow (positive). It must turn as in the figure.

??? info "Why joint 2 jogs only one way before homing"
    Before homing, the commander checks jogs against the joint limits with a position count that starts at 0, so
    some directions are refused with `Error: Robot jog -> Position out of range`.

A joint that turns the other way is the most common first-run problem. It is fixed in the firmware, not by
rewiring:

1. In `motor_init.cpp`, in `Init_Joint_N`, switch `direction_reversed` between 0 and 1:

    ```cpp
    // motor_init.cpp, in Init_Joint_N: switch between 0 and 1
    Joint__->direction_reversed = 1;
    ```

2. Upload again.
3. Check again.

Swapping one motor phase's wires has the same effect, if you prefer to open the base.

!!! success "Check"
    The left arrows of joints 1 and 3 to 6 turn them as in the figure, and joint 2's right arrow turns it the
    opposite way.

## 5. Home

1. With every direction right, set joint 6 and check the tool's homing offset, as in
   [Before you press Home](../05-operation/homing.md#before-you-press-home).
2. Press **Home**, and stay at the E-stop.

The sequence is on [Homing](../05-operation/homing.md). If a joint grinds at a stop, press the E-stop and see
[Homing failures](../08-troubleshooting/homing-failures.md).

!!! success "Check"
    Homing finishes, the simulator matches the robot, and the pin passes through the witness marks of each joint,
    which line up in the after-homing pose ([Witness marks](../05-operation/mastering.md#witness-marks)).

## The commander's terminal output

While it runs, the commander prints the robot's data to its terminal: the positions, the homed and I/O bytes, the
errors, the gripper data, and `Time between 2 commands in ms`.

That last number should be near 0.010. It is in seconds, despite the label: 0.010 is 10 ms. Watch it for a few
minutes while jogging. If it is often much higher, the PC is too slow
([Communication](../08-troubleshooting/communication.md)).
