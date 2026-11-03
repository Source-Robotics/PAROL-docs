# Errors and recovery

## What the robot reports

Every 10 ms the control board sends the PC the joints' positions and speeds, which joints are homed, the state of
the inputs, outputs and E-stop, the gripper's status, and two error bytes reserved for the drivers' temperature
and position flags. The PC software adds its own: inverse kinematics failures, limit violations, timing problems.

## The commander software

The **response log** shows what the robot and the program are doing and why a command was refused. The common
entries:

| Log | Meaning | What to do |
|---|---|---|
| *Robot disable; button or estop* | The E-stop is open, or Disable was pressed | Release the E-stop; press **Enable** |
| An inverse kinematics error | The target pose has no solution, or lies past a singularity | Change the pose or the approach; move in joint space to get near it |
| A joint limit error | The move would leave a joint's range | Choose a reachable target |
| Jogging stops in Cartesian mode | A singularity | Jog a joint away from it |
| The time between commands rises above 10 ms | The PC cannot keep the 100 Hz loop | Close other programs; a faster PC ([Communication](https://docs.source-robotics.com/PAROL-docs/1/08-troubleshooting/communication/)) |

**Enable** clears the errors and enables the robot; **Clear error** resets the homing state but does not re-enable
a disabled robot; **Disable** stops the firmware from accepting motion commands while the motors keep holding.

## The Python API

A refused command raises `MotionError` with a code, a cause and a remedy, from the controller's error catalog:
`IK_TARGET_UNREACHABLE`, `MOTN_NOT_HOMED`, `SYS_ESTOP_ACTIVE`, `SYS_SELF_COLLISION`, `MOTN_CANCELLED` and the
others on [Errors](https://docs.source-robotics.com/PAROL-docs/1/reference/python/errors/). `error()` returns the current error, `activity()` what the
robot is doing. After an E-stop is released, call `reset()`: it enables the firmware again, and until then the arm
does not move. After `stop()` nothing needs clearing.

## After a collision or a stall

The motors have lost steps and the arm is not where the software says. Stop the program, move the arm clear if
it is trapped (disable it, or switch off with the forearm held), check the belts and the printed parts, and
**home again** before anything else.

## After the arm fell

Power was lost with the arm extended. Check every joint by hand for free movement, look at the belts and the
couplers, switch on with the forearm held, and home.

## A joint moves the wrong way

On a new build or after work on the wiring: stop at once. The direction is set per joint in the firmware
([Firmware and first run](https://docs.source-robotics.com/PAROL-docs/1/build/firmware-and-first-run/#a-joint-turns-the-wrong-way)); do not try to home
until every joint jogs in the right direction.

## The gripper reports an error

The electric grippers report their own errors through the robot: not calibrated, E-stop, timeout. The commander's
**Gripper** tab has **Clear gripper error** and **Calibrate gripper**: clear the error first, then calibrate,
and wait until the calibration has finished before the first move. The Python API's `tool.calibrate()`
calibrates but has no clear ([SSG-48](https://docs.source-robotics.com/PAROL-docs/1/end-effectors/ssg-48/), [MSG](https://docs.source-robotics.com/PAROL-docs/1/end-effectors/msg/)). The gripper
manuals explain each error.
