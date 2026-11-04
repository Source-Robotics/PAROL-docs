# Errors

The error codes of the controller, with the catalog text a `MotionError` carries, from the source at
v0.9.1. The number ranges: 10 to 19 inverse kinematics, 20 to 29 trajectory planning, 30 to 39
motion execution, 40 to 49 communication, 50 to 59 system and safety. `MOTN_CANCELLED` uses the number shared
with the waldoctl interface, so that a client sees one code for a discarded command whichever arm raised it.
[Errors](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/errors/) in the guide says how to recover.

| Code | Number | Title | Cause | Effect | Remedy |
|---|---|---|---|---|---|
| `IK_TARGET_UNREACHABLE` | 10 | IK: target unreachable | Target pose has no valid IK solution. {detail} | Motion command rejected. Pipeline halted. | Verify target is within workspace. Try different orientation. |
| `IK_PARTIAL_PATH` | 11 | IK: partial path failure | Only {valid}/{total} poses along the path are reachable. | Motion command rejected. Pipeline halted. | Shorten the move, add intermediate waypoints, or adjust orientation. |
| `TRAJ_EMPTY_RESULT` | 20 | Trajectory: empty result | Trajectory generation returned no waypoints. {detail} | Motion command rejected. | Check motion parameters. Start and end may be too close. |
| `TRAJ_NO_STEPS` | 21 | Trajectory: no steps | Trajectory calculation produced zero steps. {detail} | Motion command rejected. | Increase duration or reduce speed fraction. |
| `MOTN_HOME_TIMEOUT` | 30 | Homing timeout | Robot did not start homing sequence within timeout. | Home command aborted. | Check serial connection and robot power. Ensure E-stop is released. |
| `MOTN_GRIPPER_TIMEOUT` | 31 | Gripper timeout | Gripper command timed out in state {state}. | Gripper command aborted. | Check gripper connection and calibration. |
| `MOTN_GRIPPER_UNKNOWN` | 32 | Gripper: unknown state | Gripper entered an unknown internal state. | Gripper command aborted. | Reset the controller and recalibrate the gripper. |
| `MOTN_SETUP_FAILED` | 33 | Command setup failed | Command could not be initialized. {detail} | Command rejected. Pipeline halted. | Check command parameters and robot state. |
| `MOTN_TICK_FAILED` | 34 | Command execution error | Unexpected error during execution. {detail} | Command aborted. Robot stopped. | Check robot state. May need to re-home. |
| `MOTN_NOT_HOMED` | 35 | Robot not homed |  |  |  |
| `MOTN_CANCELLED` | shared | Command cancelled | The command was cancelled by {scope} before it finished. | The motion did not run to completion. | Re-issue the command if the motion is still wanted. |
| `COMM_QUEUE_FULL` | 40 | Command queue full | Motion queue at maximum capacity. | Command rejected. | Wait for current motions to complete. |
| `COMM_UNKNOWN_COMMAND` | 41 | Unknown command | No handler for received command type. | Command ignored. | Check client library version matches server. |
| `COMM_DECODE_ERROR` | 42 | Command decode error | Failed to decode command. {detail} | Command ignored. | Check command encoding. Possible version mismatch. |
| `COMM_VALIDATION_ERROR` | 43 | Command validation error | Invalid parameters. {detail} | Command rejected. | Check parameter ranges and types. |
| `SYS_STATUS_RATE_INVALID` | 55 | Status rate not achievable | Status is broadcast every Nth control tick, so {requested} Hz does not divide the {control} Hz control loop evenly. | Broadcast rate unchanged. | Pick a rate that divides {control} Hz: {allowed}. |
| `SYS_CONTROLLER_DISABLED` | 50 | Controller disabled | Motion command sent while controller is disabled. {detail} | Command rejected. | Call reset() to re-enable the controller. |
| `SYS_ESTOP_ACTIVE` | 51 | E-stop active | Emergency stop is currently engaged. | All motion stopped. Queue cleared. | Release the E-stop button and call reset(). |
| `SYS_PORT_SAVE_FAILED` | 52 | Serial port save failed | Could not save serial port configuration. | Port may not persist across restarts. | Check file permissions and disk space. |
| `SYS_PROFILE_INVALID` | 53 | Invalid motion profile | Unrecognized motion profile: {detail} | Profile not changed. | Use one of: TOPPRA, RUCKIG, QUINTIC, TRAPEZOID, LINEAR. |
| `SYS_NOT_SIMULATOR` | 56 | Simulator-only command | {detail} is only available on the simulator. | Command rejected; the arm is unchanged. | Switch to the simulator with simulator(True), or drive the arm with a planned move. |
| `SYS_SELF_COLLISION` | 54 | Self-collision predicted | Planned configuration would self-collide at sample {sample} of {total}: {pairs} | Motion command rejected before dispatch. | Choose a different target, add intermediate waypoints, or disable via PAROL6_COLLISION_CHECK=0. |

A `RobotError` has the fields `code`, `title`, `cause`, `effect` and `remedy`, and `str(error)` joins them.
