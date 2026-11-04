# Workspace and reach

## Reach

The furthest the flange centre gets from the axis of joint 1, within the [joint limits](https://docs.source-robotics.com/PAROL-docs/1.1/03-technical-data/joint-limits/):
408 mm. The standard pneumatic gripper's tool centre point gets to 434 mm. A longer tool reaches further and
weighs on joints 4 and 5.

## Workspace

![Where the flange centre can go within the joint limits, side and top view, in mm](https://docs.source-robotics.com/PAROL-docs/1.1/assets/figures/parol6_workspace_flange.webp){ width="900" }
![Where the flange centre can go within the joint limits, side and top view, in mm](https://docs.source-robotics.com/PAROL-docs/1.1/assets/figures/parol6_workspace_flange_dark.webp){ width="900" }

In the side view the shaded region is everywhere the centre of the flange can go in the plane of the arm, within
the joint limits of the robot's model; the dotted line is the same for the wrist centre. It reaches 408 mm in
front of the joint 1 axis and 359 mm behind it, 523 mm above the mounting surface and 25 mm below it. The top view
sweeps that region about joint 1 through its ±97.4°: in front of the base the arm reaches out directly, behind it
(lighter) only by folding back over the base. A tool adds its own length; the same figure for each gripper, with
a table of the numbers, is on [Dimensions and kinematics](https://docs.source-robotics.com/PAROL-docs/1.1/03-technical-data/kinematics/#workspace). The
region is computed from the limits only: the arm's own parts, the tool and the table can block some of it.

The volume the tool can reach. The **reachable workspace** is every point it can touch with some orientation: a
near-sphere of the reach, minus the base, minus the volume behind the elbow that the limits of joints 2 and 3
exclude. The **dexterous workspace** is the part of it where the tool can take any orientation, much smaller,
around the middle of the reach and in front of the robot. A program that needs a particular orientation at a
point needs that point in the dexterous workspace, and the way to find out is to jog there and try.

## Payload across the workspace

1 kg close to the base, 0.5 kg at full reach: the torque on joints 2 and 3 grows with the distance, and the
steppers' torque does not. A heavy tool shrinks the workspace in which the arm moves without losing steps.

## Placing the task

Faster cycles and a larger usable workspace come from the layout, not from the program: put the work in front of
the robot at mid reach, at a height that keeps the elbow bent, and away from the joint 1 axis. Move the robot or
the fixture rather than fighting the kinematics. The Python API's `reachable()` reports how much travel each joint
and axis has left from the current pose, which tells you how close to a limit the program works.
