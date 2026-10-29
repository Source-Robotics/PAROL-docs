# By symptom

| Symptom | Likely cause | What to do |
|---|---|---|
| Nothing happens at the power button | No 24 V; polarity; the button cable | Check the supply's LED, the GX16 cable, the JST button cable on the board |
| The board turns on by itself when the supply is plugged in | 3.3 V on the programming header (an ST-Link or the adapter is connected); the arm was moved while unpowered | Unplug the adapter; move an unpowered robot slowly |
| The robot cannot be switched off with the button | The same 3.3 V | Unplug the programming adapter |
| Clicks on power-up, but the PC does not connect | Wrong serial port; the test firmware is on the board; Linux permissions | [Communication](communication.md) |
| A joint jogs the wrong way | Direction not set for that joint in the firmware; a motor's wires swapped | [A joint turns the wrong way](../build/firmware-and-first-run.md#a-joint-turns-the-wrong-way) |
| A joint does not move at all | Driver not seated or faulty; motor connector; the joint is at its blocker | The test firmware's `#STEPx` and `#STATUS` ([The test firmware](../board/09-test-firmware.md)) |
| A joint grinds at its end during homing | Its switch or sensor does not trigger | E-stop; [Homing failures](homing-failures.md) |
| Joint 6 keeps spinning during homing | The homing pin is not where the sensor looks | E-stop; set the joint 6 pose as in [Homing](../05-operation/homing.md) |
| The pose after homing is off by a few degrees on one joint | A loose coupler, a slipped belt, a moved switch | [Couplers](../08-maintenance/couplers.md), [Belts](../08-maintenance/belts.md), then [Mastering](../05-operation/mastering.md) |
| The robot's position drifts during a program | Lost steps: too fast, too heavy, a collision, a reduced current | Lower the speed; check the payload; home again |
| A joint hums or squeals and does not hold | A driver in error, a lost phase | `#STATUS` in the test firmware; check the motor cable |
| Cartesian jogging stops by itself | A singularity | Jog a joint away ([Configurations and singularities](../programming/02-concepts/configurations-and-singularities.md)) |
| A pose from the GUI cannot be reached by MoveCart | The inverse kinematics finds no solution along the straight line | Move in joint space; choose another orientation |
| The robot stutters while moving | The PC misses the 10 ms cycle | [Communication](communication.md) |
| The forearm is hot | Hours of motion at the default currents | [Currents and temperatures](../03-technical-data/operating-temperatures.md) |
| The gripper does nothing | Not calibrated; an error latched; the cable | Calibrate, clear the error; the gripper's manual |
| The E-stop has no effect | The PC software is frozen | Switch off the power supply; see [Emergency stop](../02-safety/emergency-stop.md) |
