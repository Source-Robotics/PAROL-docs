# Jogging and servoing

Streamed motion: takes the arm at once, cancels the planned queue (`MOTN_CANCELLED` for every discarded
command), and ends about 0.25 s after the last command, when the arm brakes to rest. Speeds are signed fractions
in [−1, 1] for jogs and fractions in (0, 1] for servo targets. [Jogging and servoing](../../programming/02-python-api/streaming.md)
in the guide.

<!-- api: jog_j -->

<!-- api: jog_l -->

!!! note
    Axis names: `X`, `Y`, `Z`, `RX`, `RY`, `RZ`; frames `WRF` and `TRF`. Jogs are clamped to 80 % of the limits.

<!-- api: servo_j -->

<!-- api: servo_l -->

<!-- api: stream_status -->

<!-- api: stream_status_shared -->
