# Motion profiles

A move has a start, an end and a time; the profile is how the speed changes in between. The profile decides how
smooth the move is, how much it shakes the arm, and whether the steppers can follow it.

## Trapezoidal

Accelerate at a constant rate, cruise at the maximum speed, decelerate at the same rate. The speed curve is a
trapezoid; the acceleration jumps between +a, 0 and −a, which is felt as a jerk at the three corners. With the
commander's `t=` argument, each third of the move is one phase.

![A trapezoidal velocity profile](../../assets/trap.webp){ width="700" }

## Polynomial

A quintic (fifth-order) polynomial through the start and end positions with zero speed and zero acceleration at
both ends: the speed rises and falls as a smooth bell, the acceleration is continuous, and the move starts and
ends from rest without a jolt. Slower in the middle for the same total time, and the arm likes it better.

![A quintic polynomial velocity profile](../../assets/poly.webp){ width="700" }

## In the commander software

`MoveJoint`, `MovePose`, `MoveCart` and `MoveCartRelTRF` take `func="trap"` or `func="poly"`; a move with `t=`
defaults to polynomial, a move with `v=` and `a=` is trapezoidal, and a move with neither runs a conservative
trapezoid ([RBTscript](../04-commander/rbtscript.md)).

## In the Python API

`select_profile()` sets the profile for all planned moves. The profiles of the version this site describes:
<!-- api-profiles -->.

| Profile | What it is |
|---|---|
| `TOPPRA` | Time-optimal path following: the fastest run along the given path within the joint speed and acceleration limits. The default |
| `RUCKIG` | Jerk-limited point-to-point motion: acceleration ramps instead of jumping. Joint moves only; a Cartesian move under it runs TOPPRA |
| `QUINTIC` | The quintic polynomial above, C² smooth |
| `TRAPEZOID` | Trapezoidal, with parabolic blends at the corners |
| `LINEAR` | Straight interpolation, no smoothing: for tests |

The move's `speed` and `accel` fractions scale the limits the profile works within; a `duration` fixes the time
instead. Streamed jogs and servo targets use their own jerk-limited profile in the controller, not the selected
one.

## Why the profile matters for a stepper arm

A stepper follows a speed command exactly until the torque runs out; a sudden acceleration demand at a corner
is where it runs out first. Smooth profiles, lower accelerations and lower currents go together: if a joint loses
steps at the start of moves, a quintic or jerk-limited profile at the same speed often fixes it.
