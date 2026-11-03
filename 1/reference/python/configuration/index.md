# Configuration

The hardware connection, the motion profile, the TCP corrections, the collision world and the status rate.
[Tools and the TCP](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/tools-and-tcp/) and [The controller](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/controller/)
in the guide.

### `connect_hardware` 

```python
rbt.connect_hardware(port_str: str) -> int
```

Connect to robot hardware via serial port.

```python
rbt.connect_hardware("/dev/ttyUSB0")
```

| Parameter | Meaning |
|---|---|
| `port_str` | Serial port path (e.g., '/dev/ttyUSB0' or 'COM3'). |

**Returns:** 1 if acknowledged, 0 on failure.

**Raises:**

- `ValueError`: If port_str is empty.

### `select_profile` 

```python
rbt.select_profile(profile: str) -> int
```

Set the motion profile (e.g. `"TOPPRA"`).

```python
rbt.select_profile("TOPPRA")
```

| Parameter | Meaning |
|---|---|
| `profile` | Motion profile type ('TOPPRA', 'RUCKIG', 'QUINTIC', 'TRAPEZOID', 'LINEAR') |
| `Note` | RUCKIG is point-to-point only; Cartesian moves will use TOPPRA. |

**Returns:** 1 once the profile is selected, 0 when no reply arrives.

**Raises:**

- `MotionError`: when `profile` is not a profile name.

!!! note
    The profiles of this version: `TOPPRA`, `RUCKIG`, `QUINTIC`, `TRAPEZOID`, `LINEAR`. [Motion profiles](https://docs.source-robotics.com/PAROL-docs/1/theory/motion-profiles/)
    says what each does.

### `set_tcp_offset` 

```python
rbt.set_tcp_offset(x: float = 0, y: float = 0, z: float = 0) -> int
```

Set TCP offset in mm, composed on top of the current tool transform.

The offset shifts the effective TCP point in the tool's local frame. Subsequent motion (especially TRF relative moves) will use the new TCP. Returns the queued index; await `wait_command(index)` to confirm application. This translation-only setter clears user TCP rotation. Call with (0, 0, 0) to reset. Changing tools resets the offset.

```python
rbt.set_tcp_offset(0, 0, -190)  # pencil tip 190mm from gripper
```

### `set_tcp_transform` 

```python
rbt.set_tcp_transform(
    x: float = 0,
    y: float = 0,
    z: float = 0,
    roll: float = 0,
    pitch: float = 0,
    yaw: float = 0,
) -> int
```

*No docstring.*

### `tcp_offset` 

```python
rbt.tcp_offset() -> list[float]
```

Query current TCP offset in mm [x, y, z].

```python
offset = rbt.tcp_offset()
```

### `tcp_transform` 

```python
rbt.tcp_transform() -> list[float]
```

*No docstring.*

!!! note
    `set_tcp_transform(x, y, z, roll, pitch, yaw)`: millimetres and intrinsic XYZ degrees relative to the
    registered tool. Both setters return a queued index; wait for it before relying on the correction. The TCP
    queries raise `TimeoutError` instead of returning a misleading zero when the controller does not answer.

### `set_shapes` 

```python
rbt.set_shapes(shapes: list) -> int
```

Replace the program-layer collision-world shapes (keep-out barriers).

Collision-enabled shapes are added to the controller's checkers so motion is blocked against them; an empty list clears the program layer. Installation-layer shapes (robot config) are unaffected.

Acknowledged: returns 1 only after the controller confirms the world was applied; 0 on timeout. Raises MotionError if the controller rejects the shapes.

```python
rbt.set_shapes([Box(name="table", x=0.6, y=0.4, z=0.02,
                    pose=(0.3, 0, -0.01, 0, 0, 0))])
```

!!! note
    Shapes are the program layer of the collision world: boxes and other primitives with a pose in metres and
    extrinsic XYZ radians, collision-enabled or visual only, attachable to the flange as held objects. The
    installation layer, from the robot's configuration, is not affected.

### `set_status_rate` 

```python
rbt.set_status_rate(hz: float) -> int
```

Set the rate the controller broadcasts status at.

```python
rbt.set_status_rate(100)
```
