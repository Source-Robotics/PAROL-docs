# Glossary

**After-homing pose**
:   Where homing leaves the robot: the standby pose turned 90° about joint 1, joints at 90°, −90°, 180°, 0°, 0°,
    180°. The firmware (`standby_position`) and the Python API (`STANDBY_ANGLES_DEG`) call this pose standby. The
    witness marks line up in it.

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

**Flange**
:   The mounting face at the end of joint 6, where the tool is screwed on. With nothing on it, the TCP is the
    flange face.

**Forearm** (lower arm)
:   The link from the elbow (joint 3) to the wrist. It carries joint 4. Forearm and lower arm mean the same link.

**Homing** (referencing)
:   Finding each joint's position after power-up by driving it to its limit switch or sensor, then moving a known
    number of steps to the after-homing pose. Needed after every power-up; the robot does not know where it is
    before.

**Jogging**
:   Moving a joint, or the tool along an axis, at a chosen speed for as long as a button is held or a command
    repeats.

**Joint names**
:   Joints 1 to 6 by number, from the base up. Other names for the same joints: base, shoulder and elbow for 1 to
    3, and wrist 1, wrist 2 and wrist 3 for 4 to 6, as in the robot model and ROS.

**Limit switch, inductive sensor**
:   The references for homing: mechanical switches on joints 2, 3 and 5, inductive sensors on joints 1, 4 and 6.

**Mastering**
:   Fine-tuning the number of steps from a joint's limit switch to its witness mark, so that a homed robot stands
    exactly in the after-homing pose.

**Motion profile**
:   The shape of the speed curve of a move: trapezoidal, polynomial, time-optimal, and so on. The Python API
    offers several; the commander uses trapezoidal and quintic polynomial.

**Parked pose**
:   The arm folded in over the base, joints 2 and 3 toward their limit switches: how the robot rests when it is
    off, and the pose to switch off in, since the arm has the least distance to fall from it. The commander's
    **Park** button writes a program that moves there (90°, −144.683°, 108.171°, 2.222°, 25.003°, 180°).

**Pose**
:   The position and the orientation of the tool together: six numbers, x, y, z in millimetres and three angles in
    degrees. The standby, after-homing and parked poses are poses of the whole arm, given as six joint angles.

**RBTscript**
:   The commander software's program language: one command per line, `MoveJoint`, `MoveCart`, `Delay`, `Gripper`
    and so on.

**Standby pose**
:   The pose of the Denavit-Hartenberg table and the reference of the joint angles: joints at 0°, −90°, 180°, 0°,
    0°, 180°, the upper arm vertical, the forearm horizontal, the arm pointing away from the electronics case at
    the back of the base.
    After homing the robot stands in it turned 90° about joint 1 (joint 1 at 90°): the after-homing pose,
    which the Python API calls its standby.

**Stepper motor**
:   The motors of PAROL6: open-loop motors that move in steps, 200 full steps per turn, 6400 with the 32
    microsteps the control board uses. The position is counted, not measured.

**Test firmware**
:   The firmware every control board from the shop carries when it ships. It reports each driver at power-on and
    answers a few text commands (`#LIMIT`, `#IO`) from a serial terminal, and it turns all six motors slowly from
    the moment it starts until the power is switched off. Replace it with the main firmware before the robot is
    used ([The test firmware](https://docs.source-robotics.com/PAROL-docs/1/board/09-test-firmware/)).

**TCP** (tool center point)
:   The point on the tool the robot positions and the origin of the tool frame. Selecting a tool in the software
    sets it; an offset moves it.

**TRF, WRF**
:   The tool reference frame, fixed to the tool, and the world reference frame, fixed to the base. Cartesian jogs
    and relative moves can be made in either.

**Upper arm**
:   The link from the shoulder (joint 2) to the elbow (joint 3).

**Witness marks**
:   Holes in the printed parts of neighbouring links that line up, so that a pin passes through, when the joint
    stands exactly in the after-homing pose.

**Wrist 1, wrist 2, wrist 3**
:   Other names for joints 4, 5 and 6. See *Joint names*.
