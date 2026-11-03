# Firmware parameters

The per-joint parameters of the control board's main firmware (`constants.h`, `motor_init.cpp`, `main.cpp` at
release V1): what a builder edits when mastering, fitting a different tool, reducing the currents, or fixing a
joint's direction. Steps are 32-microstep motor steps. [Firmware](https://docs.source-robotics.com/PAROL-docs/1/board/08-firmware/) says how to upload a
change.

## Currents (`constants.h`)

| Define | Value | Note |
|---|---|---|
| `MICROSTEP` | 32 | |
| `MOTOR1_MAX_CURRENT` | 2000 mA | motor rated 2100 |
| `MOTOR2_MAX_CURRENT` | 2000 mA | motor rated 2100 |
| `MOTOR3_MAX_CURRENT` | 1900 mA | motor rated 2000 |
| `MOTOR4_MAX_CURRENT` | 1700 mA | reduced: the motor is enclosed in the forearm |
| `MOTOR5_MAX_CURRENT` | 1700 mA | reduced: enclosed |
| `MOTOR6_MAX_CURRENT` | 965 mA | motor rated 1000 |
| `VERSION` | 1 | |

The driver is set to `MOTORx_MAX_CURRENT × 0.85` as the running current and `hold_multiplier` of that for holding
(the per-joint table below has both); the driver rounds them to its own current steps.

## Per joint (`motor_init.cpp`)

| Parameter | J1 | J2 | J3 | J4 | J5 | J6 |
|---|---|---|---|---|---|---|
| `reduction_ratio` | 6.4 | 20 | 18.0952 | 4 | 4 | 10 |
| `standby_position` (steps at standby) | 10240 | −32000 | 57905 | 0 | 0 | 32000 |
| `homed_position` (steps from the switch to standby) | 13500 | 19588 | 23020 | −10200 | 8900 (`j5_homing_offset`) | 15900 |
| `joint_range_positive_steps` | 14000 | −1200 | 92605 | 7500 | 6400 | 64000 |
| `joint_range_negative_steps` | −14000 | −51587 | 34700 | −7500 | −6400 | 0 |
| `limit_switch_trigger` (input level when triggered) | 0 (inductive) | 1 (switch) | 1 (switch) | 0 (inductive) | 1 (switch) | 0 (inductive) |
| `direction_reversed` | 1 | 0 | 1 | 0 | 0 | 1 |
| `hold_multiplier` | 0.7 | 0.8 | 0.8 | 0.8 | 0.8 | 0.88 |
| Running current, `MOTORx_MAX_CURRENT × 0.85` | 1700 mA | 1700 mA | 1615 mA | 1445 mA | 1445 mA | 820 mA |
| Holding current, the running current × `hold_multiplier` | 1190 mA | 1360 mA | 1292 mA | 1156 mA | 1156 mA | 722 mA |
| Driver position / LIMIT input | 1 / 6 | 6 / 2 | 5 / 3 | 4 / 4 | 2 / 5 | 3 / 1 |

Joint 1's standby of 10240 steps is +90° (90 / 0.05625 × 6.4): the firmware homes to the pose the software
reports as J1 = 90°. The firmware's "standby" is what these pages call the after-homing pose: the standby
pose turned 90° about joint 1 ([Joint limits and directions](https://docs.source-robotics.com/PAROL-docs/1/03-technical-data/joint-limits/#standby-and-after-homing)).

## Joint 5 and the tool (`main.cpp`)

| Variable | Value | Note |
|---|---|---|
| `j5_homing_offset` | 8900 | the pneumatic gripper holder; **8035** for the SSG-48 |

## Homing speeds and distances (`main.cpp`, `home_all`)

The approach speeds in steps/s: J1 −2050, J2 −2550, J3 −2550, J4 5550, J5 −5050, J6 −9550; the back-off
distances 850 (J1), 1050 (J2, J3), 1550 (J4, J5, J6) steps; the slow re-approach −750 steps/s for joints 1 to 3,
±4050 for 4 and 5, −8050 for 6. The firmware uses the second, slow trigger as the reference.

## The serial link

`Serial.begin(3000000)`; the timing counter runs at 90 MHz / 128 = 703 125 Hz.
