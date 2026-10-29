# Bill of materials

The complete BOM with purchase links and reference images is
[BOM.md in the repository](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/main/BOM/BOM.md).
This page is the summary; the links there are the ones to use, and some are affiliate links that support the
project.

## Motors and gearing

| Part | Quantity | Note |
|---|---|---|
| NEMA 17 stepper, 65 N·cm, 60 mm (17HS24-2104S) | 2 | joints 1 and 2 |
| NEMA 17 stepper, 45 N·cm, 40 mm (17HS16-2004S1) | 3 | joints 3, 4, 5 |
| NEMA 17 stepper, 16 N·cm, 20 mm (17HS08-1004S) | 1 | joint 6 |
| EG planetary gearbox 20:1 | 2 | joints 2 and 3; MG series fits with more backlash |
| EG planetary gearbox 10:1 | 1 | joint 6 |
| HTD3 belts 396, 342, 201, 246 mm, 6 mm wide | 1 each | joints 1, 3, 4, 5 |
| HTD3M pulleys: 12 teeth ×2, 15 teeth ×1, 5 mm bore | 3 | joints 4 and 5; joint 1 |
| Shaft couplers, 8 mm bore, M4 screws | 3 | |

## Bearings

| Part | Quantity |
|---|---|
| AXK3552 needle thrust bearing with plates | 1 |
| NSK HR32906J tapered roller bearing | 5 (joints 3, 4, 5) |
| NSK HR32907J tapered roller bearing | 4 (joints 1, 2) |
| 3 × 8 × 4 mm ball bearings | 20 (belt tension) |
| 3 × 10 × 4 mm ball bearings | 20 (belt tension) |

## Electronics

| Part | Quantity | Note |
|---|---|---|
| PAROL6 control board | 1 | [the shop](https://source-robotics.com/products/parol6-control-board) |
| TMC5160 stepper driver modules | 6 | the tested ones from the BOM's links; others at your own risk |
| Thermal cement | | only if the board comes without drivers |
| 24 V 5 A power supply | 1 | Mean Well EDR-120-24 or any 24 V 5 A |
| Power button, 12 mm, 3 to 6 V LED, and JST PH 4-pin cable | 1 | |
| 40 mm 5 V fan (Noctua NF-A4x20 5V) | 1 | not a PWM fan |
| GX16 2-pin connector pair, XT30 female | 1 | power in |
| M8 4-pin female connector | 1 | the gripper |
| Limit switches ZW12-3 | 3 | joints 2, 3, 5 |
| Inductive sensors: 4 mm NPN NO, GX-F8A, M5 NPN NO | 1 each | joints 1, 4, 6 |
| E-stop, normally closed, and a PG7 cable gland | 1 | |
| M3 brass inserts, 6 mm | 4 | |
| ST-Link programming adapter | 1 | [the official adapter](https://source-robotics.com/products/parol6-programming-adapter), or an ST-Link with the right pin order |
| USB type B cable | 1 | |

## Pneumatics

MHZ2-16D gripper, two PC4-M5 fittings, four 4 mm PM fittings for the robot, 5 m of 4 × 2.5 mm tube, a 5/2
solenoid valve, 24 V. For a vacuum gripper: a suction cup, a vacuum generator and a 4 to 6 mm coupler.

## Screws

About 250 screws, M2 to M4, mostly DIN 912 socket heads: the full list is in the BOM. Buy a box of each size
rather than counting.

## For a small print bed

If your printer cannot fit the J1 turret blocker or the upper arm, both are split in two in `STL/SMALL_PRINT_BED`
and joined with dowel pins (4 × 18 mm ×3, 6 × 22 mm ×4) and slow two-part epoxy. Nothing else changes.
