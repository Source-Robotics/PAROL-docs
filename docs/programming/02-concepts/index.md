# 2. Concepts

The vocabulary of the robot's software, explained in the order you meet it: what a joint angle and a pose are,
which frames the numbers are in, how the software goes from one to the other, why some poses cannot be reached
and some moves cannot be made, what shape a move has in time, and who is in charge of the robot at any moment.
Each page says how the concept shows up in PAROL6's software. None of it needs maths beyond what is on the page.

## In this chapter

- [Units](units.md)
- [Joints, directions and the standby pose](joints-and-poses.md)
- [Reference frames](reference-frames.md)
- [Pose and orientation](pose-and-orientation.md)
- [Forward and inverse kinematics](kinematics.md)
- [Configurations and singularities](configurations-and-singularities.md)
- [Workspace and reach](workspace-and-reach.md)
- [Homing and mastering](homing-and-mastering.md)
- [Motion profiles](motion-profiles.md)
- [Blending](blending.md)
- [Target, commanded and actual](target-commanded-actual.md)
- [Control ownership](control-ownership.md)
- [Steppers, open loop and backlash](steppers-and-open-loop.md)
- [Further reading](further-reading.md)

## Robot types

Industrial robots are sorted by their joints and how they are arranged: vertically articulated arms, Cartesian
gantries, cylindrical and polar arms, SCARA arms, delta robots. PAROL6 is a **vertically articulated** arm with
six revolute joints, the most common industrial type, and the concepts in this chapter are the ones every such
arm uses. The last three joints meet in a point, a **spherical wrist**, which the pages on kinematics return to.

![A robot with a spherical wrist (left) and one without (right)](../../assets/spherical.png){ width="650" }
