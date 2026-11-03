# The GUI

Two windows: the **commander**, where everything is done, and the **simulator**, a 3D view of the robot that
follows it once the robot is connected and homed.

![The commander window, with the joint jog menu](https://docs.source-robotics.com/PAROL-docs/1/assets/GUI2.webp){ width="800" }

![The simulator window](https://docs.source-robotics.com/PAROL-docs/1/assets/sim.webp){ width="400" }

## Connecting

![The connection bar](https://docs.source-robotics.com/PAROL-docs/1/assets/connect.PNG){ width="800" }

At the bottom: the serial port field and **Connect**. `COMx` on Windows, `ttyACMx` on Linux. The response log
starts showing the robot's data when the connection is up; press Connect again if it does not. The **Simulator**
and **Real robot** buttons have no function at present. **Clear error** resets the homing state; unlike
**Enable** it does not re-enable a disabled robot.

## The Move menu

The left part of the window is the jog menu, with two variants:

**Joint jog**: six pairs of arrows, left for the positive direction and right for the negative. The speed slider
below sets the jog speed as a percentage; it affects jogging only, not programs. Works before homing.

**Cartesian jog**: X, Y, Z and the rotations, in the **WRF** (the base) or the **TRF** (the tool), chosen with the
switch; **TRF** is the default. The rotation buttons only work in the TRF: in the WRF they do nothing. Home the
robot first (the software does not check), and the jog stops at a singularity ([Configurations and singularities](https://docs.source-robotics.com/PAROL-docs/1/theory/configurations-and-singularities/)).

![The Cartesian jog menu](https://docs.source-robotics.com/PAROL-docs/1/assets/GUI1.webp){ width="800" }

## The robot position

![Joint angles, the tool pose and the speed slider](https://docs.source-robotics.com/PAROL-docs/1/assets/robot_pos.PNG){ width="800" }

The six joint angles and the tool pose in the WRF, live. **Home** starts the homing sequence; **Enable** clears
errors and enables the robot; **Disable** disables it, the motors still holding. **Park** does not move the
robot: it inserts a three-line program at the cursor of the program window, `Begin()`, a `MoveJoint` to the park
pose with `t=4`, and `End()`, which you then run with **Start**.

## The program window

![The program editor](https://docs.source-robotics.com/PAROL-docs/1/assets/program_window.PNG){ width="800" }

An RBTscript program, one command per line ([RBTscript](https://docs.source-robotics.com/PAROL-docs/1/programming/03-commander/rbtscript/)). **Start** runs it from `Begin()`,
**Stop** halts it. **Start** first saves the editor's text: into the file you opened, if any, overwriting it,
and into `Programs/execute_script.txt`.

![Start and stop](https://docs.source-robotics.com/PAROL-docs/1/assets/start_stop.PNG){ width="350" }

The command list inserts a command at the cursor: with *Current* selected, a motion command is inserted with the
robot's current joint angles or pose as its arguments, which is how you teach a pose; with *Custom* the
arguments are left for you.

![The command list](https://docs.source-robotics.com/PAROL-docs/1/assets/Commands.PNG){ width="250" }

## The response log

![The response log](https://docs.source-robotics.com/PAROL-docs/1/assets/response_log.PNG){ width="800" }

What the robot and the program are doing, and why a command was refused: the first place to look when something
does not happen ([Errors and recovery](https://docs.source-robotics.com/PAROL-docs/1/05-operation/errors-and-recovery/)).

## The IO tab

![The IO tab](https://docs.source-robotics.com/PAROL-docs/1/assets/IO_tab.PNG){ width="650" }

The state of the two inputs, and buttons for the two outputs.

## The Gripper tab

![The gripper tab](https://docs.source-robotics.com/PAROL-docs/1/assets/parol_grip_gui.PNG){ width="650" }

For the SSG-48 and MSG grippers. After homing: **Clear gripper error**, then **Calibrate gripper**, then wait until
the tab shows `Calibration status is: 1` (about 3 s for the SSG-48, 5 to 6 s for the MSG on its longer rails).
Then set the position, speed and current with the sliders and press **Move GoTo**. The feedback section shows the
gripper's position and current, its calibrated and E-stop error bits, and its whole status byte as a number
(labelled *Gripper object detection is*). **Change gripper ID** sets the CAN ID the board addresses, 0 as the
grippers ship.

## The Calibrate and Plot buttons

The menu also has **Calibrate** and **Plot**. Both open the same panel, with **Disable motor**, **Enable motor**,
**Go to limit** and a joint menu; none of them does anything in the current version.

## The Settings tab

![The settings tab](https://docs.source-robotics.com/PAROL-docs/1/assets/Settings_tab.PNG){ width="650" }

Dark or light mode, and the scaling of the GUI for your display.

## The terminal

The terminal the program was started from prints a block of data every few seconds: the positions and speeds
from the robot, the homed, I/O and error bytes, the timing, the gripper data, the commanded data and the GUI's
state. `Time between 2 commands in ms` is the one to watch: near 0.010 is right. The value is in seconds, whatever
the label says: 0.010 is the 10 ms cycle.
