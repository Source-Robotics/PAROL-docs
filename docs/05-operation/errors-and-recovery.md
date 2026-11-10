# Errors and recovery

## What the robot reports

Every 10 ms the control board sends the PC:

- the joints' positions and speeds;
- which joints are homed;
- the state of the inputs, outputs and E-stop;
- the gripper's status;
- two error bytes, reserved for the drivers' temperature and position flags.

The PC software adds its own: inverse kinematics failures, limit violations, timing problems.

## The commander software

The **response log** shows what the robot and the program are doing, and why a command was refused.

![The response log](../assets/response_log.PNG){ width="800" }

The common entries:

| Log | Meaning | What to do |
|---|---|---|
| *Robot disable; button or estop* | The E-stop is open, or Disable was pressed | Release the E-stop; press **Enable** |
| An inverse kinematics error | The target pose has no solution, or lies past a singularity | Change the pose or the approach; move in joint space to get near it |
| A joint limit error | The move would leave a joint's range | Choose a reachable target |
| Jogging stops in Cartesian mode | A singularity | Jog a joint away from it |
| The time between commands rises above 10 ms | The PC cannot keep the 100 Hz loop | Close other programs; a faster PC ([Communication](../08-troubleshooting/communication.md)) |

The three buttons:

| Button | What it does |
|---|---|
| **Enable** | Clears the errors and enables the robot |
| **Clear error** | Resets the homing state, but does not re-enable a disabled robot |
| **Disable** | Stops the firmware from accepting motion commands, while the motors keep holding |

## The Python API

A refused command raises `MotionError` with a code, a cause and a remedy, from the controller's error catalog:
`IK_TARGET_UNREACHABLE`, `MOTN_NOT_HOMED`, `SYS_ESTOP_ACTIVE`, `SYS_SELF_COLLISION`, `MOTN_CANCELLED` and the
others on [Errors](../reference/python/errors.md).

| Call | What it does |
|---|---|
| `error()` | Returns the current error |
| `activity()` | Returns what the robot is doing |
| `reset()` | After an E-stop is released: enables the firmware again. Until then the arm does not move. |

After `stop()` nothing needs clearing.

## After a collision or a stall

The motors have lost steps, and the arm is not where the software says.

1. Stop the program.
2. If the arm is trapped, move it clear: disable it, or switch off with the forearm held.
3. Check the belts and the printed parts.
4. **Home again** before anything else.

## After the arm fell

Power was lost with the arm extended.

1. Check every joint by hand for free movement.
2. Look at the belts and the couplers.
3. Switch on with the forearm held.
4. Home.

## A joint moves the wrong way

On a new build or after work on the wiring:

1. Stop at once.
2. Fix the direction. It is set per joint in the firmware
   ([Firmware and first run](../build/firmware-and-first-run.md#a-joint-turns-the-wrong-way)).
3. Do not try to home until every joint jogs in the right direction.

## The gripper reports an error

The electric grippers report their own errors through the robot: not calibrated, E-stop, timeout. The gripper
manuals explain each error ([SSG-48](../end-effectors/ssg-48.md), [MSG](../end-effectors/msg.md)).

=== "Commander software"

    In the commander's **Gripper** tab:

    1. Press **Clear gripper error**.
    2. Press **Calibrate gripper**.
    3. Wait until the calibration has finished before the first move.

    ![The gripper tab](../assets/parol_grip_gui.PNG){ width="800" }

=== "Python API"

    `tool.calibrate()` calibrates, but the Python API has no clear.
