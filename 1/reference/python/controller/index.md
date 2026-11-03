# The controller and its environment

## The command line

`parol6-server`, from the source at v0.9.1:

| Option | Default | Meaning |
|---|---|---|
| `--host` | `0.0.0.0` | UDP host address |
| `--port` | `5001` | UDP port |
| `--serial` | — | Serial port (e.g., /dev/ttyUSB0 or COM3) |
| `--baudrate` | `3000000` | Serial baudrate |
| `-v`, `--verbose` | `0` | Increase verbosity; -v=INFO, -vv=DEBUG, -vvv=TRACE |
| `-q`, `--quiet` | flag | Enable quiet logging (WARNING level) |
| `--log-level` | — | Set specific log level (one of `TRACE`, `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) |

Without `--serial` the controller starts in simulator mode. The port can also come from `PAROL6_COM_PORT` or from
the file the last successful port was saved to.

## Environment variables

Read at the controller's start:

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

A default marked *computed* is a path or an expression; see `parol6/config.py`. [The controller](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/controller/)
in the guide says which ones matter.

## The wire protocol

Clients and the controller exchange msgpack messages over UDP: a command or query with a request ID, and an OK,
an error, a response or a status. The protocol version is checked in every status broadcast, and a client that
speaks another version raises `ProtocolVersionError`. The command and query types of this version:

**Commands:** `CmdType.PING` and the others, 54 in all, the queries among them; **queries:** `PING`, `STATUS`,
`ANGLES`, `POSE`, `IO`, `SPEEDS`, `TOOL`, `QUEUE`, `CURRENT_ACTION`, `LOOP_STATS`, `PROFILE`, `TOOL_STATUS`,
`ENABLEMENT`, `ERROR`, `TCP_SPEED`, `IS_SIMULATOR`, `TCP_OFFSET`, `SHAPES`, `STATUS_RATE`, `TCP_TRANSFORM`,
`EXECUTION_SPEED`, `COMMAND_COMPLETION`. The definitions are `parol6/protocol/wire.py`; a program in another
language can speak the protocol from them, though the Python client is the supported path.

## Python

The package needs Python >=3.11.
