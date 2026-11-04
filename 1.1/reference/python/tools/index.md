# Tools

Selecting a tool, the generic tool action, and the methods of the bound tool object `rbt.tool`. Tool actions are
queued with the motion; `tool.stop()` is immediate. [Tools and the TCP](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/tools-and-tcp/)
in the guide.

## Registered tools

| Key | Tool | Variants (default first) |
|---|---|---|
| `NONE` | Bare flange - no tool attached | — |
| `PNEUMATIC` | Pneumatic gripper assembly (vertical/horizontal mounting) | `vertical`, `horizontal` |
| `SSG-48` | SSG-48 adaptive electric gripper (Spectral micro BLDC) | `finger`, `pinch` |
| `MSG` | MSG compliant AI stepper gripper (StepFOC) | `100mm`, `150mm`, `200mm` |
| `VACUUM` | Vacuum gripper (pneumatic valve I/O) | — |

## Selecting and acting

### `select_tool` 

```python
rbt.select_tool(tool_name: str, variant_key: str = '') -> int
```

Set the active end-effector tool on the controller.

```python
rbt.select_tool("PNEUMATIC")
```

| Parameter | Meaning |
|---|---|
| `tool_name` | Name of the tool ('NONE', 'PNEUMATIC', 'SSG-48', 'MSG', 'VACUUM') |
| `variant_key` | Optional variant within the tool type. |

**Returns:** Command index (>= 0) if queued, 0 on failure.

### `tool_action` 

```python
rbt.tool_action(
    tool_key: str,
    action: str,
    params: list | None = None,
    *,
    wait: bool = False,
    timeout: float = 10.0,
) -> int
```

Send a generic tool action command.

Returns the command index (>= 0) on success, -1 on failure. The action and its parameters are checked before anything is sent: a malformed one raises `ValueError`. A key naming a tool other than the selected one is refused by the controller.

A tool action is queued work: it runs in queue order with motion, the arm holding still while it does, so a wait on it covers the motion queued ahead of it, and one sent after a blended move ends the blend there. A `move` before a completed `calibrate` is refused when its turn comes, failing its own index; a tool action that fails cancels what is queued behind it (`MOTN_CANCELLED`). A pause holds the tool actions still queued. `stop()`, `estop()`, `reset_state()`, a teleport, or a jog or servo stream taking the arm discards them and halts the one running where the jaws are, keeping the grip.

`stop` alone acts at once, on the tool fitted now: it halts the action running, failing it as cancelled by a tool stop, keeps what is queued behind it, and holds the next queued tool action until the jaws are still.

Electric grippers take `move [position, speed, current]` (exactly three fractions in `[0, 1]`; current spans the tool's `current_range`), `calibrate`, `stop` (halt in place, keep grip) and `idle` (release, the jaws left where they are); `set_position`/`open`/`close` map onto `move`. Pneumatic grippers take `open`, `close`, and `move`/`set_position [position]`.

```python
rbt.tool_action("PNEUMATIC", "open")
```

| Parameter | Meaning |
|---|---|
| `tool_key` | Tool registry key (e.g. "PNEUMATIC", "SSG-48", "MSG") |
| `action` | Action name (e.g. "open", "close", "move", "calibrate") |
| `params` | Positional parameters (meaning defined by tool config) |
| `wait` | If True, block until action completes |
| `timeout` | Maximum time to wait in seconds (only used when wait=True) |

!!! note
    The actions of the electric grippers: `move` with `[position, speed, current]` as fractions, `calibrate`,
    `stop`, `idle` (release). Of the pneumatic and vacuum grippers: `open`, `close`, and `move` (or
    `set_position`) with `[position]`, below 0.5 opening and from 0.5 closing. The tool methods below call these.

## The electric gripper tool (SSG-48, MSG)

### `tool.set_position` (electric) 

```python
rbt.tool.set_position(
    position: float,
    *,
    speed: float = 0.5,
    current: float = 0.5,
    **wait_kwargs: Any,
) -> int
```

Moves the jaws to `position`, 0 open and 1 closed, at `speed` (a fraction of the gripper's speed range) and with
`current` as the current limit, the grip force. `current` is a fraction of the tool's current range: 100 to
1300 mA for the SSG-48, 100 to 2800 mA for the MSG, so `current=0.5` is 700 mA or 1450 mA. Queued: it waits for
the motion before it, and the motion after it waits for the jaws to arrive, stop on a part or stall. Refused
when its turn comes on a gripper that was never calibrated.

### `tool.open` (electric) 

```python
rbt.tool.open(*, speed: float = 0.5, current: float = 0.5, **wait_kwargs: Any) -> int
```

`set_position(0.0, ...)`: the jaws fully open.

### `tool.close` (electric) 

```python
rbt.tool.close(*, speed: float = 0.5, current: float = 0.5, **wait_kwargs: Any) -> int
```

`set_position(1.0, ...)`: the jaws close until they reach the end or stop on a part.

### `tool.calibrate` (electric) 

```python
rbt.tool.calibrate(**kwargs: object) -> int
```

Sends the gripper its calibration: it opens fully and closes fully to find its end stops. Queued. The API counts
it done after a fixed 2 s (200 control cycles) and does not read the gripper's calibrated bit; the SSG-48 needs
about 3 s and the MSG 5 to 6 s, so queue a `delay()` after it ([Calibrating](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/tools-and-tcp/#calibrating)).
There is no clear-error action: a latched gripper error is cleared from the commander or Motor GUI.

### `tool.release` (electric) 

```python
rbt.tool.release(**kwargs: object) -> int
```

Drop the grip, freeing the jaws for manual handling, once the commands queued ahead of it have run. The jaws stay where they are.

### `tool.stop` (electric) 

```python
rbt.tool.stop(**kwargs: object) -> int
```

Halt the jaws where they are, keeping the grip, ahead of anything still queued: the action running fails as cancelled, and the queue behind it is kept. On an uncalibrated gripper, which has no position to hold, this releases instead.

## The pneumatic gripper tool (PNEUMATIC, VACUUM)

### `tool.set_position` (pneumatic) 

```python
rbt.tool.set_position(position: float, **kwargs: float | int) -> int
```

Binary position: < 0.5 opens, >= 0.5 closes.

### `tool.open` (pneumatic) 

```python
rbt.tool.open(**kwargs: float | int) -> int
```

Switches output 1 high, queued with the motion; the action lasts the tool's estimated stroke (a single control
cycle for the vacuum gripper). Which way the gripper moves depends on the tubing.

### `tool.close` (pneumatic) 

```python
rbt.tool.close(**kwargs: float | int) -> int
```

Switches output 1 low, queued with the motion; otherwise as `open()`.

Every tool object also has `status()`, returning the `ToolStatus` of the selected tool: `key`, `state`,
`engaged`, `part_detected`, `fault_code`, `positions`, `channels` and `variant_key`. For the electric grippers,
[Tool status](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/tools-and-tcp/#tool-status) says where each field comes from.
