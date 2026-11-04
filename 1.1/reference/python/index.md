# Python API reference

The public methods of `RobotClient` (the sync client; the async client has the same methods, awaited, plus the
two status streams), generated from the API's source at v0.9.1. `rbt` in the signatures is a
client, `rbt = RobotClient()`.

The conventions, once: angles in degrees in order J1 to J6, poses as `[x, y, z, rx, ry, rz]` in millimetres and
degrees, `speed` and `accel` as fractions in (0, 1], `duration` in seconds, `r` a blend radius in millimetres,
joints indexed from 0 in jog calls. A motion call returns the command index (≥ 0), or −1 if no acknowledgement arrived; a
query returns `None` on a timeout; a refused or failed command raises `MotionError` ([Errors](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/errors/)).

| Method | Category | Documented on |
|---|---|---|
| `connect_hardware` | Configuration | [configuration](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/configuration/#connect_hardware) |
| `select_profile` | Configuration | [configuration](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/configuration/#select_profile) |
| `select_tool` | Configuration | [tools](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/tools/#select_tool) |
| `set_shapes` | Configuration | [configuration](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/configuration/#set_shapes) |
| `set_status_rate` | Configuration | [configuration](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/configuration/#set_status_rate) |
| `set_tcp_offset` | Configuration | [configuration](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/configuration/#set_tcp_offset) |
| `tcp_offset` | Configuration | [configuration](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/configuration/#tcp_offset) |
| `estop` | Control | [control](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/control/#estop) |
| `pause` | Control | [control](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/control/#pause) |
| `reset` | Control | [control](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/control/#reset) |
| `reset_state` | Control | [control](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/control/#reset_state) |
| `resume` | Control | [control](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/control/#resume) |
| `set_execution_speed` | Control | [control](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/control/#set_execution_speed) |
| `simulator` | Control | [control](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/control/#simulator) |
| `stop` | Control | [control](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/control/#stop) |
| `teleport` | Control | [control](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/control/#teleport) |
| `tool_action` | I/O | [tools](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/tools/#tool_action) |
| `write_io` | I/O | [io](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/io/#write_io) |
| `jog_j` | Jog | [streaming](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/streaming/#jog_j) |
| `jog_l` | Jog | [streaming](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/streaming/#jog_l) |
| `home` | Motion | [motion](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/motion/#home) |
| `move_c` | Motion | [motion](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/motion/#move_c) |
| `move_j` | Motion | [motion](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/motion/#move_j) |
| `move_l` | Motion | [motion](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/motion/#move_l) |
| `move_p` | Motion | [motion](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/motion/#move_p) |
| `move_s` | Motion | [motion](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/motion/#move_s) |
| `close` | Other | [control](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/control/#close) |
| `run_skill` | Other | [control](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/control/#run_skill) |
| `set_tcp_transform` | Other | [configuration](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/configuration/#set_tcp_transform) |
| `stream_status` | Other | [streaming](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/streaming/#stream_status) |
| `stream_status_shared` | Other | [streaming](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/streaming/#stream_status_shared) |
| `tcp_transform` | Other | [configuration](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/configuration/#tcp_transform) |
| `wait_command` | Other | [synchronization](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/synchronization/#wait_command) |
| `wait_ready` | Other | [synchronization](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/synchronization/#wait_ready) |
| `wait_status` | Other | [synchronization](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/synchronization/#wait_status) |
| `host` | Property | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#host) |
| `port` | Property | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#port) |
| `robot` | Property | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#robot) |
| `tool` | Property | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#tool) |
| `activity` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#activity) |
| `angles` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#angles) |
| `error` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#error) |
| `execution_speed` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#execution_speed) |
| `io` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#io) |
| `is_estop_pressed` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#is_estop_pressed) |
| `is_robot_stopped` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#is_robot_stopped) |
| `is_simulator` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#is_simulator) |
| `joint_speeds` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#joint_speeds) |
| `loop_stats` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#loop_stats) |
| `ping` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#ping) |
| `pose` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#pose) |
| `profile` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#profile) |
| `queue` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#queue) |
| `reachable` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#reachable) |
| `reset_loop_stats` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#reset_loop_stats) |
| `shapes` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#shapes) |
| `status` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#status) |
| `status_rate` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#status_rate) |
| `tcp_speed` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#tcp_speed) |
| `tools` | Query | [queries](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/queries/#tools) |
| `servo_j` | Streaming | [streaming](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/streaming/#servo_j) |
| `servo_l` | Streaming | [streaming](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/streaming/#servo_l) |
| `checkpoint` | Synchronization | [synchronization](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/synchronization/#checkpoint) |
| `delay` | Synchronization | [synchronization](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/synchronization/#delay) |
| `wait_checkpoint` | Synchronization | [synchronization](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/synchronization/#wait_checkpoint) |
| `wait_motion` | Synchronization | [synchronization](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/synchronization/#wait_motion) |
