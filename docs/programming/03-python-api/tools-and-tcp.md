# Tools and the TCP

The controller needs to know the tool to compute the pose of its tip, to check it for collisions and to drive
it. Tools are registered in the API with a transform, a collision mesh, variants and the actions they support.

## Registered tools

<!-- api-tools-table -->

`select_tool(key, variant_key)` sets the active tool for everyone; `tools()` lists them; `tool_status()` reports
the applied variant and the tool's state. Changing the tool or the variant clears any TCP correction.

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
rbt.tool.calibrate()                                        # opens and closes fully; 200 ticks, two seconds
rbt.tool.set_position(0.7, speed=0.5, current=0.4)          # 0 open, 1 closed
rbt.tool.close(speed=0.5, current=0.6)
rbt.tool.open()
rbt.tool.release()                                          # drop the grip, the jaws stay
rbt.tool.stop()                                             # immediate
print(rbt.tool.status())                                    # ToolStatus: state, engaged, part_detected, positions
```

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
