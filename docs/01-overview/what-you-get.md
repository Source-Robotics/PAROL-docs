# What you get

## An assembled robot

A PAROL6 [from the shop](https://source-robotics.com/products/parol6-robotic-arm) comes assembled, wired and tested, with the control board in the base running the main
firmware, the E-stop button, the pneumatic gripper holder, and the robot homed once on the bench. Check the
contents against the order; the power supply, grippers and the programming adapter are separate items unless the
order includes them.

## A kit

The [full kit](https://source-robotics.com/products/parol6-robotic-arm-kit) contains every part of the [BOM](../build/bill-of-materials.md) except the printed parts
and the power supply. The [partial kit](https://source-robotics.com/products/parol6-partial-kit) contains the hard-to-find parts: the board, the drivers, the
bearings, belts, pulleys, connectors, sensors, switches and the pneumatics; you add the gearboxes, the motors,
the power supply and the printed parts. The [Build guide](../build/index.md#kits) lists every kit. You assemble
a kit with the Build guide and the assembly manual. The control board in a kit carries the test firmware, as
every control board from the shop does: it turns all six motors as soon as it starts. Upload the main firmware
before you switch on the assembled robot ([Firmware and first run](../build/firmware-and-first-run.md)).

## A control board on its own

Every control board is tested end to end before it ships and comes with the **test firmware**, which exercises
the drivers, the switches and the I/O from a serial terminal. Upload the main firmware before you use it with the
commander software or the Python API: [Firmware](../board/08-firmware.md).

## The files

Everything else you get is on GitHub: the STL and STEP files, the BOM with purchase links, the building
instructions PDF and the video playlist, the firmware sources, the software. [Downloads and files](../cad-files.md)
lists them.
