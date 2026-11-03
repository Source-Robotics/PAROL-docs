# Examples

The API's repository has runnable scripts in `examples/`; these are the shapes of program you will write most.

## A self-contained script

Starts the controller, runs in the simulator, moves, stops the controller.

```python
from parol6 import Robot, RobotClient

with Robot(host="127.0.0.1", port=5001, normalize_logs=True):
    with RobotClient(timeout=2.0) as rbt:
        if not rbt.wait_ready(timeout=5.0):
            raise SystemExit("controller did not start")
        rbt.simulator(True)
        rbt.home(wait=True)                     # planned motion is refused until the robot is referenced
        print("pose:", rbt.pose()[:3], "angles:", rbt.angles())
        rbt.move_l([0, 0, 5, 0, 0, 0], rel=True, duration=1.0)
```

## Pick and place with an electric gripper

```python
from parol6 import RobotClient

ABOVE_PICK  = [100, 300, 200, 90, 0, 90]
PICK        = [100, 300, 120, 90, 0, 90]
ABOVE_PLACE = [-100, 300, 200, 90, 0, 90]
PLACE       = [-100, 300, 120, 90, 0, 90]

with RobotClient() as rbt:
    rbt.select_tool("SSG-48")
    rbt.home(wait=True)
    rbt.tool.calibrate()                                # the API gives it 2 s
    rbt.delay(2)                                        # the rest of the SSG-48's calibration
    rbt.tool.open()
    for _ in range(3):
        rbt.move_j(pose=ABOVE_PICK, speed=0.5)
        rbt.move_l(PICK, speed=0.3)
        rbt.tool.close(speed=0.5, current=0.5)          # queued: the next move waits for the grip
        rbt.move_l(ABOVE_PICK, speed=0.3)
        rbt.move_j(pose=ABOVE_PLACE, speed=0.5)
        rbt.move_l(PLACE, speed=0.3)
        rbt.tool.open()
        rbt.move_l(ABOVE_PLACE, speed=0.3)
    rbt.home()
```

## A circle, a spline, a raster

From the API's showcase: three ways to draw a curve, in the XZ plane at a fixed Y.

```python
import math
from parol6 import RobotClient

rbt = RobotClient()
rbt.home()
R, Y, ORI = 30, 340, [90, 0, 90]

def pt(cx, cz, deg):
    a = math.radians(deg)
    return [cx + R * math.cos(a), Y, cz + R * math.sin(a)] + ORI

rbt.move_j(pose=pt(0, 280, 0), speed=0.5)
rbt.move_c(via=pt(0, 280, 180), end=pt(0, 280, 0), speed=0.8)            # a full circle in one arc

waypoints = [pt(0, 140, i * 30) for i in range(12)] + [pt(0, 140, 0)]
rbt.move_l(waypoints[0], speed=0.8)
rbt.move_p(waypoints, speed=0.8)                                         # the same circle as a process path

spline = [[R * math.cos(t * 6 * math.pi), Y, 140 + t * 140] + ORI for t in (i / 36 for i in range(37))]
rbt.move_s(spline, speed=0.8)                                            # a sine wave up the three circles

for i in range(6):                                                       # a raster with blended corners
    y0, y1 = (0, 160) if i % 2 == 0 else (160, 0)
    z = 200 + i * 20
    rbt.move_l([280, y0, z, -180, -90, -180], speed=0.5, r=15)
    rbt.move_l([280, y1, z, -180, -90, -180], speed=0.5, r=15)
rbt.close()
```

## Following a target with a servo stream

```python
import asyncio, math, time
from parol6 import AsyncRobotClient

async def main():
    async with AsyncRobotClient() as rbt:
        await rbt.home(wait=True)
        await rbt.move_l([0, 263, 272, 90, 0, 90], speed=0.5, wait=True)   # to the circle's start
        t0 = time.monotonic()
        while time.monotonic() - t0 < 10:
            t = time.monotonic() - t0
            await rbt.servo_l([30 * math.sin(t), 263, 242 + 30 * math.cos(t), 90, 0, 90], speed=0.5)
            await asyncio.sleep(0.02)                   # 50 targets a second
        # the stream ends by itself a quarter second after the last target

asyncio.run(main())
```

The async client's moves return at once unless `wait=True` is given (the sync client waits by default). Without
it, the first `servo_l` would take the arm from the `move_l` and cancel it.

## Switching an output between moves, and a checkpoint for the script

```python
with RobotClient() as rbt:
    rbt.home(wait=True)
    rbt.move_l([0, 263, 200, 90, 0, 90], speed=0.5, wait=False)
    rbt.write_io(0, 1)                                  # the valve, queued: it switches when the arm is at the part
    rbt.checkpoint("at_part")
    rbt.delay(0.5)
    rbt.move_l([0, 263, 242, 90, 0, 90], speed=0.5, wait=False)
    rbt.write_io(0, 0)                                  # queued after the second move
    rbt.wait_checkpoint("at_part", timeout=20)
    print("at the part")                                # the script learns it here, e.g. to trigger a camera
    rbt.wait_motion()
```

`write_io` is queued with the motion, so the valve switches between the two moves without the script's help; the
checkpoint only tells the script when the queue got there.
