# The controller and its environment

## The command line

`parol6-server`, from the source at <!-- api-version -->:

<!-- api-cli-table -->

Without `--serial` the controller starts in simulator mode. The port can also come from `PAROL6_COM_PORT` or from
the file the last successful port was saved to.

## Environment variables

Read at the controller's start:

<!-- api-env-table -->

A default marked *computed* is a path or an expression; see `parol6/config.py`. [The controller](../../programming/02-python-api/controller.md)
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

The package needs Python <!-- api-python -->.
