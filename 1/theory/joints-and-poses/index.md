# Joints, directions and the standby pose

## Numbering

Joints are numbered 1 to 6 from the base up: J1 turns the whole arm about the vertical axis, J2 is the shoulder,
J3 the elbow, J4 rotates the forearm, J5 pitches the wrist, J6 rotates the tool. The Python API indexes joints
from 0 in its jog calls (`jog_j(0, ...)` is J1) and lists angles in order J1 to J6 everywhere.

Joints 4, 5 and 6 are also called wrist 1, wrist 2 and wrist 3, as in the robot model and ROS.
The forearm is also called the lower arm: both names mean the link from the elbow to the wrist.

![Each joint turned 30 degrees in its positive direction, in colour, over the pose in grey](https://docs.source-robotics.com/PAROL-docs/1/assets/kinematics/parol6_joint_directions.webp){ width="900" }
![Each joint turned 30 degrees in its positive direction, in colour, over the pose in grey](https://docs.source-robotics.com/PAROL-docs/1/assets/kinematics/parol6_joint_directions_dark.webp){ width="900" }

## Positive direction

Each joint has a positive direction, the one in which its angle increases, drawn as the arrows in the figure on
[Joint limits and directions](https://docs.source-robotics.com/PAROL-docs/1/03-technical-data/joint-limits/). The commander's left arrows jog
positive, the right arrows negative. The firmware has a per-joint flag that inverts the motor so that the
hardware agrees with this convention; a new build sets it per joint on the first run.

## Joint space and the standby pose

A set of six joint angles is a point in **joint space**: it describes the arm's configuration completely, and a
joint move is a straight line in it, every joint moving proportionally and finishing at the same time.

The reference point is the **standby pose**, the pose of the Denavit-Hartenberg table; after homing the robot
stands in it turned 90° about joint 1:

| Pose | J1 | J2 | J3 | J4 | J5 | J6 |
|---|---|---|---|---|---|---|
| Standby | 0° | −90° | 180° | 0° | 0° | 180° |
| After homing | 90° | −90° | 180° | 0° | 0° | 180° |

Every joint angle the software reports is measured in this convention. At J1 = 0° the arm points along the
base's X axis, away from the electronics box; homing ends with J1 a quarter turn further, at 90°, and the
software reports 90° there. The Python API calls that after-homing pose its standby.

## Limits

Each joint has a software limit in both directions, enforced by the planner and by the jog, and a mechanical
stop a little past it ([Joint limits and directions](https://docs.source-robotics.com/PAROL-docs/1/03-technical-data/joint-limits/)). The limits are
in the robot model (`PAROL6_ROBOT.py` in both programs); a tool or a base that changes the real clearance does
not change them.
