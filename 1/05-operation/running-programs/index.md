# Running programs

A program is a list of moves, delays, I/O and gripper commands. PAROL6 runs programs in two ways.

## RBTscript in the commander software

The commander's **Program** window takes an RBTscript program: one command per line, `MoveJoint`, `MoveCart`,
`MoveCartRelTRF`, `Delay`, `Output`, `Gripper`, with `Begin()` and `End()` or `Loop()` around it. The command
list next to the window inserts a command with the robot's current pose as its arguments, which is how you teach
points: jog to the pose, click the command. **Start** runs the program, **Stop** halts it.

```
Begin()
MoveJoint(90,-90,180,0,0,180,t=3)
MoveCart(0,263,242,90,0,90,t=2)
Output(1,HIGH)
Delay(1)
Output(1,LOW)
End()
```

[RBTscript](https://docs.source-robotics.com/PAROL-docs/1/programming/03-commander/rbtscript/) has the language and [Examples](https://docs.source-robotics.com/PAROL-docs/1/programming/03-commander/examples/)
has programs to start from. Programs are plain text files you can keep and share.

## Python with the Python API

A Python script that calls the client is a program: every motion call queues a move on the controller, and the
script waits for it or not, as you choose.

```python
from parol6 import RobotClient

with RobotClient() as rbt:
    rbt.home(wait=True)
    rbt.select_tool("SSG-48")
    rbt.tool.calibrate()
    rbt.delay(2)                  # the SSG-48 needs about 3 s; calibrate() waits only 2 s
    rbt.move_j([90, -90, 180, 0, 0, 180], speed=0.5)
    rbt.move_l([0, 263, 200, 90, 0, 90], speed=0.3)
    rbt.tool.close(speed=0.5, current=0.4)
    rbt.move_l([0, 263, 242, 90, 0, 90], speed=0.3)
    rbt.tool.open()
```

The Python API also runs programs written for other tools, and from other machines: the controller accepts
commands over the network from any client, so a program can run on a laptop while the controller runs on the PC
at the robot. [The Python API](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/) is the guide.

## Simulate first

Both programs have a simulator. The commander opens its 3D window with the GUI and mirrors the robot; the Python
API's controller runs with `simulator(True)` or the `DryRunRobotClient` without hardware, through the same
kinematics and collision checks. Run a new program in the simulator at full speed, then on the robot at low speed.

## Speed

The commander's speed slider scales jogging only; a program's speed is in its moves, `v=` and `a=` or `t=`. The Python API takes a `speed` fraction per move and
`set_execution_speed()` scales the queue while it runs; `pause()` and `resume()` hold and continue it.

## Stopping a program

- **Stop** in the commander, or `stop()` in the API: the current move is cancelled, the queue cleared, the robot
  stays enabled and holding.
- The **E-stop**: the robot is disabled and the program or the queue is stopped; in the Python API, call
  `reset()` after releasing it ([Emergency stop](https://docs.source-robotics.com/PAROL-docs/1/02-safety/emergency-stop/)).
- Closing the software: stop the program first. The firmware has no timeout: it keeps executing the last packet
  it received until the next one arrives. After a move to a position the joints stop near that target and hold.

!!! danger "When the PC stops sending during a jog"
    If the commander closes, crashes or loses the USB connection while a joint jogs (in joint or Cartesian
    jog), the firmware keeps that joint turning at its jog speed until it reaches its blocker. Programs that use
    speed tracking (`speed` as the last argument of a move) behave the same way. Use the mains switch of the power
    supply ([Emergency stop](https://docs.source-robotics.com/PAROL-docs/1/02-safety/emergency-stop/)).
