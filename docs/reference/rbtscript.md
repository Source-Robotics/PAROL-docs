# RBTscript commands

The commands of the commander software's program language, as its interpreter accepts them. One command per
line; arguments in the order given; angles in degrees, positions in millimetres, speed and acceleration in
percent, time in seconds. [RBTscript](../programming/03-commander/rbtscript.md) in the guide has the rules and
examples.

| Command | Arguments | What it does |
|---|---|---|
| `Begin()` | | Execution starts here |
| `End()` | | Execution stops here |
| `Loop()` | | Restart from `Begin()` |
| `Delay(t)` | `t` seconds, 0.01 minimum | Wait |
| `MoveJoint(j1,j2,j3,j4,j5,j6, v=, a=, t=, func, speed)` | six joint angles; `v`, `a` in % for the leading joint; `t` duration; `func` `"poly"` or `"trap"`; the word `speed` | A move to joint angles, straight in joint space |
| `MovePose(x,y,z,Rx,Ry,Rz, v=, a=, t=, func, speed)` | a WRF pose, then as `MoveJoint` | IK at the target, then a joint-space move |
| `MoveCart(x,y,z,Rx,Ry,Rz, t=, func, speed)` | a WRF pose; `t`; `func`; `speed` | A straight-line move of the tool in the WRF; stops at a singularity |
| `MoveCartRelTRF(x,y,z,Rx,Ry,Rz, t=, func, speed)` | a pose relative to the tool frame | A straight-line move relative to the tool |
| `SpeedJoint()`, `SpeedCart()` | | In the menu; not implemented |
| `Output(n, HIGH\|LOW)` | output 1 or 2; `HIGH` or `LOW` | Sets an output |
| `Input()` | | In the menu; conditions on inputs are not implemented |
| `Gripper_cal()` | | Calibrates and activates the electric gripper; follow with a `Delay()` |
| `Gripper(position, speed, current)` | 0 to 255; 0 to 255; mA (0 to 1300) | Moves the electric gripper; continues at once, so follow with a `Delay()` |

Rules for the motion commands: `t` overrides `v` and `a` and makes the profile polynomial unless `func="trap"`;
`v` with `a` makes it trapezoidal; neither gives a conservative trapezoid; `speed` as the last argument tracks the
speed curve only and may stop short of the target. The list is in the commander's `PAROL6_ROBOT.py` as
`Commands_list`.
