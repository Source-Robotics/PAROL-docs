# Status and waiting

## Queries

Every query is a request to the controller with a reply, returning `None` on a timeout:

```python
rbt.ping()            # PingResult: hardware_connected
rbt.angles()          # [J1..J6] in degrees
rbt.pose()            # [x, y, z, rx, ry, rz], mm and degrees; pose("TRF") in the tool frame
rbt.joint_speeds()    # deg/s
rbt.tcp_speed()       # mm/s
rbt.io()              # [in1, in2, out1, out2, estop]
rbt.status()          # StatusSnapshot: pose, angles, speeds, io, tool_status
rbt.activity()        # what the robot does now: state, command, parameters, error
rbt.queue()           # the queued commands
rbt.error()           # the current RobotError, or None
rbt.reachable()       # remaining travel per joint and axis
rbt.tools(); rbt.profile(); rbt.tcp_offset(); rbt.tcp_transform(); rbt.shapes()
rbt.loop_stats(); rbt.status_rate(); rbt.execution_speed(); rbt.is_simulator()
```

## The status stream

The controller broadcasts its state at 50 Hz (`set_status_rate()` changes it) as multicast; the async client
yields it as a stream:

```python
async for s in rbt.stream_status():
    s.angles, s.speeds, s.pose, s.io, s.tool_status
    s.action_state, s.action_current, s.executing_index, s.completed_index, s.accepted_index
    s.error, s.homed, s.enabled, s.simulator_active, s.collision_active
    s.session_id, s.seq, s.mono_time_ns          # for recording: a session, a sequence, a timestamp
```

The fields are listed on [Status fields](https://docs.source-robotics.com/PAROL-docs/1/reference/python/status/). `seq` gaps mean missed broadcasts;
`session_id` changes when the controller restarts; `mono_time_ns` is the time of the controller's snapshot, not
of the sensor reading. The sync client's `wait_status(predicate)` waits for a status that satisfies a function.

## Waiting for a command

```python
index = rbt.move_l(target, wait=False)
ok = rbt.wait_command(index, timeout=10)        # True when completed; raises MotionError if it failed
```

`wait_command` asks the controller for that command's exact result. Queued commands run in index order, so a
wait on one covers everything queued before it; a jog or a `tool.stop()` can finish earlier than something queued
before it, which is why a wait never infers success from the highest completed index. A command discarded by
`stop()`, an E-stop, `reset_state()`, a teleport or a failure ahead of it raises `MotionError` with
`MOTN_CANCELLED` at once; an unknown or expired result stays unconfirmed and the wait returns `False` at its
timeout. The controller keeps its last 1024 completions and 1024 failures.

`wait_motion()` waits for the whole queue to run out and the arm to hold still for a settle window; `wait_ready()`
polls `ping()` until the controller answers; `is_robot_stopped()` looks at the joint speeds only.

## What "done" means

A blocking move returns when the controller reports the command complete: the trajectory played to its end and
the arm at the commanded position, in counted steps. For a tool action, when the gripper's estimated travel
time or its reported state says so. Neither is a measurement of the world: a program that needs to know the
part is in the gripper checks where the jaws stopped (`tool.status().positions`) or reads a sensor. For the electric
grippers, the tool status's `part_detected` does not follow the gripper's object-detection bits at this version
([Tool status](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/tools-and-tcp/#tool-status)).
