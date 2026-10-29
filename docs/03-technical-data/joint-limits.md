# Joint limits and directions

## Joint numbering and positive directions

Joints are numbered from the base up. A joint's angle increases in the direction of the arrow in the figure; the
commander software's left arrows jog in that direction.

![Joint numbering and the positive direction of each joint](../assets/rotations1.png){ width="560" }

## The standby pose

The pose the robot takes after homing, and the reference for the limits below. In the kinematic model's
Denavit-Hartenberg convention this pose has joint 1 at 0°; the firmware homes joint 1 to +90° so that the arm
stands square to the base, and the software reports the standby pose as follows.

| Joint 1 | Joint 2 | Joint 3 | Joint 4 | Joint 5 | Joint 6 |
|---|---|---|---|---|---|
| 90° (0° in the DH table) | −90° | 180° | 0° | 0° | 180° |

![The standby pose](../assets/Joints.png){ width="500" }

## Limits

The limits the software enforces, in degrees, as the robot reaches them after homing. Both the commander and the
Python API refuse a target outside them.

| Joint | Negative limit | Standby | Positive limit | In motor steps (from standby) |
|---|---|---|---|---|
| J1 | −123.05° | 0° (DH) | +123.05° | −14000 to +14000 |
| J2 | −145.01° | −90° | −3.38° | −51587 to −1200 |
| J3 | 107.87° | 180° | 287.87° | 34700 to 92605 |
| J4 | −105.47° | 0° | +105.47° | −7500 to +7500 |
| J5 | −90° | 0° | +90° | −6400 to +6400 |
| J6 | 0° | 180° | 360° | one turn |

Joints 2 and 3 are limited in both directions by their geometry and their switches; joints 1 and 4 by printed
blockers; joint 5 by the length of its belt path; joint 6 only by the cables and tubes that run through the wrist.

!!! warning "Grippers and bases change the limits"
    A gripper changes where joint 5 can go without colliding with the forearm, and a riser under the base changes
    what joint 2 can reach. The software limits do not know about either: check the real clearances with a slow
    jog before you run a program near a limit.

!!! danger "Joint 5 and joint 6"
    Joint 5 must never be turned more than one rotation, by hand or by software; joint 6 and joint 1 must never
    be spun more than one turn. The cables and pneumatic tubes that pass through them wrap and tear.
    [Moving the robot by hand](../02-safety/moving-by-hand.md) has the figure.

![The range of joint 5](../assets/Limits_j5.png){ width="700" }
