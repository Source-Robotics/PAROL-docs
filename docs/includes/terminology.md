<!-- One shared glossary, included by the Glossary page. Keep entries alphabetical. -->

**Blending** (blend radius)
:   Passing through a waypoint without stopping: the path cuts the corner within the given radius. The Python
    API's `r` parameter.

**Commander software**
:   Source Robotics' desktop program for PAROL6: a GUI with jogging, a simulator, a program editor for RBTscript,
    I/O and gripper control, talking to the control board over USB.

**Control board**
:   The electronics inside the base: an STM32 microcontroller, six TMC5160 stepper drivers, the inputs, outputs,
    E-stop input, CAN and USB. It runs the low-level firmware; the PC runs the high-level software.

**Controller** (Python API)
:   The `parol6-server` process: it talks to the control board over serial at 100 Hz, plans the motion and accepts
    commands over UDP from any number of clients.

**Direction, positive**
:   The direction in which a joint's angle increases, shown in the figure on *Joint limits and directions*. The
    commander's left arrows jog positive.

**E-stop**
:   The normally closed button on the base. Pressing it, unplugging it or cutting its wire opens the circuit, and
    the robot stops. It must be connected for the robot to run.

**Firmware**
:   The program on the control board. The *main* firmware runs the robot with the PC software; the *test* firmware
    checks the board and the wiring from a serial terminal.

**Homing** (referencing)
:   Finding each joint's position after power-up by driving it to its limit switch or sensor, then moving a known
    number of steps to the standby pose. Needed after every power-up; the robot does not know where it is before.

**Jogging**
:   Moving a joint, or the tool along an axis, at a chosen speed for as long as a button is held or a command
    repeats.

**Limit switch, inductive sensor**
:   The references for homing: mechanical switches on joints 2, 3 and 5, inductive sensors on joints 1, 4 and 6.

**Mastering**
:   Fine-tuning the number of steps from a joint's limit switch to its witness mark, so that a homed robot stands
    exactly in the standby pose.

**Motion profile**
:   The shape of the speed curve of a move: trapezoidal, polynomial, time-optimal, and so on. The Python API
    offers several; the commander uses trapezoidal and quintic polynomial.

**Pose**
:   The position and the orientation of the tool together: six numbers, x, y, z in millimetres and three angles in
    degrees.

**RBTscript**
:   The commander software's program language: one command per line, `MoveJoint`, `MoveCart`, `Delay`, `Gripper`
    and so on.

**Standby pose**
:   The pose the robot takes after homing and the zero of its joint angles: joints at 90°, −90°, 180°, 0°, 0°,
    180°. The Denavit-Hartenberg zero of the kinematic model has joint 1 at 0° instead; the firmware homes to +90°.

**Stepper motor**
:   The motors of PAROL6: open-loop motors that move in steps, 200 full steps per turn, 6400 with the 32
    microsteps the control board uses. The position is counted, not measured.

**TCP** (tool center point)
:   The point on the tool the robot positions and the origin of the tool frame. Selecting a tool in the software
    sets it; an offset moves it.

**TRF, WRF**
:   The tool reference frame, fixed to the tool, and the world reference frame, fixed to the base. Cartesian jogs
    and relative moves can be made in either.

**Witness marks**
:   Holes in the printed parts of neighbouring links that line up, so that a pin passes through, when the joint
    stands exactly at its zero.
