# Jogging and servoing

Streamed motion is for a hand on a button or a loop that computes the next target: a jog is a velocity held for
a short time, a servo target is a position to go to now. Both bypass the queue and take the arm at once (the
queue is cancelled). They end differently:

- **A jog** runs for its `duration` (0.1 s by default), then the arm brakes to rest and holds. A held button sends
  a new jog before the last one runs out.
- **A servo stream** ends about 0.25 s after the last target arrives, when the arm brakes to rest and holds.

## Jogging

```python
rbt.jog_j(0, speed=0.3, duration=0.5)                             # joint 1 (index 0), 30 %, 0.5 s
rbt.jog_j(joints=[1, 2], speeds=[0.2, -0.2], duration=1.0)        # two joints
rbt.jog_l("WRF", "X", speed=0.2, duration=0.5)                    # the tool along world X
rbt.jog_l("TRF", axes=["Z", "RZ"], speeds_list=[0.2, 0.1], duration=0.5)
```

Speeds are signed fractions of the maximum in [−1, 1]; the controller clamps jogs to 80 % of the limits. A GUI
sends a jog every few tens of milliseconds while the button is held; the controller de-duplicates repeated
targets and extends the motion. A jog stops at a joint limit, and a Cartesian jog stops before a singularity.

## Servoing

```python
rbt.servo_j([90, -90, 180, 0, 0, 180], speed=0.5, accel=0.5)       # go to these angles, now
rbt.servo_j(pose=[0, 263, 242, 90, 0, 90])                          # via IK
rbt.servo_l([0, 263, 242, 90, 0, 90], speed=0.5)                    # a straight line to the pose
```

A servo target is fire-and-forget: the controller plans a jerk-limited motion from where the arm is to the
target and follows it, re-planning as new targets arrive. A stream of targets at 20 to 100 Hz gives smooth
tracking of a moving goal, which is how teleoperation and following a camera are built. The stream ends a
quarter second after the last target.

## Rules

- Cartesian jogs (`jog_l`) and servo targets need a homed robot, like planned motion; they are refused with
  `MOTN_NOT_HOMED` before it. Joint jogs (`jog_j`) work before homing, so that an arm can be jogged clear of an
  obstruction first.
- It cancels the planned queue: every queued command fails with `MOTN_CANCELLED`. Do not interleave a servo
  stream with planned moves you still want.
- Keep the targets reachable and the steps between them small; a target far from the current pose is a fast
  move at the asked speed.
- Collision checking applies to jogs with a look-ahead (`PAROL6_COLLISION_JOG_LOOKAHEAD_S`).

## Status while streaming

The status stream reports `action_state` and the actual angles at 50 Hz; `stream_status()` on the async client is
the natural partner of a servo loop ([Status and waiting](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/status-and-waiting/)).
