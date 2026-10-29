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
seconds, gripper position and speed 0 to 255, gripper current in milliamps ([Units](../02-concepts/units.md)).

## Motion

### MoveJoint

```
MoveJoint(j1, j2, j3, j4, j5, j6, v=0, a=0, t=0, func, speed)
```

Moves all joints to the given angles; the path is a straight line in joint space, all joints stopping together.
The tool's path curves.

| Argument | Meaning | Unit |
|---|---|---|
| `j1` … `j6` | The target joint angles | degrees |
| `v` | Speed of the leading joint, the one with the longest way | % (0 to 100) |
| `a` | Acceleration and deceleration of the leading joint | % |
| `t` | Duration of the move; overrides `v` and `a` | seconds |
| `func` | The profile: `"poly"` (quintic polynomial) or `"trap"` (trapezoidal) | |
| `speed` | The word `speed` as the last argument: track the speed curve only | |

The arguments must be in this order. The rules:

- With `t`, the move takes that long; the profile is polynomial unless `func="trap"`, and a trapezoid with `t`
  spends a third of the time in each phase.
- With `v` and `a`, the profile is trapezoidal, for the leading joint; the other joints get what makes them
  finish together.
- With neither, a conservative trapezoid.
- With `speed` last, only the speed curve is tracked: smoother and quieter, and the robot may stop a few steps
  short of the target ([Target, commanded and actual](../02-concepts/target-commanded-actual.md)).

```
MoveJoint(0,-90,180,0,0,180,t=4)
MoveJoint(0,-90,180,0,0,180,v=50,a=50)
MoveJoint(0,-90,180,0,0,180)
MoveJoint(0,-90,180,0,0,180,speed)
```

### MovePose

```
MovePose(x, y, z, Rx, Ry, Rz, v=0, a=0, t=0, func, speed)
```

Like `MoveJoint`, but the target is a pose in the WRF: the inverse kinematics is solved once at the target and the
robot moves in joint space to the configuration it found, which may not be the one you expected. The same
arguments and rules as `MoveJoint`.

### MoveCart

```
MoveCart(x, y, z, Rx, Ry, Rz, t=0, func, speed)
```

Moves the tool in a straight line to the pose, in the WRF. The joints' motion is whatever the straight line
requires, and the move stops if it meets a singularity; the robot does not deviate from the line to avoid one.
`t`, `func` and `speed` as above.

### MoveCartRelTRF

```
MoveCartRelTRF(x, y, z, Rx, Ry, Rz, t=0, func, speed)
```

A straight-line move relative to the current tool frame: `MoveCartRelTRF(-80,0,0,0,0,0)` moves 80 mm along the
tool's −X. For rotations about more than one axis, use two commands, one axis each.

### SpeedJoint, SpeedCart

Listed in the command menu as joint and Cartesian speed moves; not implemented in the current version.

## Timing and flow

| Command | Meaning |
|---|---|
| `Begin()` | Where execution starts |
| `End()` | Where it stops |
| `Loop()` | Restart from the beginning |
| `Delay(t)` | Wait `t` seconds; the shortest delay is one control cycle, 10 ms |

## I/O

```
Output(1,HIGH)
Output(2,LOW)
```

Sets output 1 or 2. `Input()` appears in the menu for reading an input; conditions on it are not available in
this version.

## Gripper

```
Gripper_cal()
Delay(3)
Gripper(position, speed, current)
Delay(2)
```

`Gripper_cal()` calibrates and activates the SSG-48 or MSG gripper; add a delay for it to finish. `Gripper()`
moves it: position 0 (open) to 255 (closed), speed 0 to 255, current 0 to 1300 mA, the current being the grip
force; below about 150 mA the gripper does not move. The program continues at once, so add a `Delay()` for the
gripper to arrive.

!!! danger
    A current above about 700 mA with a high speed slams the jaws into the part and can damage the gripper, the
    robot and the part. Start low.

A gripper error (not calibrated, E-stop, timeout) stops the gripper until it is cleared in the Gripper tab.

## Reference

The commands on one page: [RBTscript commands](../../reference/rbtscript.md).
