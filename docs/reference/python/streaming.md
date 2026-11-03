# Jogging and servoing

Streamed motion: takes the arm at once and cancels the planned queue (`MOTN_CANCELLED` for every discarded
command). A jog ends when its `duration` runs out; a servo stream ends about 0.25 s after the last target. Then
the arm brakes to rest. Speeds are signed fractions in [−1, 1] for jogs and fractions in (0, 1] for servo
targets. `jog_j` works before homing; `jog_l` and the servo targets need a homed robot.
[Jogging and servoing](../../programming/02-python-api/streaming.md) in the guide.

<!-- api: jog_j -->

<!-- api: jog_l -->

!!! note
    Axis names: `X`, `Y`, `Z`, `RX`, `RY`, `RZ`; frames `WRF` and `TRF`. Jogs are clamped to 80 % of the limits.

<!-- api: servo_j -->

<!-- api: servo_l -->

<!-- api: stream_status -->

<!-- api: stream_status_shared -->
