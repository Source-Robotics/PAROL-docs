# Inspection

With the robot switched off and the supply unplugged:

- **Belts** (joints 1, 3, 4, 5): press each with a finger through its cover opening; it should give a little and
  spring back. A belt that sags or that you can push against the pulley needs tensioning ([Belts](https://docs.source-robotics.com/PAROL-docs/1/07-maintenance/belts/)).
  Look for frayed edges and missing teeth.
- **Couplers and set screws**: hold the output of each joint and try to turn the motor side; any play that is not
  the gearbox's backlash is a loose set screw ([Couplers and threadlocker](https://docs.source-robotics.com/PAROL-docs/1/07-maintenance/couplers/)).
- **Limit switches and sensors**: press each switch lever; it should click. The inductive sensors' LEDs light
  when a screw head comes near.
- **Printed parts**: cracks at screw bosses and bearing seats, especially on the elbow and the upper arm, and
  any warping of the forearm from heat.
- **Cables and tubes**: chafing where the arm's cables pass through the joints, and where the gripper's cable
  and tubes cross joints 5 and 6 from the forearm; the gripper cable's connector tight.
- **The fan**: turning when the robot is on, and the intake free of dust. A stopped fan overheats the drivers.
- **The base**: the mounting bolts tight, the E-stop button firm in its housing.

Then switch on, home, and watch the homing: each joint should back off and re-approach its switch cleanly, and
the pose at the end should match the witness marks ([Checking the homing](https://docs.source-robotics.com/PAROL-docs/1/07-maintenance/homing-check/)).

## Cleaning

Clean the robot switched off and unplugged. Wipe the printed parts with a dry or slightly damp cloth; use no
solvents on them, and never spray anything into the base, where the control board and the fan are open to it.
Clear dust from the fan intake with a soft brush or a vacuum cleaner, not with compressed air, which drives the
dust into the board.
