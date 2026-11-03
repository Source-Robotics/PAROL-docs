# Theory corner

The theory behind a six-axis robot arm and its software, explained in the order you meet it: what a joint angle and a pose are,
which frames the numbers are in, how the software goes from one to the other, why some poses cannot be reached
and some moves cannot be made, what shape a move has in time, and who is in charge of the robot at any moment.
Each page says how the idea shows up in PAROL6's software. None of it needs maths beyond what is on the page,
and none of it is needed to run the robot: read it when you want to know why the robot does what it does.

## The pages

- [Units](https://docs.source-robotics.com/PAROL-docs/1/theory/units/)
- [Joints, directions and the standby pose](https://docs.source-robotics.com/PAROL-docs/1/theory/joints-and-poses/)
- [Reference frames](https://docs.source-robotics.com/PAROL-docs/1/theory/reference-frames/)
- [Pose and orientation](https://docs.source-robotics.com/PAROL-docs/1/theory/pose-and-orientation/)
- [Forward and inverse kinematics](https://docs.source-robotics.com/PAROL-docs/1/theory/kinematics/)
- [Configurations and singularities](https://docs.source-robotics.com/PAROL-docs/1/theory/configurations-and-singularities/)
- [Workspace and reach](https://docs.source-robotics.com/PAROL-docs/1/theory/workspace-and-reach/)
- [Homing and mastering](https://docs.source-robotics.com/PAROL-docs/1/theory/homing-and-mastering/)
- [Motion profiles](https://docs.source-robotics.com/PAROL-docs/1/theory/motion-profiles/)
- [Blending](https://docs.source-robotics.com/PAROL-docs/1/theory/blending/)
- [Target, commanded and actual](https://docs.source-robotics.com/PAROL-docs/1/theory/target-commanded-actual/)
- [Control ownership](https://docs.source-robotics.com/PAROL-docs/1/theory/control-ownership/)
- [Steppers, open loop and backlash](https://docs.source-robotics.com/PAROL-docs/1/theory/steppers-and-open-loop/)
- [Further reading](https://docs.source-robotics.com/PAROL-docs/1/theory/further-reading/)

## Robot types

Industrial robots are sorted by their joints and how they are arranged: vertically articulated arms, Cartesian
gantries, cylindrical and polar arms, SCARA arms, delta robots. PAROL6 is a **vertically articulated** arm with
six revolute joints, the most common industrial type, and the ideas on these pages are the ones every such
arm uses. The last three joints meet in a point, a **spherical wrist**, which the pages on kinematics return to.

![A robot with a spherical wrist (left) and one without (right)](https://docs.source-robotics.com/PAROL-docs/1/assets/spherical.png){ width="650" }
