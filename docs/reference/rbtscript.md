# RBTscript commands

The commands of the commander software's program language, as its interpreter accepts them. One command per
line; arguments in the order given; angles in degrees, positions in millimetres, speed and acceleration in
percent, time in seconds. [RBTscript](../programming/03-commander/rbtscript.md) in the guide has the rules and
examples.

| Command | Arguments | What it does |
|---|---|---|
| `Begin()` | | Must be the first line, or the program is refused |
| `End()` | | Stops the program; the last line must be `End()` or `Loop()` |
| `Loop()` | | Restart at the line after `Begin()` |
| `Delay(t)` | `t` seconds, more than 0.01 | Wait; `Delay(0.01)` is refused |
| `MoveJoint(j1,j2,j3,j4,j5,j6, v=, a=, t=, trap\|poly, speed)` | six joint angles; `v`, `a` in % for the leading joint; `t` duration; the bare word `trap` or `poly`; the word `speed` | A move to joint angles, straight in joint space |
| `MovePose(x,y,z,Rx,Ry,Rz, v=, a=, t=, trap\|poly, speed)` | a WRF pose, then as `MoveJoint` | IK at the target, then a joint-space move |
| `MoveCart(x,y,z,Rx,Ry,Rz, v=, a=, t=, trap\|poly, speed)` | a WRF pose; `t`; `poly` or `trap`; `speed` | A straight-line move of the tool in the WRF; stops at a singularity. With `t`: trapezoidal unless `poly`. Without `t`: always 3.6 s |
| `MoveCartRelTRF(x,y,z,Rx,Ry,Rz, v=, a=, t=, trap\|poly, speed)` | a pose relative to the tool frame | A straight-line move relative to the tool; timing as `MoveCart` |
| `SpeedJoint()` | | No action: the program stops on it until Stop |
| `SpeedCart()` | | Not accepted: a program containing it is refused |
| `Output(n,HIGH\|LOW)` | output 1; `HIGH` or `LOW`, no space | Sets output 1; `Output(2,...)` is refused in the current version and stops the program |
| `Input()`, `Home()` | | No action: the program stops on it until Stop |
| `Gripper_cal()` | | Calibrates the electric gripper (activation is the Gripper tab's Activate option); follow with a `Delay()` |
| `Gripper(position, speed, current)` | whole numbers: 0 to 255; 0 to 255; mA, 100 to 1000 | Moves the electric gripper; continues at once, so follow with a `Delay()` |

Rules for `MoveJoint` and `MovePose`: `t` overrides `v` and `a` and makes the profile polynomial unless the word
`trap` follows; `v` with `a` makes it trapezoidal; neither gives a conservative trapezoid; `speed` as the last argument tracks the
speed curve only and may stop short of the target. `MoveCart` and `MoveCartRelTRF` are trapezoidal with `t` unless
`poly` follows, and take 3.6 s for any move without `t`. The list is in the commander's `PAROL6_ROBOT.py` as
`Commands_list`.
