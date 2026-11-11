# Installation site

- **A rigid table or frame.** The arm accelerates its 5.5 kg quickly; a wobbly table shakes and spoils the
  repeatability. An aluminium profile frame or a solid bench is right.
- **Clearance.** The flange reaches 408 mm from the axis of joint 1 in front of the base and 359 mm behind it,
  plus the tool, and the elbow swings behind the base when the arm folds
  ([Workspace](../03-technical-data/kinematics.md#workspace)). Keep a free sphere of about 500 mm around the base
  with the pneumatic gripper, about 600 mm with the SSG-48 or the MSG, and nothing fragile in it. The simulator
  shows the sweep of a program before the robot runs it.
- **Room temperature, dry, dust-free.** The base draws air through its fan over the stepper drivers.
- **The E-stop within reach** of the person at the PC, and reachable from where someone would stand to load the
  robot.
- **Cables.** The power, USB and E-stop cables leave the base at the back; route them so that nothing pulls on
  them and so that the arm cannot sweep over them.
- **Pneumatics.** If you use the pneumatic gripper, a valve and an air supply at 5 to 7 bar near the base; check
  your gripper's rating ([Pneumatics](../06-peripherals/pneumatics.md)).
- **A mains switch within reach** on the power supply's mains side, a switched socket strip for example: the stop
  for when the PC software has frozen ([Emergency stop](../02-safety/emergency-stop.md)).

The [Planning the cell](../02-safety/planning-the-cell.md) page covers the safety side: who can reach the robot,
guarding, and what the software can and cannot stop.
