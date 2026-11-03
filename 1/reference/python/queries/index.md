# Queries

Requests with a reply, immediate, returning `None` when no reply arrives in the client's timeout (the TCP queries
raise instead, see [Configuration](https://docs.source-robotics.com/PAROL-docs/1/reference/python/configuration/)). [Status and waiting](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/status-and-waiting/)
in the guide.

### `ping` 

```python
rbt.ping() -> PingResult | None
```

Return parsed ping result with hardware_connected status.

```python
rbt.ping()
```

### `angles` 

```python
rbt.angles() -> list[float] | None
```

Current joint angles in degrees [J1, J2, J3, J4, J5, J6].

```python
angles = rbt.angles()
```

### `pose` 

```python
rbt.pose(frame: str = 'WRF') -> list[float] | None
```

Current TCP pose as [x, y, z, rx, ry, rz] in mm and degrees.

```python
pose = rbt.pose()
```

### `joint_speeds` 

```python
rbt.joint_speeds() -> list[float] | None
```

Current joint velocities in deg/s [J1, J2, J3, J4, J5, J6], the units of `StatusBuffer.speeds`.

```python
speeds = rbt.joint_speeds()
```

### `tcp_speed` 

```python
rbt.tcp_speed() -> float | None
```

TCP linear velocity in mm/s.

```python
speed = rbt.tcp_speed()
```

### `io` 

```python
rbt.io(*, timeout: float | None = None) -> list[int] | None
```

Digital I/O status [in1, in2, out1, out2, estop].

`timeout` bounds setup, retries, and the reply; None uses client defaults.

```python
io = rbt.io()
```

### `status` 

```python
rbt.status() -> StatusSnapshot | None
```

Aggregate status snapshot (pose, angles, speeds, io, tool_status). Its `tool_status` is always a `ToolStatus`, key `"NONE"` when no tool is fitted.

```python
status = rbt.status()
```

### `activity` 

```python
rbt.activity() -> ActivityResult | None
```

What the robot is currently doing.

Returns state (idle/executing/error), current command name, parameters, and error description if applicable.

```python
act = rbt.activity()
```

### `queue` 

```python
rbt.queue() -> list[str] | None
```

Queued command list.

```python
queue = rbt.queue()
```

### `error` 

```python
rbt.error() -> RobotError | None
```

Current error state, or None if no error.

```python
err = rbt.error()
```

### `reachable` 

```python
rbt.reachable() -> EnablementResultStruct | None
```

Remaining freedom of movement per joint/axis before hitting limits.

```python
en = rbt.reachable()
```

### `is_estop_pressed` 

```python
rbt.is_estop_pressed() -> bool
```

Check if E-stop is pressed. Returns True if pressed.

```python
pressed = rbt.is_estop_pressed()
```

### `is_robot_stopped` 

```python
rbt.is_robot_stopped(threshold_speed: float = 0.5) -> bool
```

Check if robot has stopped moving.

Prefer `wait_command()` for waiting on specific commands. This method polls raw joint speeds and is mainly useful for diagnostics or manual stopping logic.

```python
stopped = rbt.is_robot_stopped()
```

| Parameter | Meaning |
|---|---|
| `threshold_speed` | Speed threshold in deg/s |

**Returns:** True if all joints below threshold

### `is_simulator` 

```python
rbt.is_simulator() -> bool
```

Query whether simulator mode is active.

```python
active = rbt.is_simulator()
```

### `tools` 

```python
rbt.tools() -> ToolResult | None
```

Current tool and available tools.

```python
tools = rbt.tools()
```

### `profile` 

```python
rbt.profile() -> str | None
```

Current motion profile name.

```python
profile = rbt.profile()
```

### `shapes` 

```python
rbt.shapes()
```

The collision world the controller is currently enforcing, by layer.

Readback truth for displays; re-query when `StatusBuffer.scene_epoch` changes. Returns None if the controller is unreachable.

```python
world = rbt.shapes()
```

### `execution_speed` 

```python
rbt.execution_speed(*, timeout: float = 3.0) -> ExecutionSpeed
```

Read fresh requested, applied, and retained execution scales.

```python
speed = rbt.execution_speed()
```

### `status_rate` 

```python
rbt.status_rate() -> StatusRate | None
```

Current broadcast rate and the control rate it divides.

```python
rate = rbt.status_rate()
```

### `loop_stats` 

```python
rbt.loop_stats() -> LoopStatsResult | None
```

Fetch control-loop runtime metrics.

```python
stats = rbt.loop_stats()
```

### `reset_loop_stats` 

```python
rbt.reset_loop_stats() -> int
```

Reset control-loop min/max metrics and overrun count.

```python
rbt.reset_loop_stats()
```

## Properties

### `host` (property) 

```python
rbt.host
```

*No docstring.*

### `port` (property) 

```python
rbt.port
```

*No docstring.*

### `robot` (property) 

```python
rbt.robot
```

The backend this client drives, built on first read when a bare client (what a user script constructs) supplied none.

### `tool` (property) 

```python
rbt.tool
```

Active bound tool. Raises if no tool has been set.
