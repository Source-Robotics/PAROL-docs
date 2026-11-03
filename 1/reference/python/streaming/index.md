# Jogging and servoing

Streamed motion: takes the arm at once and cancels the planned queue (`MOTN_CANCELLED` for every discarded
command). A jog ends when its `duration` runs out; a servo stream ends about 0.25 s after the last target. Then
the arm brakes to rest. Speeds are signed fractions in [−1, 1] for jogs and fractions in (0, 1] for servo
targets. `jog_j` works before homing; `jog_l` and the servo targets need a homed robot.
[Jogging and servoing](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/streaming/) in the guide.

### `jog_j` 

```python
rbt.jog_j(
    joint: int | None = None,
    speed: float = 0.0,
    duration: float = 0.1,
    *,
    joints: list[int] | None = None,
    speeds: list[float] | None = None,
    accel: float = 0.5,
) -> int
```

Joint velocity jog. Single-joint or multi-joint.

Single joint:   jog_j(0, 0.5, 1.0) Multi joint:    jog_j(joints=[0,1], speeds=[0.5, -0.3], duration=1.0)

```python
rbt.jog_j(0, speed=0.5, duration=1.0)
```

| Parameter | Meaning |
|---|---|
| `joint` | Joint index (0-5) for single-joint jog |
| `speed` | Signed speed fraction for single-joint jog |
| `duration` | Jog duration in seconds |
| `joints` | List of joint indices for multi-joint jog |
| `speeds` | List of signed speed fractions for multi-joint jog |
| `accel` | Acceleration fraction 0-1 |

### `jog_l` 

```python
rbt.jog_l(
    frame: Frame,
    axis: Axis | None = None,
    speed: float = 0.0,
    duration: float = 0.1,
    *,
    axes: list[Axis] | None = None,
    speeds_list: list[float] | None = None,
    accel: float = 0.5,
) -> int
```

Cartesian velocity jog. Single-axis or multi-axis.

Single axis:  jog_l("WRF", "X", 0.5, 1.0) Multi axis:   jog_l("WRF", axes=["X","Y"], speeds_list=[0.5, -0.3], duration=1.0)

```python
rbt.jog_l("WRF", "X", speed=0.5, duration=1.0)
```

| Parameter | Meaning |
|---|---|
| `frame` | Reference frame ("WRF" or "TRF") |
| `axis` | Axis name for single-axis jog |
| `speed` | Signed speed fraction for single-axis jog |
| `duration` | Jog duration in seconds |
| `axes` | List of axis names for multi-axis jog |
| `speeds_list` | List of signed speed fractions for multi-axis jog |
| `accel` | Acceleration fraction 0-1 |

!!! note
    Axis names: `X`, `Y`, `Z`, `RX`, `RY`, `RZ`; frames `WRF` and `TRF`. Jogs are clamped to 80 % of the limits.

### `servo_j` 

```python
rbt.servo_j(
    angles: list[float] | None = None,
    *,
    pose: list[float] | None = None,
    speed: float = 0.5,
    accel: float = 0.5,
) -> int
```

Streaming joint position target. Fire-and-forget.

The stream stops about 0.25 s after the last target arrives: the arm brakes to rest and holds there.

```python
rbt.servo_j([90, -90, 180, 0, 0, 180])
```

| Parameter | Meaning |
|---|---|
| `angles` | 6 joint angles in degrees (ignored if pose= is set) |
| `pose` | If set, Cartesian target — dispatches to SERVOJ_POSE |
| `speed` | Speed fraction 0-1 |
| `accel` | Acceleration fraction 0-1 |

### `servo_l` 

```python
rbt.servo_l(pose: list[float], *, speed: float = 0.5, accel: float = 0.5) -> int
```

Streaming linear Cartesian position target. Fire-and-forget.

The stream stops about 0.25 s after the last target arrives: the tool brakes along its line to rest and holds there.

```python
rbt.servo_l([0, 263, 242, 90, 0, 90])
```

| Parameter | Meaning |
|---|---|
| `pose` | Target [x,y,z,rx,ry,rz] in mm and degrees |
| `speed` | Speed fraction 0-1 |
| `accel` | Acceleration fraction 0-1 |

### `stream_status` (async client only) 

```python
rbt.stream_status() -> AsyncIterator[StatusBuffer]
```

Async generator that yields status updates from multicast broadcasts.

```python
async for status in client.stream_status():
    print(f"Angles: {status.angles}")
```

This generator terminates automatically when `close` is called on the client, so callers do not need to manually cancel their consumer tasks.

Each yielded StatusBuffer is a copy - safe to store or process async. For zero-copy hot paths, use `stream_status_shared` instead.

Slow consumers automatically skip to the latest state (desired for real-time).

### `stream_status_shared` (async client only) 

```python
rbt.stream_status_shared() -> AsyncIterator[StatusBuffer]
```

Zero-copy async generator that yields the shared status buffer.

```python
async for status in client.stream_status_shared():
    # Process immediately - don't store references
    print(f"Angles: {status.angles}")
```

WARNING: The same buffer instance is yielded on every iteration. Do not store references to the yielded object - data will be overwritten on the next iteration. For safe storage, use `stream_status` or call status.copy().

This generator terminates automatically when `close` is called on the client.

Slow consumers automatically skip to the latest state (desired for real-time).
