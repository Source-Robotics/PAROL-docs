# Units

Robotics mixes units, and PAROL6's software converts between them at several places. The rule is: the interfaces
speak degrees and millimetres, the firmware speaks motor steps, and the maths in between is in radians and
metres.

| Quantity | At the interface (commander GUI, RBTscript, Python API) | Inside the software | At the firmware |
|---|---|---|---|
| Joint angle | degrees | radians | motor steps (microsteps) |
| Position | millimetres | metres | — |
| Orientation | degrees (three angles) | rotation matrices, radians | — |
| Joint speed | commander: percent of the maximum; API: a fraction of the maximum in (0, 1] | rad/s | steps per second |
| Tool speed | commander: percent; API: a fraction | m/s, rad/s | — |
| Acceleration | percent, or a fraction | rad/s², m/s² | steps/s² |
| Time | seconds | seconds | 10 ms cycles; the timing counter in 1.422 µs ticks |
| Gripper position | commander: 0 to 255; API: a fraction 0 to 1 | | 0 to 255 |
| Gripper current | commander: milliamps; API: a fraction of the tool's current range | | milliamps |

## Steps

The firmware knows nothing but steps: 200 full steps per motor turn, 32 microsteps each, 6400 per turn, times the
joint's gear ratio for a turn of the joint ([Drives, ratios and resolution](https://docs.source-robotics.com/PAROL-docs/1/03-technical-data/drives-and-ratios/)).
The PC software converts with the two constants it keeps in its robot model:

```
degrees per step = 360 / (200 × 32) / ratio          # 0.05625° / ratio
steps = degrees / 0.05625 × ratio
```

## Speed fractions

The Python API's `speed` and `accel` are fractions of the robot model's maxima, in (0, 1], not percentages: a
`speed=0.5` joint move runs the leading joint at half its maximum speed, and the others proportionally so that
all finish together. A `duration` above zero overrides the speed: the move takes that long, whatever the speed
fraction says. The commander's speed slider is a percentage applied to its own, lower, maxima.

## Angles wrap

Joint 3 reports about 105° to 295° and joint 6 0° to 360°, both with the standby at 180°; joints 1, 2, 4 and 5
report signed angles. Orientation angles
wrap at ±180°: a pose with Rz = 179° and one with Rz = −181° are the same, and a program that compares angles
must take that into account.
