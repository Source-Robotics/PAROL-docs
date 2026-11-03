# Errors

## MotionError

A command the controller refuses or fails raises `MotionError`, carrying a `RobotError` with a code, a title, a
cause, an effect and a remedy from the controller's catalog:

```python
from parol6 import RobotClient, MotionError

with RobotClient() as rbt:
    try:
        rbt.move_l([900, 0, 0, 0, 0, 0], speed=0.5)
    except MotionError as e:
        print(e)            # IK: target unreachable — ... — Verify target is within workspace...
```

The codes are on [Errors](https://docs.source-robotics.com/PAROL-docs/1/reference/python/errors/). The ones you meet first:

| Code | When |
|---|---|
| `MOTN_NOT_HOMED` | Planned motion before the robot is referenced: `home()` first |
| `IK_TARGET_UNREACHABLE`, `IK_PARTIAL_PATH` | The pose, or part of a Cartesian path, has no solution |
| `SYS_ESTOP_ACTIVE` | The E-stop is pressed or a protective stop is latched: release, then `reset()` |
| `SYS_CONTROLLER_DISABLED` | The controller is disabled |
| `SYS_SELF_COLLISION` | The path collides with the robot itself or with a declared shape |
| `MOTN_CANCELLED` | The command was discarded by `stop()`, an E-stop, a stream taking the arm, a teleport, or a failure ahead of it in the queue |
| `COMM_VALIDATION_ERROR`, `COMM_DECODE_ERROR` | A malformed command; usually a version mismatch between client and controller |

`error()` returns the current error, `activity()` the state with the error description, and the status stream
carries `error`.

## ValueError and TimeoutError

The client checks parameters before sending: a wrong number of angles, a speed outside (0, 1], a non-finite
value, an unknown tool action raise `ValueError` locally. A blocking call whose completion is not confirmed in
its `timeout` raises `TimeoutError`; the command stays queued, and `stop()` cancels it. A query that gets no
reply returns `None`, except the TCP queries and bounded I/O writes, which raise rather than report a misleading
value.

## ConnectionError

A controller restart during a wait changes the session, and the wait raises `ConnectionError`: the index you
were waiting for belongs to a controller that no longer exists.

## Recovering

| After | Do |
|---|---|
| `stop()` | Nothing: the controller is enabled and holding; queue again |
| `estop()` or the E-stop button | Release the button; `reset()` |
| `reset_state()` | The shapes, tool, errors, pause, profile and speed are back to defaults; select the tool again; a protective stop stays until `reset()` |
| A collision or stall on the hardware | Stop; move the arm clear; `home(calibrate=True)` |
| A failed command in the queue | Everything behind it was cancelled: re-queue from the failed one |
