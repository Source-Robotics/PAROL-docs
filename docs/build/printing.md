# Printing the parts

## Material

PETG. The motors run warm and the parts around them see 60 to 70 °C in long use, which PLA does not survive;
PETG softens around 80 °C, prints without an enclosure, and bonds layers well. ABS or ASA work with an enclosure.
The repository's [PETG notes](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/main/Building%20instructions/PETG_printing.md)
give the printing basics: hot end 220 to 250 °C, bed 60 to 90 °C with glue, a layer fan, and the warping is
small.

## The files

All parts are in the repository's `STL` folder, grouped by link: `BASE`, `SHOULDER`, `UPPER_ARM`, `ELBOW`,
`FOREARM`, `WRIST`, `ESTOP`, `GRIPPER_ATTACHMENTS`, `UTILITY`, and `SMALL_PRINT_BED` for the split versions of
the two largest parts. The print table below says how each was printed on the reference robots; it is a tested
starting point, not a rule.

## Print table

0.2 mm layers, 3 perimeters, 6 top and 4 bottom layers, honeycomb or gyroid infill, 15 % cooling, PETG. The
infill and supports per part:

| Part | Where | Supports | Infill | Weight, time |
|---|---|---|---|---|
| Main base, electronics case, fan cover, J1 bottom lid | base | minimal | 50 % base and case, 20 to 25 % lids | |
| J1 turret and its blocker, J1 motor holder | shoulder | minimal | 25 % turret, 80 % motor holder | 210 g, 18 h (turret) |
| J1 rotation shaft, J2 shaft | shoulder | none | 50 % | 31 g and 43 g |
| J1 backplate, J1 belt cover, J2 cover, J2 bearing backplate, J2 stopper block | shoulder | none or minimal | 20 to 50 % | |
| Upper arm, upper arm cover, wires cover | upper arm | minimal | 35 % arm, 15 % cover | 220 g, 18 h (arm) |
| 38- and 42-tooth J3 pulleys, J3 limit switch cover | upper arm | none | 50 to 70 % | |
| Elbow part, elbow lids, J4 limiter, J4 bearing backplate | elbow | a lot (elbow part) | 25 % elbow, 80 % limiter | 215 g, 16 h (elbow) |
| J5 part, J5 belt lid, J5 electronics lid, J5 pulley, 48-tooth pulley, J4 output pulley | forearm | minimal | 30 % part, 15 % lids, 40 to 60 % pulleys | 114 g, 10 h (J5 part) |
| Wrist | wrist | minimal | 40 % | 78 g, 8 h |
| Pneumatic gripper holder, gripper arms, vacuum holder | tool | none | 30 to 40 % | |
| E-stop top and bottom | base | none | 20 % | |

The spreadsheet with every part is `Print table/PR_EXCEL.xlsx` in the repository. Print the pulleys with high
infill and slow outer walls: their teeth carry the load. Check the first printed pulley against a belt before
printing the rest.

## Tolerances

Bearing seats and shafts are designed for a well-calibrated printer; a seat that is too tight is reamed, one
that is too loose is shimmed with tape or a drop of epoxy. Test the fit of the tapered bearings in their seats
before assembling a joint.

## Inserts

Four M3 brass inserts are melted into their holes with a soldering iron; everything else screws directly into the
plastic.
