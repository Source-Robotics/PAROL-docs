# Jogging

Jogging moves one joint, or the tool along one axis, for as long as you hold a button or repeat a command. It is
how you check a new robot, teach a pose and get out of trouble.

There are two kinds. A joint jog moves one joint, and works before homing. A Cartesian jog moves the tool along
X, Y or Z, or about them, and needs a homed robot.

## Joint jog

=== "Commander software"

    Each joint has a pair of arrows in the commander's **Joint jog** menu.

    - The **left arrow is the positive** direction, the right arrow negative, as in
      [Joint limits and directions](https://docs.source-robotics.com/PAROL-docs/1.1/03-technical-data/joint-limits/).
    - The speed slider sets the speed as a percentage of the commander's jog maximum. That maximum is lower than
      the speed a program may use ([Speeds](https://docs.source-robotics.com/PAROL-docs/1.1/03-technical-data/specifications/#speeds)).

    ![The commander window](https://docs.source-robotics.com/PAROL-docs/1.1/assets/GUI2.webp){ width="800" }

=== "Python API"

    ```python
    rbt.jog_j(0, speed=0.3, duration=0.5)               # joint index 0 = J1, 30 % speed, 0.5 s
    rbt.jog_j(joints=[1, 2], speeds=[0.2, -0.2], duration=1.0)
    ```

    - Joints are indexed from 0 in the API.
    - A jog command runs for `duration`, and the arm brakes to rest when no newer jog arrives.
    - A GUI repeats it while the button is held.

A jog stops at the joint limit.

## Cartesian jog

The tool moves along X, Y or Z, or rotates about them, in the **world frame** (WRF, fixed to the base) or the
**tool frame** (TRF, fixed to the tool). A jog in the tool frame moves the tool along its own axes, which is the
natural way to approach a part.

=== "Commander software"

    The commander's **Cartesian jog** menu has the six pairs of arrows and the WRF/TRF switch.

    ![The Cartesian jog menu](https://docs.source-robotics.com/PAROL-docs/1.1/assets/GUI1.webp){ width="800" }

=== "Python API"

    ```python
    rbt.jog_l("WRF", "X", speed=0.2, duration=0.5)
    rbt.jog_l("TRF", axes=["Z", "RZ"], speeds_list=[0.2, 0.1], duration=0.5)
    ```

A Cartesian jog needs a homed robot.

!!! note "When a Cartesian jog stops: a singularity"
    A Cartesian jog can run into a singularity, where the planner cannot find joint speeds for the tool's motion.
    The commander stops the jog, and the Python API refuses it. Jog a joint away from the singular pose and
    continue ([Configurations and singularities](https://docs.source-robotics.com/PAROL-docs/1.1/theory/configurations-and-singularities/)).

## Jogging a robot that is not homed

Joint jog works before homing: it is how you check the directions on a new build. The positions shown are
meaningless until the robot is homed, and a Cartesian jog is refused.

!!! warning
    Before homing, the limits are checked against a count that does not match the arm, so they do not protect
    the joint: nothing stops it at its real limit except the printed blocker. Jog briefly and slowly.

Until the robot is homed, some joints jog one way only:

| Joint | Jogs before homing |
|---|---|
| **Joints 1, 4 and 5** | Both ways |
| **Joint 2** | Only in its negative direction (the right arrow) |
| **Joints 3 and 6** | Only in their positive direction (the left arrow) |

A refused jog does not move. The commander logs `Error: Robot jog -> Position out of range`; the Python API stops
the joint before it starts.

??? info "Why some joints jog one way only before homing"
    Both programs still check each jog against the joint limits, with a position count that starts at 0 when the
    board is switched on. That count puts joint 2 past its positive limit and joints 3 and 6 at or below their
    negative limits.
