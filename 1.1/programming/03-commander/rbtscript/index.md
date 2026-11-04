# RBTscript

RBTscript is the commander's program language: one command per line, executed in order, synchronised to the
100 Hz control loop. It has motion in joint and Cartesian space, delays, outputs and the gripper, and a loop.
There are no variables, conditions or arithmetic: a program is a sequence.

```
Begin()
MoveJoint(90,-90,180,0,0,180,t=3)
MoveCart(0,263,242,90,0,90)
Delay(1)
Loop()
```

## Units

Angles in degrees, positions in millimetres, speed and acceleration in percent of the robot's maximum, time in
seconds, gripper position and speed 0 to 255, gripper current in milliamps ([Units](https://docs.source-robotics.com/PAROL-docs/1.1/theory/units/)).

## Motion

### MoveJoint

```
MoveJoint(j1, j2, j3, j4, j5, j6, v=0, a=0, t=0, trap|poly, speed)
```

Moves all joints to the given angles; the path is a straight line in joint space, all joints stopping together.
The tool's path curves.

| Argument | Meaning | Unit |
|---|---|---|
| `j1` … `j6` | The target joint angles | degrees |
| `v` | Speed of the leading joint, the one with the longest way | % (0 to 100) |
| `a` | Acceleration and deceleration of the leading joint | % |
| `t` | Duration of the move; overrides `v` and `a` | seconds |
| `trap`, `poly` | The profile, as a bare word: `poly` (quintic polynomial) or `trap` (trapezoidal). `"trap"` in quotes or `func=trap` is ignored without a message and gives the default | |
| `speed` | The word `speed` as the last argument: track the speed curve only | |

The arguments must be in this order. The rules:

- With `t`, the move takes that long; the profile is polynomial unless the word `trap` follows, and a trapezoid
  with `t` spends a third of the time in each phase.
- With `v` and `a`, the profile is trapezoidal, for the leading joint; the other joints get what makes them
  finish together.
- With neither, a conservative trapezoid.
- With `speed` last, only the speed curve is tracked: smoother and quieter, and the robot may stop a few steps
  short of the target ([Target, commanded and actual](https://docs.source-robotics.com/PAROL-docs/1.1/theory/target-commanded-actual/)).

```
MoveJoint(0,-90,180,0,0,180,t=4)
MoveJoint(0,-90,180,0,0,180,t=4,trap)
MoveJoint(0,-90,180,0,0,180,v=50,a=50)
MoveJoint(0,-90,180,0,0,180)
MoveJoint(0,-90,180,0,0,180,speed)
```

### MovePose

```
MovePose(x, y, z, Rx, Ry, Rz, v=0, a=0, t=0, trap|poly, speed)
```

Like `MoveJoint`, but the target is a pose in the WRF: the inverse kinematics is solved once at the target and the
robot moves in joint space to the configuration it found, which may not be the one you expected. The same
arguments and rules as `MoveJoint`.

### MoveCart

```
MoveCart(x, y, z, Rx, Ry, Rz, v=0, a=0, t=0, trap|poly, speed)
```

Moves the tool in a straight line to the pose, in the WRF. The joints' motion is whatever the straight line
requires, and the move stops if it meets a singularity; the robot does not deviate from the line to avoid one.
The timing rules differ from `MoveJoint`:

- With `t`, the move takes that long and the profile is **trapezoidal** unless the word `poly` follows, the
  opposite of `MoveJoint`.
- Without `t`, **every move takes 3.6 s**, however long it is, so a long move without `t` is fast. `v` and `a`
  are accepted but only checked for range. Give `t` for every Cartesian move.

### MoveCartRelTRF

```
MoveCartRelTRF(x, y, z, Rx, Ry, Rz, v=0, a=0, t=0, trap|poly, speed)
```

A straight-line move relative to the current tool frame: `MoveCartRelTRF(-80,0,0,0,0,0)` moves 80 mm along the
tool's −X. For rotations about more than one axis, use two commands, one axis each. The timing rules are
those of `MoveCart`.

### SpeedJoint, SpeedCart

Listed in the command menu, but neither works. `SpeedJoint()` passes the program check and has no action: the
program stops on that line until you press **Stop**. `SpeedCart()` fails the check, and a program that contains
it is refused; so are the menu's `Get_data` and `Timeouts`.

## Timing and flow

| Command | Meaning |
|---|---|
| `Begin()` | Must be the first line; a program that does not start with it is refused |
| `End()` | Stops the program; the last line must be `End()` or `Loop()`, or the program is refused |
| `Loop()` | Restarts at the line after `Begin()` |
| `Delay(t)` | Waits `t` seconds; `t` must be more than 0.01, and `Delay(0.01)` is refused and stops the program |

## I/O

```
Output(1,HIGH)
Output(1,LOW)
```

Sets output 1, with no space after the comma. In the current version `Output(2,HIGH)` and `Output(2,LOW)` are
refused by a bug in the check (`Invalid Output() command`) and stop the program, so only output 1 can be switched
from a program. `Input()` appears in the menu but has no action: a program stops on it until you press **Stop**;
`Home()` behaves the same.

## Gripper

```
Gripper_cal()
Delay(4)
Gripper(position, speed, current)
Delay(2)
```

`Gripper_cal()` calibrates the SSG-48 or MSG gripper. Clear the gripper's error first, with the Gripper tab's
**Clear gripper error** (RBTscript has no command for it), and add a delay for the calibration to finish:
`Delay(4)` for the SSG-48 (about 3 s) and `Delay(7)` for the MSG (5 to 6 s on the longer rails). Activating it
is the Gripper tab's **Activate** option, which is on by default. `Gripper()` moves it, with whole numbers only:
position 0 (open) to 255 (closed), speed 0 to 255, current 100 to 1000 mA, the current being the grip force;
below about 150 mA the gripper does not move. A value outside these ranges is logged as `Gripper() invalid input value`, the
line is skipped and the program goes on. The program continues at once, so add a `Delay()` for the
gripper to arrive.

!!! danger
    A current above about 700 mA with a high speed slams the jaws into the part and can damage the gripper, the
    robot and the part. Start low.

A gripper error (not calibrated, E-stop, timeout) stops the gripper until it is cleared in the Gripper tab.

## Reference

The commands on one page: [RBTscript commands](https://docs.source-robotics.com/PAROL-docs/1.1/reference/rbtscript/).
