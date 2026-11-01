# Jogging and servoing

Streamed motion is for a hand on a button or a loop that computes the next target: a jog is a velocity held for
a short time, a servo target is a position to go to now. Both bypass the queue, take the arm at once (the queue
is cancelled), and stop about 0.25 s after the last command, when the arm brakes to rest and holds.

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

- Streamed motion needs a homed robot, like planned motion.
- It cancels the planned queue: every queued command fails with `MOTN_CANCELLED`. Do not interleave a servo
  stream with planned moves you still want.
- Keep the targets reachable and the steps between them small; a target far from the current pose is a fast
  move at the asked speed.
- Collision checking applies to jogs with a look-ahead (`PAROL6_COLLISION_JOG_LOOKAHEAD_S`).

## Status while streaming

The status stream reports `action_state` and the actual angles at 50 Hz; `stream_status()` on the async client is
the natural partner of a servo loop ([Status and waiting](status-and-waiting.md)).
