# I/O, delays and checkpoints

## Digital I/O

The control board's two inputs, two outputs and the E-stop, as the firmware reports them:

```python
state = rbt.io()                 # [in1, in2, out1, out2, estop], or None on a timeout
rbt.write_io(0, 1)               # output 1 high; logical index 0 = the first output
rbt.write_io(1, 0, timeout=1.0)  # raises TimeoutError if not confirmed in time
```

The firmware's I/O byte is `[in1, in2, out1, out2, estop, ...]`, so logical output 0 is bit 2 of the byte;
`write_io` does the mapping. `is_estop_pressed()` reads the E-stop alone. A per-call `timeout` bounds the setup,
the retries and the reply; without one the client's defaults apply.

A write is queued with the motion: it takes effect when its turn in the queue comes, and it returns a command
index that `wait_command()` waits on. The pneumatic gripper's `open()` and `close()` are output writes of the same
kind. While the controller is disabled, after `estop()` or the E-stop until `reset()`, a write is refused with
`SYS_CONTROLLER_DISABLED`, like a move.

### Switching an output at a point of a program

Queue the write between the two moves it belongs between. The output changes when the first move has finished,
and the second move starts after it:

```python
rbt.move_l([0, 263, 200, 90, 0, 90], speed=0.5, wait=False)   # to the part
rbt.write_io(0, 1)                                              # output 1 high, once the arm is there
rbt.delay(0.5)                                                  # let the valve act
rbt.move_l([0, 263, 242, 90, 0, 90], speed=0.5, wait=False)   # away again
rbt.write_io(0, 0)                                              # output 1 low at the end
rbt.wait_motion()
```

A `checkpoint()` is for something outside the robot that must know when the queue reaches a point; the outputs
do not need one.

## Delays

```python
rbt.delay(1.0)                   # a second of nothing, in the queue
```

A queued delay holds the arm for its duration at its place in the queue; it is not `time.sleep()`, which would
hold your script and not the robot. A paused queue keeps the delay's remaining time.

## Checkpoints

```python
index = rbt.checkpoint("pick_done")
...
rbt.wait_checkpoint("pick_done", timeout=30)
```

A checkpoint is a labelled marker in the queue; `wait_checkpoint()` blocks until the queue reaches it, and the
status stream reports `last_checkpoint`. It is how a program synchronises something outside the robot, a
conveyor or a camera, with a point in the motion.
