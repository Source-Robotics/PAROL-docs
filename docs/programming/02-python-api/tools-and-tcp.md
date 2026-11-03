# Tools and the TCP

The controller needs to know the tool to compute the pose of its tip, to check it for collisions and to drive
it. Tools are registered in the API with a transform, a collision mesh, variants and the actions they support.

## Registered tools

<!-- api-tools-table -->

`select_tool(key, variant_key)` sets the active tool for everyone, queued with the motion; `tools()` lists them;
`rbt.tool.status()` and the status stream's `tool_status` report the applied variant and the tool's state.
Changing the tool or the variant clears any TCP correction.

```python
rbt.select_tool("PNEUMATIC")                        # the default variant
rbt.select_tool("PNEUMATIC", variant_key="horizontal")
rbt.select_tool("SSG-48", variant_key="pinch")
rbt.select_tool("MSG", variant_key="150mm")
```

## Driving the tool

`rbt.tool` is the selected tool's object. The electric grippers (SSG-48, MSG) have position, speed and current
as fractions of their ranges, and the actions calibrate, stop and release; the pneumatic and vacuum grippers
have open and close on an output.

```python
rbt.select_tool("SSG-48")
rbt.tool.calibrate()                                        # queued; the API gives it 2 s
rbt.delay(2)                                                # the rest of the SSG-48's calibration
rbt.tool.set_position(0.7, speed=0.5, current=0.4)          # 0 open, 1 closed
rbt.tool.close(speed=0.5, current=0.6)
rbt.tool.open()
rbt.tool.release()                                          # drop the grip, the jaws stay
rbt.tool.stop()                                             # immediate
print(rbt.tool.status())                                    # ToolStatus: state, engaged, part_detected, positions
```

The current fraction spans the tool's current range: 100 to 1300 mA for the SSG-48 and 100 to 2800 mA for the
MSG, so `current=0.4` is 580 mA on the SSG-48 and 1180 mA on the MSG. Keep an MSG within its stepper's rating
([MSG](../../end-effectors/msg.md#current-and-force)).

### Calibrating

The gripper has to be calibrated after every power-up: it opens fully and closes fully to find its end stops.
`calibrate()` sends the calibration and counts it done after a fixed 2 s (200 control cycles); it does not read
the gripper's calibrated bit. The gripper takes longer: about 3 s for the SSG-48, and about 5 to 6 s for the MSG
on the longer rails. Queue a `delay()` after `calibrate()` to cover the rest with a margin, 2 s for the SSG-48 and 5 s
for the MSG, before the first move. A gripper that has latched an error must be cleared first: the API has no
clear-error action at this version, so use the commander's **Clear gripper error** or Motor GUI, then calibrate.

### Tool status

`rbt.tool.status()` returns a `ToolStatus`. For the electric grippers, `positions` is the jaw position (0 open,
1 closed) and `channels` the current in mA. `engaged` is taken from the gripper-speed field of the telemetry,
which firmware 1 always reports as 1, so it reads true. `part_detected` is taken from bits 3 and 2 of the
gripper's status byte, where the gripper manuals put the temperature and timeout errors (they put the object
detection in bits 5 and 4). The calibrated and error bits are not in `ToolStatus` at this version. To know that a
part is held, check the position the jaws stopped at, or use a sensor.

Tool actions are **queued work**: an action waits for the motion queued before it, the arm holds still while it
runs, and the motion queued after it waits for it. A `move` on a gripper that was never calibrated is refused
when its turn comes and, like any failing command, cancels what is queued behind it. `stop()` is the exception:
it is immediate, halts the running action, and keeps the queue. `tool_action(key, action, params)` is the generic
form the tool methods are built on.

## The TCP

The tool centre point is the point the robot positions: the registered tool's tip. Two corrections on top of
it:

```python
index = rbt.set_tcp_offset(0, 0, -190)           # a translation in the tool frame, mm
index = rbt.set_tcp_transform(0, 0, 25, 0, 90, 0) # translation and intrinsic XYZ rotation, degrees
rbt.wait_command(index)                           # queued: wait before relying on it
print(rbt.tcp_transform())                        # six values; tcp_offset() the three translations
```

Both are queued with the motion so that moves planned before the change keep their frame. `set_tcp_offset`
clears a rotation; a tool change clears both. The correction applies to live FK, Cartesian planning, TRF motion
and dry-run previews alike; the collision meshes stay on their links regardless.

## Your own tool

Add a `ToolConfig` and `register_tool("KEY", config)` in `parol6/tools.py`: the transform from the flange, the
collision mesh, the variants, and the actions if it is driven through the robot ([Your own tool](../../end-effectors/custom-tools.md)).
The controller validates every tool action against the config before it is acknowledged.

## Held objects

A program can declare the shape of what the gripper holds, attached to the flange, so that the collision checker
accounts for it: `shape.attach(...)` on a shape from `rbt.shapes()`, applied with `set_shapes()`. The declaration
is tied to the tool, the world and a fresh position reference; a change in any of them invalidates it and
blocks motion until it is reconciled. The README of the API has the rules in full.
