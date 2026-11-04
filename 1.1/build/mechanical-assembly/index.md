# Mechanical assembly

The assembly is documented step by step in the
[Parol building instructions PDF](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/main/Building%20instructions/Parol%20building%20instructions.pdf)
and shown in the [video playlist](https://www.youtube.com/playlist?list=PLSueoDrBt5MMTL9O8qAWZiJrNIf8-29Qz).
Read the whole manual once before you start: some steps cannot be undone without taking the joint apart again.
This page lists what to get right.

## The building instructions

<object data="../../assets/pdf/PAROL6_building_instructions.pdf#view=FitH&amp;navpanes=0" type="application/pdf" width="100%" height="820">
  <p>Your browser does not show PDFs inline: <a href="../../assets/pdf/PAROL6_building_instructions.pdf">download the building instructions (PDF, 8 MB)</a>.</p>
</object>

[Download the building instructions (PDF, 8 MB)](https://docs.source-robotics.com/PAROL-docs/1.1/assets/pdf/PAROL6_building_instructions.pdf)

## Things to get right

- **Bearings seated square**: the tapered roller bearings carry the joint; a bearing that sits crooked makes the
  joint stiff in one direction and loose in the other.
- **Belt tension** as in the [belt tension video](https://www.youtube.com/watch?v=v0PYfEoIr3k): maximum hand
  force for joints 3 and 5, slightly less for 1 and 4, with the tension bearings ([Belts](https://docs.source-robotics.com/PAROL-docs/1.1/07-maintenance/belts/)).
- **Threadlocker** on every metal-to-metal screw, blue, and on all set screws ([Couplers and threadlocker](https://docs.source-robotics.com/PAROL-docs/1.1/07-maintenance/couplers/)).
  The couplers between motors, gearboxes and shafts are where a loose screw costs the most.
- **The limit switches and sensors** positioned so that the moving part presses the lever, or passes the sensor
  within a millimetre or two, before the joint reaches its mechanical stop.
- **Joint 1's blockers** fitted: without them joint 1 can spin a full turn and tear its wires.
- **Wires and tubes** with enough slack through each joint for its full range, and fixed so that they cannot be
  pinched by the belts.
- **Wire markings**: the print table spreadsheet's *Wire_markings* sheet lists the colour code of the motor and
  sensor cables used on the reference robots, which helps when the base is wired.

## Small print beds

The J1 turret blocker and the upper arm come split in `STL/SMALL_PRINT_BED`, with a README. Join the halves with
the dowel pins and slow epoxy, clamp them straight, and let them cure before the joint is assembled.

## Custom couplers and flanges

The repository's `custom_couplers.md` is a work in progress on machined alternatives to the shaft couplers, with
a press-fit flange; use the BOM's couplers until it is finished.

## Before the electronics

Turn every joint by hand through its range. Everything should move smoothly against the gearbox's resistance,
with no clicks and no tight spots, and every switch should click as its joint reaches it.
