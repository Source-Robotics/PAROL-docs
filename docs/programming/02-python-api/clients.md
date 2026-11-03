# Clients

Three clients, one interface.

| | `RobotClient` | `AsyncRobotClient` | `DryRunRobotClient` |
|---|---|---|---|
| Style | Blocking calls | `async`/`await`, status as an async generator | Blocking, same methods |
| Needs | A running controller | A running controller | Nothing: plans in-process |
| For | Scripts, programs, tests on the robot | GUIs, teleoperation, anything that streams | Unit tests, previews, CI |

All three are created with the controller's host and port (`127.0.0.1`, `5001` by default), work as context
managers, and are closed with `close()`.

## The sync client

```python
from parol6 import RobotClient

with RobotClient(host="127.0.0.1", port=5001, timeout=2.0) as rbt:
    if not rbt.wait_ready(timeout=5):
        raise SystemExit("no controller")
    rbt.home(wait=True)
    index = rbt.move_j([90, -90, 180, 0, 0, 180], speed=0.5)    # waits by default (wait=True)
    print(rbt.pose(), rbt.angles())
```

A motion call returns the **command index** the controller assigned, or −1 if no acknowledgement arrived; a
command the controller refuses raises `MotionError`. With `wait=True` the call blocks until that command
completes and raises `MotionError` if it failed; with `wait=False` the call returns at once and
`wait_command(index)` waits later. Queries return values or `None` on a timeout.

The defaults differ between the calls and between the clients:

| Call | `RobotClient` | `AsyncRobotClient` | `timeout` (used when waiting) |
|---|---|---|---|
| `move_j`, `move_l`, `move_c`, `move_s`, `move_p` | `wait=True` | `wait=False` | 10 s |
| `home` | `wait=False` | `wait=False` | 60 s |
| `tool_action` and the `rbt.tool` methods | `wait=False` | `wait=False` | 10 s |

A move that runs longer than its `timeout` raises `TimeoutError` while it goes on running: give long moves a
larger `timeout`.

## The async client

```python
import asyncio
from parol6 import AsyncRobotClient

async def main():
    async with AsyncRobotClient() as rbt:
        await rbt.wait_ready(timeout=3)
        await rbt.home(wait=True)
        async for status in rbt.stream_status():
            print(status.angles, status.action_state)
            if status.completed_index >= 0:
                break

asyncio.run(main())
```

The same methods, awaited, with one difference: the moves return at once unless you pass `wait=True` (the
table above). Plus `stream_status()`, which yields a copy of every status broadcast, and
`stream_status_shared()`, which yields the same buffer each time for zero-copy hot paths. Slow consumers skip to
the latest status.

## The dry-run client

```python
from parol6 import DryRunRobotClient

with DryRunRobotClient() as rbt:
    rbt.home(wait=True)
    rbt.move_l([0, 263, 242, 90, 0, 90], speed=0.5)     # planned, collision-checked, not executed anywhere
```

The same calls run through the planner in your process and report what the controller would do: refused
targets, collisions, durations. Its status and timing are a preview, not a measurement; the API marks that by
advertising `execution.preview`.

## The bound tool

`rbt.tool` is the tool object of the selected tool, with `open()`, `close()`, `set_position()`, `calibrate()`,
`release()`, `stop()` and `status()` as the tool type has them ([Tools and the TCP](tools-and-tcp.md)). It raises
if no tool is selected.

## Several clients

The controller serves any number of clients at once; the queue and the streamed motion are shared
([Control ownership](../../theory/control-ownership.md)). A client that must know its command finished waits
on its own index, never on "the robot stopped".
