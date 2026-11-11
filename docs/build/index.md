# Build guide

PAROL6 is open hardware: you can print the parts, buy the rest from the bill of materials and build the robot
yourself. This guide is the order to do it in, with the facts that are not in the assembly manual; the step by
step assembly is in the [building instructions PDF](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/Building%20instructions)
and the [video playlist](https://www.youtube.com/playlist?list=PLSueoDrBt5MMTL9O8qAWZiJrNIf8-29Qz).

!!! warning
    A self-built robot is yours to make safe: the motor currents, the wiring, the switches and the stops. Read the
    [Safety](../02-safety/index.md) chapter before the first power-on, as you would for a bought one.

## The steps

1. [Bill of materials](bill-of-materials.md): what to buy
2. [Printing the parts](printing.md): the material, the settings, the print table
3. [Mechanical assembly](mechanical-assembly.md): the manual, the videos, the things to get right
4. [Electronics and wiring](electronics-and-wiring.md): the control board, the drivers, the motors, the switches
5. [Firmware and first run](firmware-and-first-run.md): the test firmware, the main firmware, directions, homing

## Kits

You do not have to source everything yourself. The [shop](https://source-robotics.com/collections/all) sells the
robot in every state between a bag of parts and a working arm:

| | What is in it | You add |
|---|---|---|
| [Assembled robot](https://source-robotics.com/products/parol6-robotic-arm) | the robot, built, tested and ready for the commander software | nothing |
| [Full kit](https://source-robotics.com/products/parol6-robotic-arm-kit) | every part of the BOM except the printed parts and the power supply | the printed parts, a 24 V 5 A supply |
| [Partial kit](https://source-robotics.com/products/parol6-partial-kit) | the hard-to-find parts: the board, the drivers, the bearings, belts, pulleys, connectors, sensors, switches, the pneumatics | the gearboxes, the stepper motors and the power supply, which are heavy to ship and cheaper from a supplier near you; the printed parts |
| [Printed parts kit](https://source-robotics.com/products/parol6-3d-printed-parts-kit) | every printed part, in PETG, in several colours | everything else |
| [Screw kit](https://source-robotics.com/products/parol6-screw-kit) | every screw and nut of the BOM, counted | everything else |
| [Control board](https://source-robotics.com/products/parol6-control-board), [programming adapter](https://source-robotics.com/products/parol6-programming-adapter) | the electronics alone | everything else |

The partial kit is the best value for a builder with a printer: it carries the parts that are hard to find or
easy to get wrong, and leaves out the three items a local supplier sells cheaper than we can ship them. A full
kit skips the bill of materials; a printed parts kit skips the printing.
