# Checking the homing

Homing is the robot's only position reference, so check it after any mechanical work, after a collision, and
whenever the robot's accuracy seems off.

1. Home the robot and watch each joint: it must reach its switch, back off, re-approach slowly, and move on. A
   joint that grinds at a stop, or re-approaches at full speed, has a switch problem ([Homing failures](https://docs.source-robotics.com/PAROL-docs/1/08-troubleshooting/homing-failures/)).
2. At the end, try the pin at the witness marks of each joint ([Mastering](https://docs.source-robotics.com/PAROL-docs/1/05-operation/mastering/)). It
   should slide in, or nearly. A joint that is off by more than a degree was knocked, slipped, or its switch
   moved.
3. Home three times in a row and compare the witness marks each time. The pose should repeat exactly: if it
   does not, the switch or the sensor triggers inconsistently, or something in the joint moves.
4. Jog to a taught pose from a program and check that the tool is where it was taught.

A joint that homes repeatably but to the wrong place is mastered; a joint that does not repeat is repaired.
