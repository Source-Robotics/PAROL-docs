# What you need

| You need | In short | More |
|---|---|---|
| Power | A 24 V DC supply of at least 5 A, behind a mains switch within reach | [Power](#power) |
| An E-stop | A normally closed button | [The E-stop](#the-e-stop) |
| A PC | One that sends a packet every 10 ms without hiccups | [The PC](#the-pc) |
| A USB cable | Type B | [The PC](#the-pc) |
| Tools | Hex keys and a small screwdriver | [Tools](#tools) |
| Knowledge | How to use a hex key | [Knowledge](#knowledge) |

## Power

A 24 V DC supply of at least 5 A. The [BOM](../build/bill-of-materials.md) names a Mean Well 120 W DIN-rail unit;
any regulated 24 V 5 A supply with the robot's GX16 power connector wired to it does.

| | |
|---|---|
| Input the control board accepts | 18 to 24 V; below 24 V the motors lose torque and speed |
| What the robot draws | About 40 W in typical use, more when all six motors accelerate at once |

| Supply | Mains wiring |
|---|---|
| A closed supply with a mains cable | None |
| The DIN-rail unit | Yes, in a closed box ([The power supply](../04-installation/connecting.md#the-power-supply)) |

!!! warning "A mains switch within reach"
    Plug the supply in through a **mains switch within reach**, a switched socket strip for example. It is the
    stop that still works when the PC software has frozen ([Emergency stop](../02-safety/emergency-stop.md)), and
    the switch you reach for when the E-stop has no effect.

## The E-stop

A normally closed emergency stop button, wired to the two E-stop terminals of the control board. The robot does not
run without it.

The kit's button sits in its own 3D-printed box, on a cable as long as your setup needs. Any NC switch works for a
bench setup ([Emergency stop](../02-safety/emergency-stop.md)).

## The PC

The PC runs the kinematics and the planner, and must send a packet to the robot every 10 ms without hiccups. A
machine that falls behind makes the robot stutter.

| | |
|---|---|
| Minimum | An Intel i5 six-core processor of 2017 or newer, or an AMD equivalent |
| Tested systems include | Two Windows 10 PCs with six-core AMD Ryzen processors, a Radxa ROCK 5B on Linux, a six-core MacBook Pro |

Tested systems and the minimum are in the commander repository's
[confirmed working systems](https://github.com/Source-Robotics/PAROL-commander-software/blob/main/confirmed_working_systems.md).

| | Commander software | Python API |
|---|---|---|
| Operating system | Windows, Linux, macOS | Windows, Linux (x86-64 and ARM64), macOS (ARM64) |
| Python | 3.10 or 3.11 | 3.11 or newer |
| Connection | USB (a serial port, 3 Mbaud) | USB on the PC that runs the controller; clients anywhere on the network |

A USB type B cable connects the robot to the PC. USB does not power the board.

## Tools

| For | Tools |
|---|---|
| An assembled robot | Hex keys: 4 mm for the M5 mounting screws, and 2, 2.5 and 3 mm for the gripper. A small screwdriver for the terminal blocks. |
| A build | The [Build guide](../build/index.md) lists the rest, down to the blue threadlocker and the thermal cement |

## Knowledge

You should be able to use a hex key. Python and the terminal you can learn on the way:

| To learn | Read |
|---|---|
| Every command to type, for someone who has never used Python or a terminal | The [Quick start](../quick-start.md) |
| The robotics vocabulary the software uses, from joint numbering to singularities, in the order you meet it | The [Theory corner](../theory/index.md) |
