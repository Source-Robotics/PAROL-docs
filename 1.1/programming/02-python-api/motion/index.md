# Motion

Planned motion: the client sends a target, the controller plans the trajectory in its planner subprocess,
checks it for collisions and limits, queues it, and plays it. Every planned command returns a command index and
runs in queue order.

## The five moves

| Call | Path | Target |
|---|---|---|
| `move_j(angles)` | Straight in joint space: every joint moves proportionally, all finish together. The tool's path curves | Six joint angles, or `pose=` a Cartesian pose solved once at the target |
| `move_l(pose)` | A straight line of the tool, orientation interpolated | A pose in the WRF, or in the TRF with `frame="TRF"` |
| `move_c(via, end)` | A circular arc from the current pose through `via` to `end` | Two poses |
| `move_s(waypoints)` | A cubic spline through the waypoints | A list of poses |
| `move_p(waypoints)` | A process path: the waypoints joined by lines, run at constant tool speed with automatic blending at the corners | A list of poses |

`rel=True` on `move_j` and `move_l` makes the target relative to the current angles or pose; with `frame="TRF"`
a relative `move_l` moves along the tool's own axes.

```python
rbt.move_j([90, -90, 180, 0, 0, 180], speed=0.5)                 # joint move
rbt.move_j(pose=[100, 340, 334, 90, 0, 90], speed=0.5)           # IK at the target, then a joint move
rbt.move_l([-50, 340, 334, 90, 0, 90], speed=0.3)                # straight line
rbt.move_l([0, 0, -20, 0, 0, 0], frame="TRF", rel=True, speed=0.2)   # 20 mm out of the tool: the API's -Z
rbt.move_c(via=[0, 250, 250, 90, 0, 90], end=[0, 263, 242, 90, 0, 90], speed=0.5)
rbt.move_s([[0, 263, 242, 90, 0, 90], [50, 250, 200, 90, 0, 90]], speed=0.5)
rbt.move_p(waypoints, speed=0.8)
```

## Speed, acceleration, duration

`speed` and `accel` are fractions of the robot model's maxima in (0, 1], default 0.5 each. For a joint move
they scale the leading joint; for a Cartesian move they scale the tool's linear and angular limits, with the
joint limits as hard bounds. A `duration` in seconds times the move instead and `speed` is ignored; `duration`
and `speed` are not combined. The move's actual speed is also capped by what the profile and the limits allow:
a short move never reaches the asked speed.

```python
rbt.move_l(target, speed=0.25, accel=1.0)      # a quarter of the Cartesian speed limit, full acceleration
rbt.move_l(target, duration=2.0)               # two seconds, whatever that takes
```

## Blending

`r`, in millimetres, on `move_j`, `move_l` and `move_c`: the move does not stop at its target but blends into the
next queued move within that radius ([Blending](https://docs.source-robotics.com/PAROL-docs/1.1/theory/blending/)). `move_p` blends on its own.

## Profiles

`select_profile("TOPPRA")` and the others set how the speed curve is shaped for all planned moves
([Motion profiles](https://docs.source-robotics.com/PAROL-docs/1.1/theory/motion-profiles/)); `profile()` reads it. The profiles of this version:
`TOPPRA`, `RUCKIG`, `QUINTIC`, `TRAPEZOID`, `LINEAR`.

## Waiting

`wait=True`, the default, blocks until the move completes and raises `MotionError` if it was cancelled or
failed; `TimeoutError` if the `timeout` runs out first, in which case the move is still queued and `stop()`
cancels it. `wait=False` returns the index for a later `wait_command()`; `wait_motion()` waits for the whole
queue and for the arm to come to rest ([Status and waiting](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/status-and-waiting/)).

## Execution speed and pause

`set_execution_speed(0.5)` runs the queued trajectory at half its planned speed from now on, 10 to 100 %;
`pause()` decelerates the queue to a hold and `resume()` continues it. Both keep the queue. A paused robot's
`execution_speed().paused` is true once it has actually stopped.

## Refusals

A target outside the joint limits, a pose the IK cannot solve, a path that collides, an unhomed robot, a latched
protective stop: the command is refused before anything moves, with a `MotionError` whose code says why
([Errors](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/errors/)). A refused command cancels nothing already queued; a command that **fails while running**
cancels everything queued behind it.
