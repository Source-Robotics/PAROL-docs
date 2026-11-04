# 2. The Python API

The Python API, package `parol6`, is two things: a **controller** process that owns the robot, talks to the
control board over serial at 100 Hz, plans the motion and checks collisions; and a **client library** that sends
it commands over UDP, from the same PC or any other on the network, with a blocking interface for scripts and an
asynchronous one for applications. A **dry-run client** runs the same planning without a robot, for tests.

This chapter walks through it in the order you use it. The reference lists every method:
[Python API reference](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/), read from the API's source at the version this site
describes.

## In this chapter

- [Installation](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/installation/)
- [The controller](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/controller/): starting it, the serial port, simulator mode, the environment variables
- [Clients](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/clients/): the sync client, the async client, the dry-run client, the `Robot` lifecycle helper
- [Motion](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/motion/): joint, linear, circular, spline and process moves, speed and duration, blending, profiles
- [Jogging and servoing](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/streaming/): streamed velocity and position targets
- [Tools and the TCP](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/tools-and-tcp/): selecting a tool, gripper actions, the TCP transform
- [I/O, delays and checkpoints](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/io-and-delays/)
- [Status and waiting](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/status-and-waiting/): queries, the status stream, waiting for commands
- [Errors](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/errors/)
- [Examples](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/examples/)

## In three lines

```python
from parol6 import RobotClient
with RobotClient() as rbt:            # the controller runs already: parol6-server --serial COM5
    rbt.home(wait=True); rbt.move_j([90, -90, 180, 0, 0, 180], speed=0.5)
```

## Architecture

```mermaid
flowchart LR
    subgraph Client["Your program"]
        RC["RobotClient / AsyncRobotClient"]
        DR["DryRunRobotClient (no robot)"]
    end
    subgraph Controller["parol6-server"]
        UDP["UDP 5001: commands and queries"]
        Q["Command queue"]
        MP["Motion planner (subprocess)"]
        SP["Segment player, 100 Hz loop"]
        ST["Status broadcast (multicast, 50 Hz)"]
    end
    CB["Control board (serial, 3 Mbaud, 100 Hz)"]
    RC -- commands --> UDP --> Q --> MP --> SP --> CB
    CB -- telemetry --> SP --> ST -- status --> RC
```

The controller is the only process that touches the serial port. The planner runs in a subprocess so that a
long plan never delays the 100 Hz loop; the loop plays the planned segments and streams the jog and servo
targets. Status goes out as multicast, so any number of listeners see the robot's state without asking.
