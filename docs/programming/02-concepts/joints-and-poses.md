# Joints, directions and the standby pose

## Numbering

Joints are numbered 1 to 6 from the base up: J1 turns the whole arm about the vertical axis, J2 is the shoulder,
J3 the elbow, J4 rotates the forearm, J5 pitches the wrist, J6 rotates the tool. The Python API indexes joints
from 0 in its jog calls (`jog_j(0, ...)` is J1) and lists angles in order J1 to J6 everywhere.

![Joint numbering](../../assets/Joints.png){ width="500" }

## Positive direction

Each joint has a positive direction, the one in which its angle increases, drawn as the arrows in the figure on
[Joint limits and directions](../../03-technical-data/joint-limits.md). The commander's left arrows jog
positive, the right arrows negative. The firmware has a per-joint flag that inverts the motor so that the
hardware agrees with this convention; a new build sets it per joint on the first run.

## Joint space and the standby pose

A set of six joint angles is a point in **joint space**: it describes the arm's configuration completely, and a
joint move is a straight line in it, every joint moving proportionally and finishing at the same time.

The reference point is the **standby pose**, the pose after homing:

| J1 | J2 | J3 | J4 | J5 | J6 |
|---|---|---|---|---|---|
| 90° | −90° | 180° | 0° | 0° | 180° |

Every joint angle the software reports is measured from the kinematic model's zero in this convention. The model's
Denavit-Hartenberg zero has J1 at 0°, with the arm along the base's X axis; the firmware homes J1 a quarter turn
further, to 90°, so that the arm stands square to the base, and the software reports 90°. Both say the same
thing about the same pose.

## Limits

Each joint has a software limit in both directions, enforced by the planner and by the jog, and a mechanical
stop a little past it ([Joint limits and directions](../../03-technical-data/joint-limits.md)). The limits are
in the robot model (`PAROL6_ROBOT.py` in both programs); a tool or a base that changes the real clearance does
not change them.
