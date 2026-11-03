# Control

Commands that change what the controller is doing: stops, the protective stop and its reset, pause and execution
speed, simulator mode, teleport, and the state reset. They are system commands: immediate, not queued, and
accepted also while the controller is disabled, except `teleport`, which is refused then. [Control ownership](https://docs.source-robotics.com/PAROL-docs/1/theory/control-ownership/).

### `stop` 

```python
rbt.stop() -> int
```

Stop all motion — cancel the active move and clear the queue.

The controller stays enabled and holding position; the next motion command is accepted immediately.

```python
rbt.stop()
```

**Returns:** 1 if acknowledged, 0 on failure.

### `estop` 

```python
rbt.estop() -> int
```

Protective stop: stop all motion and latch the controller disabled until `reset()`.

```python
rbt.estop()
```

**Returns:** 1 if acknowledged, 0 on failure.

### `reset` 

```python
rbt.reset() -> int
```

Clear a latched protective stop, re-enabling motion.

```python
rbt.reset()
```

**Returns:** 1 if acknowledged, 0 on failure.

### `reset_state` 

```python
rbt.reset_state() -> int
```

Reset program state — world shapes, tool selection, errors, pause, motion profile and execution speed — and discard the queue, each discarded command failing with `MOTN_CANCELLED`.

The arm holds where it is. A protective stop stays latched (only `reset()` clears it), and homed state, digital outputs and the serial connection are kept.

```python
rbt.reset_state()
```

### `pause` 

```python
rbt.pause(*, timeout: float = 3.0) -> int
```

Request a controlled hold, retaining queued trajectory progress.

A confirmed request returns 1. Read `execution_speed().paused` to confirm the hold. Standalone Python completion timeouts continue.

```python
rbt.pause()
```

### `resume` 

```python
rbt.resume(*, timeout: float = 3.0) -> int
```

Resume the retained queue at its selected positive speed.

```python
rbt.resume()
```

### `set_execution_speed` 

```python
rbt.set_execution_speed(scale: float, *, timeout: float = 3.0) -> int
```

Select 10–100% of planned queued-motion speed, preserving pause.

```python
rbt.set_execution_speed(0.5)
```

### `simulator` 

```python
rbt.simulator(enabled: bool) -> int
```

Enable or disable simulator mode.

```python
rbt.simulator(True)
```

### `teleport` 

```python
rbt.teleport(angles_deg: list[float], tool_positions: list[float] | None = None) -> int
```

Instantly set joint angles and optional tool positions (simulator only).

The pose is exact, so the arm counts as homed afterwards and planned motion may follow. Whatever was driving the arm is cancelled with `MOTN_CANCELLED`.

```python
rbt.teleport([90, -90, 180, 0, 0, 180])
rbt.teleport([90, -90, 180, 0, 0, 180], tool_positions=[1.0])
```

**Returns:** 1 once the pose is applied, 0 when no reply arrives.

**Raises:**

- `ValueError`: for a non-finite angle, one outside the hard joint limits, or a tool position outside `[0, 1]`.
- `MotionError`: off the simulator (`SYS_NOT_SIMULATOR`), when the tool positions do not match the fitted tool's DOF count, or while the controller is disabled.

### `run_skill` 

```python
rbt.run_skill(invoke: Callable[[AsyncRobotClient], Coroutine[Any, Any, T]]) -> T
```

Execute a Python skill using this connection and its existing loop.

!!! note
    Skills are decorated Python functions from the waldoctl skill runtime, run on the connected client; Waldo
    Commander uses them. A plain script does not need them.

### `close` 

```python
rbt.close() -> None
```

Release UDP transport and background tasks.

Safe to call multiple times.
