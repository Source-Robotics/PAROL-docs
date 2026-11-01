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
    `stop`, `idle` (release). Of the pneumatic and vacuum grippers: `open`, `close`. The tool methods below call
    these.

## The electric gripper tool (SSG-48, MSG)

<!-- api-tool: electric.set_position -->

<!-- api-tool: electric.open -->

<!-- api-tool: electric.close -->

<!-- api-tool: electric.calibrate -->

<!-- api-tool: electric.release -->

<!-- api-tool: electric.stop -->

## The pneumatic gripper tool (PNEUMATIC, VACUUM)

<!-- api-tool: pneumatic.set_position -->

<!-- api-tool: pneumatic.open -->

<!-- api-tool: pneumatic.close -->

Every tool object also has `status()`, returning the `ToolStatus` of the selected tool: `tool_key`, `state`,
`engaged`, `part_detected`, `fault_code`, `positions`, and the applied variant.
