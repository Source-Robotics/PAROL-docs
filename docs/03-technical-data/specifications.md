# Specifications

| Parameter | Value |
|---|---|
| Degrees of freedom | 6 revolute joints |
| Reach | 408 mm to the flange, 434 mm to the standard pneumatic gripper's TCP, from the axis of joint 1 |
| Payload | 1 kg near the base, 0.5 kg across the full workspace |
| Repeatability | 0.1 mm |
| Weight | 5.5 kg |
| Material | 3D-printed PETG, steel shafts and bearings |
| Motors | NEMA 17 stepper motors, one per joint |
| Gearing | Planetary gearboxes (joints 2, 3, 6) and HTD3 belts (joints 1, 3, 4, 5) |
| Position reference | Limit switches (joints 2, 3, 5) and inductive sensors (joints 1, 4, 6); no joint encoders |
| Brakes | None: the arm falls when the motors lose power |
| Power supply | 24 V DC, 5 A (18 V minimum) |
| Power consumption | About 40 W typical |
| Control | PAROL6 control board (STM32F446, six TMC5160 drivers) in the base |
| PC connection | USB, serial at 3 Mbaud, 100 Hz command cycle |
| Inputs and outputs | 2 isolated inputs, 2 isolated outputs, E-stop input |
| Buses | 1 CAN bus for electric grippers (a second is on the board, not populated) |
| Tool connections | M8 4-pin gripper connector (24 V, CAN) at the forearm; 2 pneumatic lines, 4 mm tube, base to forearm |
| Mounting | 6 holes in the base, spaced for 30×30 mm aluminium profiles; clamps |
| Operating temperature | Room temperature; the printed parts limit the motor temperatures ([Currents and temperatures](operating-temperatures.md)) |

## Joint ranges

| Joint | Range |
|---|---|
| Joint 1 | 194.8° (±97.4°) |
| Joint 2 | 113.4° |
| Joint 3 | 189.1° |
| Joint 4 | 229.2° (±114.6°) |
| Joint 5 | 240.6° (±120.3°) |
| Joint 6 | 360° in software; mechanically unlimited, but see [Moving the robot by hand](../02-safety/moving-by-hand.md) |

The ranges are those of the robot's model (robot_descriptions 2.13.0); the exact limits are on
[Joint limits and directions](joint-limits.md).

## Speeds

The speed limits are set in the PC software, not in the firmware, and the two programs differ: the commander
software is the more conservative.

| Joint | Python API: maximum speed | Python API: acceleration | Commander: maximum speed |
|---|---|---|---|
| Joint 1 | 132 °/s (15000 steps/s) | 395 °/s² | 57 °/s (6500 steps/s) |
| Joint 2 | 70 °/s (25000 steps/s) | 211 °/s² | 51 °/s (18000 steps/s) |
| Joint 3 | 99 °/s (32000 steps/s) | 298 °/s² | 62 °/s (20000 steps/s) |
| Joint 4 | 141 °/s (10000 steps/s) | 422 °/s² | 309 °/s (22000 steps/s) |
| Joint 5 | 141 °/s (10000 steps/s) | 422 °/s² | 309 °/s (22000 steps/s) |
| Joint 6 | 152 °/s (27000 steps/s) | 456 °/s² | 124 °/s (22000 steps/s) |
| Tool, linear | 200 mm/s | 550 mm/s² | 60 mm/s |
| Tool, angular | 100 °/s | 275 °/s² | 25 °/s |

The steps per second are converted with the ratios of [Drives, ratios and resolution](drives-and-ratios.md). In
the Python API the acceleration is three times the speed, so a joint reaches full speed in a third of a second,
and jogging is limited to 80 % of the maxima; the commander scales its limits with the speed slider. A joint
driven at its maximum with a reduced motor current or a heavy payload loses steps: lower the speed before you
lower the current.
