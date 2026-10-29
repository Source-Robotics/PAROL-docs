# Printing the parts

## Material

PETG. The motors run warm and the parts around them see 60 to 70 °C in long use, which PLA does not survive;
PETG softens around 80 °C, prints without an enclosure, and bonds layers well. ABS or ASA work with an enclosure.
The repository's [PETG notes](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/main/Building%20instructions/PETG_printing.md)
give the printing basics: hot end 220 to 250 °C, bed 60 to 90 °C with glue, a layer fan, and the warping is
small.

## The files

All parts are in the repository's [`STL`](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL) folder, grouped by link:
[`BASE`](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL/BASE), [`SHOULDER`](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL/SHOULDER), [`UPPER_ARM`](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL/UPPER_ARM), [`ELBOW`](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL/ELBOW), [`FOREARM`](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL/FOREARM), [`WRIST`](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL/WRIST), [`ESTOP`](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL/ESTOP), [`GRIPPER_ATTACHMENTS`](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL/GRIPPER_ATTACHMENTS), [`UTILITY`](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL/UTILITY), [`mounting plates`](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL/mounting%20plates),
and [`SMALL_PRINT_BED`](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL/SMALL_PRINT_BED) for the split versions of the two largest parts.
The print table below says how each was printed on the reference robots; it is a tested starting point, not a
rule.

## Print table

The repository's [print table](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/main/Print%20table/PR_EXCEL.xlsx) (`Print table/PR_EXCEL.xlsx`,
also as a [PDF](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/main/Print%20table/Print_table.pdf)), copied as it is: a row per part with the
supports, infill, mass, print time, cooling, layer height, top and bottom layers and perimeters used on the
reference robots. 0.2 mm layers, 3 perimeters, 6 top and 4 bottom layers, honeycomb infill and 15 % cooling
throughout; PETG.

--8<-- "generated/print_table.md"

Print the pulleys with high infill and slow outer walls: their teeth carry the load. Check the first printed
pulley against a belt before printing the rest.

## Tolerances

Bearing seats and shafts are designed for a well-calibrated printer; a seat that is too tight is reamed, one
that is too loose is shimmed with tape or a drop of epoxy. Test the fit of the tapered bearings in their seats
before assembling a joint.

## Inserts

Four M3 brass inserts are melted into their holes with a soldering iron; everything else screws directly into the
plastic.
