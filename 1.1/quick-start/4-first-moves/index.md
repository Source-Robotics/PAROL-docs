# 4. First moves

The robot is on and the software is connected. Now it moves: you jog each joint, home the robot and run a first
program.

!!! danger "Read first"
    PAROL6 has no brakes: when the power goes, the arm falls. It has pinch points, it moves fast, and it moves by
    itself while homing. Anchor it to the table, keep the E-stop within reach, keep hands out of the arm's path, and
    read the [Safety](https://docs.source-robotics.com/PAROL-docs/1.1/02-safety/) chapter: it is five minutes long.

## 1. Jog each joint

Before homing, check that every joint turns the way the software thinks it does. Jog each one briefly, a few
degrees.

The figure shows each joint's positive direction, in colour, over the pose in grey.

![Each joint turned 30 degrees in its positive direction, in colour, over the pose in grey](https://docs.source-robotics.com/PAROL-docs/1.1/assets/kinematics/parol6_joint_directions.webp){ width="900" }
![Each joint turned 30 degrees in its positive direction, in colour, over the pose in grey](https://docs.source-robotics.com/PAROL-docs/1.1/assets/kinematics/parol6_joint_directions_dark.webp){ width="900" }

Until the robot is homed, some joints jog one way only:

| Joint | Jogs | What to check |
|---|---|---|
| **1, 4 and 5** | both ways | It turns as in the figure |
| **2** | only in its **negative** direction | It turns opposite to the figure |
| **3 and 6** | only in their positive direction | It turns as in the figure |

=== "Commander software"

    In the **Joint jog** menu:

    1. Press the left arrow (positive) of joints 1 and 3 to 6, briefly.
    2. Press the right arrow (negative) of joint 2, briefly.

    ![The commander window](https://docs.source-robotics.com/PAROL-docs/1.1/assets/GUI2.webp){ width="800" }

=== "Python API"

    ```python
    rbt.jog_j(0, speed=0.2, duration=0.5)     # joint 1, positive, half a second
    rbt.jog_j(1, speed=-0.2, duration=0.5)    # joint 2, negative
    ```

    The first number is the joint: `0` is joint 1, `5` is joint 6. A negative `speed` jogs the negative way.

A refused jog does not move. The commander logs `Error: Robot jog -> Position out of range`; the Python API
stops the joint before it starts.

??? info "Why some joints jog one way only before homing"
    Before homing, both programs check each jog against the joint limits with a position count that starts at 0
    when the board is switched on. That count puts joint 2 past its positive limit and joints 3 and 6 at or below
    their negative limits.

!!! success "Check"
    Joints 1 and 3 to 6 turned the way the figure shows, and joint 2 turned the opposite way on its negative jog.
    If one did not, fix it before you home. A joint that turns the wrong way is fixed in the firmware, not by
    trial: [A joint turns the wrong way](https://docs.source-robotics.com/PAROL-docs/1.1/build/firmware-and-first-run/#a-joint-turns-the-wrong-way).

More: [Jogging](https://docs.source-robotics.com/PAROL-docs/1.1/05-operation/jogging/) · [Joint limits and directions](https://docs.source-robotics.com/PAROL-docs/1.1/03-technical-data/joint-limits/).

## 2. Home

Homing finds each joint's reference at its limit switch or sensor. Joints 1, 2 and 3 move to their switches
together, then 4, then 6, then 5. The arm ends in the after-homing pose: the standby pose turned 90° about joint 1.

Before you press Home:

1. Turn **joint 6** so that it finds its sensor within one turn in the negative direction. The tool's cables and
   tubes must not be wound up.

    ![Joint 6 before homing: the sensor, the homing pin and the direction of rotation](https://docs.source-robotics.com/PAROL-docs/1.1/assets/J6_home.webp){ width="700" }

    The figure shows the pose: the gripper as drawn, the sensor (blue) and the homing pin (red). Joint 6 turns
    along the green arrow.

2. Mount **the tool**, and check that the firmware's joint 5 homing offset matches it.

    | Tool | `j5_homing_offset` in `main.cpp` |
    |---|---|
    | Pneumatic gripper holder (as shipped) | 8900 |
    | SSG-48 | 8035 |

    Joint 5 homes against a feature of the tool holder. If you change the offset, upload the firmware again as
    in [2. Upload the firmware](https://docs.source-robotics.com/PAROL-docs/1.1/quick-start/2-firmware/) ([Joint 5 and the tool](https://docs.source-robotics.com/PAROL-docs/1.1/05-operation/mastering/#joint-5-and-the-tool)).

3. Stay at the E-stop. A joint that grinds at its end stop has a switch that does not trigger.

Then start the homing:

=== "Commander software"

    Press **Home**.

=== "Python API"

    ```python
    rbt.home(wait=True)
    ```

!!! success "Check"
    Homing finishes, the physical arm matches the simulator, and the pin passes through the witness marks of each
    joint, which line up in the after-homing pose ([Witness marks](https://docs.source-robotics.com/PAROL-docs/1.1/05-operation/mastering/#witness-marks)). If a
    joint keeps travelling or the pose is wrong, stop and use [Homing failures](https://docs.source-robotics.com/PAROL-docs/1.1/08-troubleshooting/homing-failures/).

More: [Homing](https://docs.source-robotics.com/PAROL-docs/1.1/05-operation/homing/) · [Homing failures](https://docs.source-robotics.com/PAROL-docs/1.1/08-troubleshooting/homing-failures/).

## 3. Move it

The robot now knows where it is. Three simple moves: bend the arm a little, turn the base, and come back. The
Python API adds a short straight line down and up from the bent pose.

=== "Commander software"

    1. Paste this program into the program window:

        ```
        Begin()
        MoveJoint(90,-70,160,0,30,180,t=3)
        Delay(1)
        MoveJoint(60,-70,160,0,30,180,t=3)
        Delay(1)
        MoveJoint(90,-90,180,0,0,180,t=3)
        End()
        ```

    2. Press **Start**. **Stop** halts it.

        ![Start and stop](https://docs.source-robotics.com/PAROL-docs/1.1/assets/start_stop.PNG){ width="300" }

    `MoveJoint` takes the six joint angles in degrees; `t=3` makes the move take three seconds. Jogging in the
    Cartesian jog menu moves the tool in straight lines instead.

=== "Python API"

    Type these lines at the `>>>` prompt, one at a time. Each waits until its move is done:

    ```python
    rbt.move_j([90, -70, 160, 0, 30, 180], speed=0.3)       # bend the arm: six joint angles in degrees
    rbt.move_l([0, 0, -30, 0, 0, 0], rel=True, speed=0.3)   # a straight line 30 mm down
    rbt.move_l([0, 0, 30, 0, 0, 0], rel=True, speed=0.3)    # and 30 mm back up
    rbt.move_j([60, -70, 160, 0, 30, 180], speed=0.3)       # turn the base
    rbt.move_j([90, -90, 180, 0, 0, 180], speed=0.3)        # back to the after-homing pose
    ```

    `speed` is a fraction of the maximum: 0.3 is gentle. With `rel=True`, `move_l` takes a change from where the
    tool is: x, y and z in mm in the world frame, then three rotations in degrees.

More: [RBTscript](https://docs.source-robotics.com/PAROL-docs/1.1/programming/03-commander/rbtscript/) · [The Python API](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/).

## 4. Switch off

1. Bring the arm to the **parked pose**: folded in over the base, so that it has the least distance to fall.

    ![The parked pose: the arm folded in over the base](https://docs.source-robotics.com/PAROL-docs/1.1/assets/figures/parol6_parked.webp){ width="420" }
    ![The parked pose: the arm folded in over the base](https://docs.source-robotics.com/PAROL-docs/1.1/assets/figures/parol6_parked_dark.webp){ width="420" }

    === "Commander software"

        Press **Park**: it writes a three-line program into the program window. Press **Start** to run it.

    === "Python API"

        ```python
        rbt.move_j([90, -144.683, 108.171, 2.222, 25.003, 180], speed=0.3)   # the commander's park pose
        ```

        Type `exit()` to leave Python.

2. Hold the forearm.
3. Press the power button. The arm goes limp the moment the motors lose power.

## Where to go next

| You want to | Read |
|---|---|
| attach a gripper | [End effectors](https://docs.source-robotics.com/PAROL-docs/1.1/end-effectors/) |
| write programs | [Programming](https://docs.source-robotics.com/PAROL-docs/1.1/programming/), [RBTscript](https://docs.source-robotics.com/PAROL-docs/1.1/programming/03-commander/rbtscript/), [The Python API](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/) |
| use inputs, outputs, pneumatics | [Peripherals](https://docs.source-robotics.com/PAROL-docs/1.1/06-peripherals/) |
| understand what the robot does and does not protect against | [Safety functions](https://docs.source-robotics.com/PAROL-docs/1.1/02-safety/safety-functions/) |
| fix something | [Troubleshooting](https://docs.source-robotics.com/PAROL-docs/1.1/08-troubleshooting/) |
| look up a command | [API reference](https://docs.source-robotics.com/PAROL-docs/1.1/reference/) |
