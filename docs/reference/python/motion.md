# Motion

Planned moves: queued, run in order, each returning its command index. `wait=True` (the default) blocks until the
command completes and raises `MotionError` if it failed or was cancelled; `wait=False` returns at once for a later
`wait_command()`. Either `duration` or `speed` times a move, not both. [Motion](../../programming/03-python-api/motion.md)
in the guide explains the choices.

<!-- api: home -->

!!! note
    The referencing sequence is the firmware's ([Homing](../../05-operation/homing.md)): it ignores the collision
    world, and it takes about half a minute. A later `home()` is a planned joint move to standby.

<!-- api: move_j -->

<!-- api: move_l -->

<!-- api: move_c -->

<!-- api: move_s -->

<!-- api: move_p -->
