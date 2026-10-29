# Drives, ratios and resolution

## Motors and gearing

| Joint | Motor | Gearing | Ratio |
|---|---|---|---|
| Joint 1 | NEMA 17, 65 N·cm (60 mm) | HTD3 belt, 15-tooth pulley to a 96-tooth printed pulley | 6.4 : 1 |
| Joint 2 | NEMA 17, 65 N·cm (60 mm) | EG planetary gearbox | 20 : 1 |
| Joint 3 | NEMA 17, 45 N·cm (40 mm) | EG planetary gearbox 20 : 1, then a belt 38 : 42 | 18.095 : 1 |
| Joint 4 | NEMA 17, 45 N·cm (40 mm) | HTD3 belt, 12-tooth pulley to 48 teeth | 4 : 1 |
| Joint 5 | NEMA 17, 45 N·cm (40 mm) | HTD3 belt, 12-tooth pulley to 48 teeth | 4 : 1 |
| Joint 6 | NEMA 17, 16 N·cm (20 mm) | EG planetary gearbox | 10 : 1 |

The planetary gearboxes are the precision EG series with 15 to 20 arc-minutes of backlash; the cheaper MG series
fits and works, with more backlash. The belts are 6 mm wide HTD3, tensioned by small bearings; their lengths are
in the [BOM](../build/bill-of-materials.md).

## Steps and microsteps

The stepper motors have 200 full steps per turn. The control board runs the TMC5160 drivers at 32 microsteps, so
one motor turn is 6400 microsteps, and every position and speed the firmware and the PC exchange is in these
steps. Through the gearing, one step at the joint is:

| Joint | Steps per joint turn | Step size |
|---|---|---|
| Joint 1 | 40 960 | 0.00879° (0.000153 rad) |
| Joint 2 | 128 000 | 0.00281° (0.000049 rad) |
| Joint 3 | 115 810 | 0.00311° (0.000054 rad) |
| Joint 4 | 25 600 | 0.01406° (0.000245 rad) |
| Joint 5 | 25 600 | 0.01406° (0.000245 rad) |
| Joint 6 | 64 000 | 0.00563° (0.000098 rad) |

Conversions: degrees per step = 360 / (200 × 32) / ratio; the software's `DEG2STEPS` and `STEPS2DEG` do exactly
this. A microstep is not a guaranteed position: the motor's holding torque at a fraction of a full step is small,
so the real resolution under load is coarser than the table, which is why the repeatability is specified at
0.1 mm rather than at the step size.

## Why open loop works here

The motors are not fitted with encoders: the position is the count of steps commanded since homing. This works
because the planner never asks a motor for more than its torque at the commanded speed and acceleration, with
margin; a stepper that is not overloaded does not lose steps. If one is overloaded (a collision, a payload over
the limit, too high a speed with a reduced current) it loses steps silently, the arm is then not where the
software thinks it is, and the only cure is to home again. [Steppers, open loop and backlash](../programming/02-concepts/steppers-and-open-loop.md)
goes deeper.
