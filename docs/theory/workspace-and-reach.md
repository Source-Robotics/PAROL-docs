# Workspace and reach

## Reach

The furthest the tool centre point gets from the axis of joint 1: 400 mm with the standard pneumatic gripper,
about 338 mm to the flange. A longer tool reaches further and weighs on joints 4 and 5.

## Workspace

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
