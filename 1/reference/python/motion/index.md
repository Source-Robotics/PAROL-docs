# Motion

Planned moves: queued, run in order, each returning its command index. `wait=True` (the default) blocks until the
command completes and raises `MotionError` if it failed or was cancelled; `wait=False` returns at once for a later
`wait_command()`. Either `duration` or `speed` times a move, not both. [Motion](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/motion/)
in the guide explains the choices.

### `home` 

```python
rbt.home(wait: bool = False, calibrate: bool = False, timeout: float = 60.0) -> int
```

Home the robot to its home position.

Uncalibrated (first home after power-on), this runs the full referencing sequence: each joint seeks its limit switch, then the robot moves to standby. Calibrated, it returns to standby with a normal planned, collision-checked joint move — unless `calibrate=True`, which re-runs the referencing sequence. The referencing sequence is firmware-driven and ignores the collision world, so clear keep-out geometry from the joints' sweep first.

Returns the command index (≥ 0) on success, -1 on failure.

```python
rbt.home()
```

| Parameter | Meaning |
|---|---|
| `wait` | If True, block until motion completes |
| `calibrate` | If True, always run the referencing sequence |
| `timeout` | Maximum time to wait in seconds (only used when wait=True) |

!!! note
    The referencing sequence is the firmware's ([Homing](https://docs.source-robotics.com/PAROL-docs/1/05-operation/homing/)): it ignores the collision
    world, and it takes about half a minute. A later `home()` is a planned joint move to the API's standby, the after-homing pose.

### `move_j` 

```python
rbt.move_j(
    angles: list[float] | None = None,
    *,
    pose: list[float] | None = None,
    duration: float = 0.0,
    speed: float = 0.5,
    accel: float = 0.5,
    r: float = 0.0,
    rel: bool = False,
    wait: bool = True,
    timeout: float = 10.0,
) -> int
```

Joint-space move. Positional arg = joint angles; pose= kwarg = Cartesian target with IK.

Returns the command index (≥ 0) on success, -1 on failure.

```python
rbt.move_j([90, -90, 180, 0, 0, 180], speed=0.5)
```

| Parameter | Meaning |
|---|---|
| `angles` | 6 joint angles in degrees (ignored if pose= is set) |
| `pose` | If set, Cartesian target [x,y,z,rx,ry,rz] — dispatches to MOVEJ_POSE |
| `duration` | Motion duration in seconds; > 0 times the move and speed is unused |
| `speed` | Speed fraction in (0, 1], used when duration is 0 |
| `accel` | Acceleration fraction in (0, 1] |
| `r` | Blend radius in mm (0 = stop at target) |
| `rel` | If True, angles are relative to current position |
| `wait` | If True, block until motion completes |

### `move_l` 

```python
rbt.move_l(
    pose: list[float],
    *,
    frame: Frame = 'WRF',
    duration: float = 0.0,
    speed: float = 0.5,
    accel: float = 0.5,
    r: float = 0.0,
    rel: bool = False,
    wait: bool = True,
    timeout: float = 10.0,
) -> int
```

Linear Cartesian move to target pose.

Returns the command index (≥ 0) on success, -1 on failure.

```python
rbt.move_l([0, 263, 242, 90, 0, 90], speed=0.5)
```

| Parameter | Meaning |
|---|---|
| `pose` | Target [x,y,z,rx,ry,rz] in mm and degrees |
| `frame` | Reference frame ("WRF" or "TRF") |
| `duration` | Motion duration in seconds; > 0 times the move and speed is unused |
| `speed` | Speed fraction in (0, 1], used when duration is 0 |
| `accel` | Acceleration fraction in (0, 1] |
| `r` | Blend radius in mm |
| `rel` | If True, pose is relative delta |
| `wait` | If True, block until motion completes |

### `move_c` 

```python
rbt.move_c(
    via: list[float],
    end: list[float],
    *,
    frame: Frame = 'WRF',
    duration: float = 0.0,
    speed: float = 0.5,
    accel: float = 0.5,
    r: float = 0.0,
    wait: bool = True,
    timeout: float = 10.0,
) -> int
```

Circular arc through current position -> via -> end.

Returns the command index (≥ 0) on success, -1 on failure.

```python
rbt.move_c(via=[0, 250, 250, 90, 0, 90], end=[0, 263, 242, 90, 0, 90], speed=0.5)
```

| Parameter | Meaning |
|---|---|
| `via` | Via-point pose [x,y,z,rx,ry,rz] |
| `end` | End-point pose [x,y,z,rx,ry,rz] |
| `frame` | Reference frame |
| `duration` | Motion duration in seconds; > 0 times the move and speed is unused |
| `speed` | Speed fraction in (0, 1], used when duration is 0 |
| `accel` | Acceleration fraction in (0, 1] |
| `r` | Blend radius in mm |
| `wait` | If True, block until motion completes |

### `move_s` 

```python
rbt.move_s(
    waypoints: list[list[float]],
    *,
    frame: Frame = 'WRF',
    duration: float = 0.0,
    speed: float = 0.5,
    accel: float = 0.5,
    wait: bool = True,
    timeout: float = 10.0,
) -> int
```

Cubic spline through waypoints.

Returns the command index (≥ 0) on success, -1 on failure.

```python
rbt.move_s([[0, 263, 242, 90, 0, 90], [50, 250, 200, 90, 0, 90]], speed=0.5)
```

| Parameter | Meaning |
|---|---|
| `waypoints` | List of poses [[x,y,z,rx,ry,rz], ...] |
| `frame` | Reference frame |
| `duration` | Motion duration in seconds; > 0 times the move and speed is unused |
| `speed` | Speed fraction in (0, 1], used when duration is 0 |
| `accel` | Acceleration fraction in (0, 1] |
| `wait` | If True, block until motion completes |

### `move_p` 

```python
rbt.move_p(
    waypoints: list[list[float]],
    *,
    frame: Frame = 'WRF',
    duration: float = 0.0,
    speed: float = 0.5,
    accel: float = 0.5,
    wait: bool = True,
    timeout: float = 10.0,
) -> int
```

Process move — constant TCP speed with auto-blending at corners.

Returns the command index (≥ 0) on success, -1 on failure.

```python
rbt.move_p([[0, 263, 242, 90, 0, 90], [50, 250, 200, 90, 0, 90]], speed=0.5)
```

| Parameter | Meaning |
|---|---|
| `waypoints` | List of poses [[x,y,z,rx,ry,rz], ...] |
| `frame` | Reference frame |
| `duration` | Motion duration in seconds; > 0 times the move and speed is unused |
| `speed` | Speed fraction in (0, 1], used when duration is 0 |
| `accel` | Acceleration fraction in (0, 1] |
| `wait` | If True, block until motion completes |
