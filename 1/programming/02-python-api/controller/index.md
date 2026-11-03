# The controller

`parol6-server` is the process that owns the robot. Start it on the PC the control board is plugged into, and
leave it running; clients connect and disconnect as they like.

## Starting it

```
parol6-server --serial COM5                # Windows
parol6-server --serial /dev/ttyACM0        # Linux
parol6-server --serial /dev/cu.usbmodem1   # macOS: ls /dev/cu.usbmodem* gives the name
parol6-server                              # no serial port: simulator mode
parol6-server --serial COM5 --log-level INFO
```

The options, from the source:

| Option | Default | Meaning |
|---|---|---|
| `--host` | `0.0.0.0` | UDP host address |
| `--port` | `5001` | UDP port |
| `--serial` | — | Serial port (e.g., /dev/ttyUSB0 or COM3) |
| `--baudrate` | `3000000` | Serial baudrate |
| `-v`, `--verbose` | `0` | Increase verbosity; -v=INFO, -vv=DEBUG, -vvv=TRACE |
| `-q`, `--quiet` | flag | Enable quiet logging (WARNING level) |
| `--log-level` | — | Set specific log level (one of `TRACE`, `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) |

The serial port can also come from the environment (`PAROL6_COM_PORT`) or from the file the controller saves
the last port to, so that a second start needs no option. Once running, `connect_hardware("COM5")` from a client
connects or re-connects the port, and `simulator(True)` switches to the virtual arm.

## From Python

The `Robot` class starts and stops the controller as a subprocess, for scripts that should be self-contained:

```python
from parol6 import Robot, RobotClient

with Robot(host="127.0.0.1", port=5001) as robot:      # starts parol6-server, waits until it answers
    with RobotClient() as rbt:
        rbt.wait_ready(timeout=5)
        rbt.simulator(True)
        rbt.home(wait=True)
```

`Robot` also carries the robot model (kinematics, limits, tools) that the clients use for previews.

## Simulator mode

Without a serial port, or after `simulator(True)`, the controller runs the same planner against a virtual arm
and broadcasts its state. Everything works except the hardware: homing is instant, `teleport()` sets the pose,
collisions are checked. Develop in the simulator and switch to the hardware with `connect_hardware()` or a
restart with `--serial`.

## The loop

The controller sends a packet to the board every 10 ms (100 Hz) and broadcasts status at 50 Hz. If the PC cannot
keep up it logs `loop overbudget by +N%`, as a warning when it happens more than three times a minute (at DEBUG
level otherwise); `loop_stats()` shows the figures. Lower
`PAROL6_CONTROL_RATE_HZ`, close other programs, and keep logging at INFO or above: TRACE and DEBUG cost time.

## Environment variables

Everything configurable without code, read at start-up:

| Variable | Default |
|---|---|
| `PAROL6_BLEND_HOLD_S` | `0.1` |
| `PAROL6_BUSY_THRESHOLD_MS` | `1.0` |
| `PAROL6_COLLISION_CHECK` | `1` |
| `PAROL6_COLLISION_CLEARANCE_M` | `0.005` |
| `PAROL6_COLLISION_JOG_LOOKAHEAD_S` | `0.15` |
| `PAROL6_COLLISION_PATH_SAMPLES` | `16` |
| `PAROL6_COLLISION_SRDF` | `computed` |
| `PAROL6_COM_FILE` | `computed` |
| `PAROL6_COM_PORT` | — |
| `PAROL6_CONTROL_RATE_HZ` | `100` |
| `PAROL6_EXECUTION_OVERRIDE_TRANSITION_S` | `1.0` |
| `PAROL6_MAX_BACKLOG_COUNT` | `500` |
| `PAROL6_MAX_BLEND_LOOKAHEAD` | `100` |
| `PAROL6_MCAST_GROUP` | `239.255.0.101` |
| `PAROL6_MCAST_IF` | `127.0.0.1` |
| `PAROL6_MCAST_PORT` | `50510` |
| `PAROL6_MCAST_TTL` | `1` |
| `PAROL6_PATH_SAMPLES` | `200` |
| `PAROL6_SERIAL` | — |
| `PAROL6_SETTLE_MAX_TICKS` | `20` |
| `PAROL6_STATUS_RATE_HZ` | `50` |
| `PAROL6_STATUS_STALE_S` | `0.5` |
| `PAROL6_STATUS_TRANSPORT` | `MULTICAST` |
| `PAROL6_STATUS_UNICAST_HOST` | `127.0.0.1` |
| `PAROL_TRACE` | `0` |

The ones you are most likely to touch: `PAROL6_COM_PORT` (the serial port), `PAROL6_CONTROL_RATE_HZ` and
`PAROL6_STATUS_RATE_HZ` (the loop and broadcast rates), `PAROL6_MCAST_GROUP` and `PAROL6_MCAST_PORT` (where the
status goes; `PAROL6_STATUS_TRANSPORT=UNICAST` with `PAROL6_STATUS_UNICAST_HOST` for networks without multicast),
and `PAROL6_COLLISION_CHECK` (0 disables collision checking). A path or an expression as the default is marked
*computed*: see `config.py`.

## Security

The controller accepts any well-formed command on its UDP port from anyone who can reach it. That is by design,
so that a GUI and a script can share it, and it means: run it on a trusted network, or bind `--host 127.0.0.1`.
