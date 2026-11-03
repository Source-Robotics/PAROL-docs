# Synchronization

Waiting for the controller, for a command, for a checkpoint or for the arm to come to rest; and the two queued
markers, delays and checkpoints. [Status and waiting](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/status-and-waiting/) in the
guide says what "done" means.

### `wait_ready` 

```python
rbt.wait_ready(timeout: float = 5.0, interval: float = 0.05) -> bool
```

Poll ping() until server responds or timeout.

| Parameter | Meaning |
|---|---|
| `timeout` | Maximum time to wait for server to respond |
| `interval` | Polling interval between ping attempts |

**Returns:** True if server responded to PING, False on timeout

### `wait_command` 

```python
rbt.wait_command(command_index: int, timeout: float = 10.0) -> bool
```

Wait until a specific command index has been completed.

Queries exact success in the controller's last 1024 completions: a later command that finishes first — a jog, a `tool.stop()` — does not complete an unfinished one queued before it. Queued commands, tool actions among them, run in index order, so a wait on one covers everything queued ahead of it. Unknown or expired results are never inferred successful from the status high-water mark. A command that ended as a failure — cancelled by `stop()`/`estop()` (`MOTN_CANCELLED`) or failed by the pipeline — raises MotionError.

| Parameter | Meaning |
|---|---|
| `command_index` | The command index to wait for (returned by motion commands). |
| `timeout` | Maximum time to wait in seconds. |

**Returns:** True if the command completed within timeout, False otherwise.

**Raises:**

- `MotionError`: If the pipeline errored at or before command_index.

### `wait_motion` 

```python
rbt.wait_motion(
    timeout: float = 10.0,
    settle_window: float = 0.25,
    speed_threshold: float = 0.5,
    angle_threshold: float = 0.5,
) -> bool
```

Wait until the queue has run out and the arm has come to rest.

First waits for the latest command the controller has accepted — every command this client queued, and each newer one the status stream reports accepted — to end, then for the arm to hold still for `settle_window`. A command that failed or was cancelled ends the wait like one that completed; `wait_command()` tells which.

```python
rbt.wait_motion()
```

| Parameter | Meaning |
|---|---|
| `timeout` | Maximum time to wait in seconds |
| `settle_window` | How long robot must be stable to be considered stopped |
| `speed_threshold` | Max joint speed to be considered stopped (deg/s) |
| `angle_threshold` | Max angle change to be considered stopped (degrees) |

**Returns:** True if robot stopped, False if timeout

**Raises:**

- `ConnectionError`: If the controller session changes while a command is still being waited on.

### `wait_status` 

```python
rbt.wait_status(predicate: Callable[[StatusBuffer], bool], timeout: float = 5.0) -> bool
```

Wait until a multicast status satisfies predicate(status) within timeout.

### `checkpoint` 

```python
rbt.checkpoint(label: str) -> int
```

Insert a checkpoint marker in the motion queue.

Returns the command index (≥ 0) on success, -1 on failure.

```python
rbt.checkpoint("pick_done")
```

| Parameter | Meaning |
|---|---|
| `label` | Checkpoint label for progress tracking |

### `wait_checkpoint` 

```python
rbt.wait_checkpoint(label: str, timeout: float = 30.0) -> bool
```

Wait until a checkpoint with the given label has been reached.

```python
rbt.wait_checkpoint("pick_done")
```

| Parameter | Meaning |
|---|---|
| `label` | Checkpoint label to wait for |
| `timeout` | Maximum wait time in seconds |

### `delay` 

```python
rbt.delay(seconds: float) -> int
```

Insert a non-blocking delay in the motion queue.

Returns the command index (≥ 0) on success, -1 on failure.

```python
rbt.delay(1.0)
```
