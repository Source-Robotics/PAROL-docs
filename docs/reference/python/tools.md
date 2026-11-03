# Tools

Selecting a tool, the generic tool action, and the methods of the bound tool object `rbt.tool`. Tool actions are
queued with the motion; `tool.stop()` is immediate. [Tools and the TCP](../../programming/02-python-api/tools-and-tcp.md)
in the guide.

## Registered tools

<!-- api-tools-table -->

## Selecting and acting

<!-- api: select_tool -->

<!-- api: tool_action -->

!!! note
    The actions of the electric grippers: `move` with `[position, speed, current]` as fractions, `calibrate`,
    `stop`, `idle` (release). Of the pneumatic and vacuum grippers: `open`, `close`, and `move` (or
    `set_position`) with `[position]`, below 0.5 opening and from 0.5 closing. The tool methods below call these.

## The electric gripper tool (SSG-48, MSG)

<!-- api-tool: electric.set_position -->

Moves the jaws to `position`, 0 open and 1 closed, at `speed` (a fraction of the gripper's speed range) and with
`current` as the current limit, the grip force. `current` is a fraction of the tool's current range: 100 to
1300 mA for the SSG-48, 100 to 2800 mA for the MSG, so `current=0.5` is 700 mA or 1450 mA. Queued: it waits for
the motion before it, and the motion after it waits for the jaws to arrive, stop on a part or stall. Refused
when its turn comes on a gripper that was never calibrated.

<!-- api-tool: electric.open -->

`set_position(0.0, ...)`: the jaws fully open.

<!-- api-tool: electric.close -->

`set_position(1.0, ...)`: the jaws close until they reach the end or stop on a part.

<!-- api-tool: electric.calibrate -->

Sends the gripper its calibration: it opens fully and closes fully to find its end stops. Queued. The API counts
it done after a fixed 2 s (200 control cycles) and does not read the gripper's calibrated bit; the SSG-48 needs
about 3 s and the MSG 5 to 6 s, so queue a `delay()` after it ([Calibrating](../../programming/02-python-api/tools-and-tcp.md#calibrating)).
There is no clear-error action: a latched gripper error is cleared from the commander or Motor GUI.

<!-- api-tool: electric.release -->

<!-- api-tool: electric.stop -->

## The pneumatic gripper tool (PNEUMATIC, VACUUM)

<!-- api-tool: pneumatic.set_position -->

<!-- api-tool: pneumatic.open -->

Switches output 1 high, queued with the motion; the action lasts the tool's estimated stroke (a single control
cycle for the vacuum gripper). Which way the gripper moves depends on the tubing.

<!-- api-tool: pneumatic.close -->

Switches output 1 low, queued with the motion; otherwise as `open()`.

Every tool object also has `status()`, returning the `ToolStatus` of the selected tool: `key`, `state`,
`engaged`, `part_detected`, `fault_code`, `positions`, `channels` and `variant_key`. For the electric grippers,
[Tool status](../../programming/02-python-api/tools-and-tcp.md#tool-status) says where each field comes from.
