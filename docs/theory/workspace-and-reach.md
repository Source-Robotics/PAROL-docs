# Workspace and reach

## Reach

The furthest the flange centre gets from the axis of joint 1, within the [joint limits](../03-technical-data/joint-limits.md):
408 mm. The standard pneumatic gripper's tool centre point gets to 434 mm. A longer tool reaches further and
weighs on joints 4 and 5.

## Workspace

![Where the flange centre can go within the joint limits, side and top view, in mm](../assets/figures/parol6_workspace_flange.webp#only-light){ width="900" }
![Where the flange centre can go within the joint limits, side and top view, in mm](../assets/figures/parol6_workspace_flange_dark.webp#only-dark){ width="900" }

In the side view the shaded region is everywhere the centre of the flange can go in the plane of the arm, within
the joint limits of the robot's model. The dotted line is the same for the wrist centre.

| It reaches | |
|---|---|
| In front of the joint 1 axis | 408 mm |
| Behind it | 359 mm |
| Above the mounting surface | 523 mm |
| Below it | 25 mm |

The top view sweeps that region about joint 1 through its ±97.4°: in front of the base the arm reaches out
directly, behind it (lighter) only by folding back over the base.

A tool adds its own length. The same figure for each gripper, with a table of the numbers, is on
[Dimensions and kinematics](../03-technical-data/kinematics.md#workspace).

The region is computed from the limits only: the arm's own parts, the tool and the table can block some of it.

The volume the tool can reach.

| Workspace | What it is |
|---|---|
| The **reachable workspace** | Every point it can touch with some orientation: a near-sphere of the reach, minus the base, minus the volume behind the elbow that the limits of joints 2 and 3 exclude |
| The **dexterous workspace** | The part of it where the tool can take any orientation: much smaller, around the middle of the reach and in front of the robot |

A program that needs a particular orientation at a point needs that point in the dexterous workspace. The way to
find out is to jog there and try.

## Payload across the workspace

1 kg close to the base, 0.5 kg at full reach: the torque on joints 2 and 3 grows with the distance, and the
steppers' torque does not. A heavy tool shrinks the workspace in which the arm moves without losing steps.

## Placing the task

Faster cycles and a larger usable workspace come from the layout, not from the program. Put the work:

- in front of the robot, at mid reach;
- at a height that keeps the elbow bent;
- away from the joint 1 axis.

Move the robot or the fixture rather than fighting the kinematics.

The Python API's `reachable()` reports how much travel each joint and axis has left from the current pose, which
tells you how close to a limit the program works.
