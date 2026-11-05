# What you need

## Power

A 24 V DC supply of at least 5 A. The [BOM](https://docs.source-robotics.com/PAROL-docs/1.1/build/bill-of-materials/) names a Mean Well 120 W DIN-rail unit;
any regulated 24 V 5 A supply with the robot's GX16 power connector wired to it does. The control board accepts
18 to 24 V; below 24 V the motors lose torque and speed. The robot draws about 40 W in typical use and more when
all six motors accelerate at once. A closed supply with a mains cable needs no mains wiring; the DIN-rail unit
does, in a closed box ([The power supply](https://docs.source-robotics.com/PAROL-docs/1.1/04-installation/connecting/#the-power-supply)).

Plug the supply in through a **mains switch within reach**, a switched socket strip for example. It is the stop
that still works when the PC software has frozen ([Emergency stop](https://docs.source-robotics.com/PAROL-docs/1.1/02-safety/emergency-stop/)), and the
switch you reach for when the E-stop has no effect.

## The E-stop

A normally closed emergency stop button, wired to the two E-stop terminals of the control board. The robot does
not run without it. The kit's button sits in its own 3D-printed box, on a cable as long as your setup needs; any NC switch works for a bench
setup ([Emergency stop](https://docs.source-robotics.com/PAROL-docs/1.1/02-safety/emergency-stop/)).

## The PC

The PC runs the kinematics and the planner and must send a packet to the robot every 10 ms without hiccups. A
machine that falls behind makes the robot stutter. Tested systems and the minimum are in the commander
repository's [confirmed working systems](https://github.com/Source-Robotics/PAROL-commander-software/blob/main/confirmed_working_systems.md):
at least an Intel i5 six-core processor of 2017 or newer, or an AMD equivalent. The tested systems include two
Windows 10 PCs with six-core AMD Ryzen processors, a Radxa ROCK 5B on Linux and a six-core MacBook Pro.

| | Commander software | Python API |
|---|---|---|
| Operating system | Windows, Linux, macOS | Windows, Linux (x86-64 and ARM64), macOS (ARM64) |
| Python | 3.10 or 3.11 | 3.11 or newer |
| Connection | USB (a serial port, 3 Mbaud) | USB on the PC that runs the controller; clients anywhere on the network |

A USB type B cable connects the robot to the PC. USB does not power the board.

## Tools

For an assembled robot: hex keys, 4 mm for the M5 mounting screws and 2, 2.5 and 3 mm for the gripper, a small screwdriver for
the terminal blocks. For a build, the [Build guide](https://docs.source-robotics.com/PAROL-docs/1.1/build/) lists the rest, down to the blue
threadlocker and the thermal cement.

## Knowledge

You should be able to use a hex key. Python and the terminal you can learn on the way: the
[Quick start](https://docs.source-robotics.com/PAROL-docs/1.1/quick-start/) gives every command to type, for someone who has never used either. The
[Theory corner](https://docs.source-robotics.com/PAROL-docs/1.1/theory/) explains the robotics vocabulary the software uses, from
joint numbering to singularities, in the order you meet it.
