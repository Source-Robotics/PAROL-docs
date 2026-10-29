# Status fields

The fields of the status buffer the controller broadcasts, as `stream_status()` yields it and `status()`
summarises it, from the source at <!-- api-version -->. Arrays are numpy arrays.

<!-- api-status-fields -->

## Meaning

| Field | Meaning |
|---|---|
| `session_id`, `seq`, `mono_time_ns` | The status publisher's lifetime (changes on restart), a sequence number (gaps mean missed broadcasts), and the monotonic time of the controller's snapshot |
| `pose` | The tool pose as a 4×4 matrix, flattened (16 values), in the WRF |
| `angles`, `speeds` | Joint angles in degrees and speeds in deg/s, J1 to J6 |
| `io` | `[in1, in2, out1, out2, estop]` |
| `tool_status` | The selected tool's `ToolStatus`; key `NONE` when no tool is fitted |
| `joint_en`, `cart_en_wrf`, `cart_en_trf`, `cart_en` | Enablement: whether each joint, and each Cartesian axis in each frame, can still move in the positive and negative direction (12 values: six axes, two directions) |
| `action_current`, `action_params`, `action_state` | What the controller is executing, its parameters, and the state: idle, executing, error |
| `executing_index`, `completed_index`, `accepted_index` | The index of the command running, the highest completed, and the latest accepted |
| `last_checkpoint` | The label of the last checkpoint reached |
| `error` | The current `RobotError`, or `None` |
| `queued_segments`, `queued_duration` | How much motion is queued, in segments and in seconds of estimated duration (tool actions included) |
| `tcp_speed` | The tool's linear speed in mm/s |
| `simulator_active` | Simulator mode |
| `collision_active`, `collision_pairs` | Whether the collision checker is on, and the pairs it currently reports |
| `scene_epoch` | Changes when the collision world changes: re-query `shapes()` |
| `homed`, `enabled` | Whether the robot is referenced, and whether motion is enabled |
| `torques`, `torques_ext` | Reserved for arms with torque sensing; zero on PAROL6 |
| `warnings`, `link_health`, `drive_health`, `loop_health` | Diagnostics: warnings, the serial link, the drives, the control loop timing |
| `homing` | The progress of a homing sequence |

The buffer's `freedrive` property is always false: PAROL6's steppers cannot be back-driven. `mode` is an alias of
`action_state`.
