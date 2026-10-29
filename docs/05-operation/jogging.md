# Jogging

Jogging moves one joint, or the tool along one axis, for as long as you hold a button or repeat a command. It is
how you check a new robot, teach a pose and get out of trouble.

## Joint jog

Each joint has a pair of arrows in the commander's **Joint jog** menu: the **left arrow is the positive**
direction, the right arrow negative, as in [Joint limits and directions](../03-technical-data/joint-limits.md).
The speed slider sets the speed as a percentage of the joint's maximum. A jog stops at the joint limit.

=== "Python API"
    ```python
    rbt.jog_j(0, speed=0.3, duration=0.5)               # joint index 0 = J1, 30 % speed, 0.5 s
    rbt.jog_j(joints=[1, 2], speeds=[0.2, -0.2], duration=1.0)
    ```
    A jog command runs for `duration` and the arm brakes to rest when no newer jog arrives; a GUI repeats it while
    the button is held. Joints are indexed from 0 in the API.

## Cartesian jog

The tool moves along X, Y or Z, or rotates about them, in the **world frame** (WRF, fixed to the base) or the
**tool frame** (TRF, fixed to the tool). The commander's **Cartesian jog** menu has the six pairs of arrows and
the WRF/TRF switch; a jog in the tool frame moves the tool along its own axes, which is the natural way to
approach a part.

=== "Python API"
    ```python
    rbt.jog_l("WRF", "X", speed=0.2, duration=0.5)
    rbt.jog_l("TRF", axes=["Z", "RZ"], speeds_list=[0.2, 0.1], duration=0.5)
    ```

A Cartesian jog needs a homed robot, and it can run into a singularity, where the planner cannot find joint
speeds for the tool's motion: the commander stops the jog, and the Python API refuses it. Jog a joint away from
the singular pose and continue ([Configurations and singularities](../programming/02-concepts/configurations-and-singularities.md)).

## Jogging a robot that is not homed

Joint jog works before homing: it is how you check the directions on a new build. The positions shown are
meaningless until the robot is homed, the limits are not enforced, and a Cartesian jog is refused.

!!! warning
    Before homing, nothing stops a joint at its limit except the printed blocker. Jog briefly and slowly.
