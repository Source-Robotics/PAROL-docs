# Quick start

From the PAROL6 you have just built to one that is homed and moves on command, on one page. It assumes the robot
is assembled and wired as in the [Build guide](build/index.md) ([Mechanical assembly](build/mechanical-assembly.md),
[Electronics and wiring](build/electronics-and-wiring.md)), and nothing more: no firmware uploaded yet, no software
on your PC, and no experience with Python or a terminal. Every step ends with a link to the page that explains it;
follow it when a step is not clear or something fails.

!!! danger "Read first"
    PAROL6 has no brakes: when the power goes, the arm falls. It has pinch points, it moves fast, and it moves by
    itself while homing. Anchor it to the table, keep the E-stop within reach, keep hands out of the arm's path, and
    read the [Safety](02-safety/index.md) chapter: it is five minutes long.

## 1. What you need

| | Where to get it |
|---|---|
| **Your PAROL6**, assembled and wired, with the control board inside the base | the [Build guide](build/index.md); the parts in the [BOM](build/bill-of-materials.md), or as kits from [the shop](https://source-robotics.com/) |
| **A 24 V power supply**, 5 A | the [BOM](build/bill-of-materials.md) names one; any 24 V 5 A supply works |
| **An E-stop**, a normally closed button on the base | the [BOM](build/bill-of-materials.md) names one; any NC switch works |
| **A USB cable**, type B, to the PC | |
| **An ST-Link programmer and the programming adapter**, to upload the firmware once | the [programming adapter](https://source-robotics.com/products/parol6-programming-adapter) in the shop |
| **A PC** with Windows, Linux or macOS | see the [minimum PC](01-overview/what-you-need.md#the-pc) |

Read in more detail: [What you need](01-overview/what-you-need.md).

## 2. Anchor the robot

Bolt the base to the table through its six holes, or clamp it to the edge. A free-standing PAROL6 tips over when
it extends.

!!! success "Check"
    Push the top of the base sideways, firmly: it must not lift or slide.

Read in more detail: [Mounting the robot](04-installation/mounting.md).

## 3. Install Python and open a terminal

The PC software is written in Python. A **terminal** is the window where you type commands: type one line, press
Enter, wait until it finishes.

=== "Windows"
    1. Download **Python 3.11** from [python.org](https://www.python.org/downloads/windows/): the "Windows
       installer (64-bit)" of the newest 3.11 release.
    2. Run it. On its first screen tick **Add python.exe to PATH**, then press **Install Now**.
    3. Open a terminal: press the Windows key, type `cmd` and press Enter. A black window opens.
    4. Type `python --version` and press Enter.

=== "Linux"
    1. Open a terminal: Ctrl+Alt+T on Ubuntu, or Terminal in the applications menu.
    2. Install Python's tools: `sudo apt install python3-pip python3-venv python3-tk python3-pil python3-pil.imagetk`
       (it asks for your password).
    3. Type `python3 --version` and press Enter. The commander software needs 3.10 or 3.11, the Python API 3.11
       or newer. In the commands below, type `python3` where they say `python`.

=== "macOS"
    1. Download **Python 3.11** from [python.org](https://www.python.org/downloads/macos/): the "macOS 64-bit
       universal2 installer" of the newest 3.11 release, and run it.
    2. Open a terminal: press Cmd+Space, type `Terminal` and press Enter.
    3. Type `python3 --version` and press Enter. In the commands below, type `python3` where they say `python`.

!!! success "Check"
    The terminal answers `Python 3.11` and a number. If it says the command is not found, install Python again and
    (on Windows) tick **Add python.exe to PATH**; then open a new terminal.

## 4. Upload the main firmware

A control board from the shop comes with the **test firmware**, which turns all six motors as soon as the board
starts. Put the **main firmware** on it before you switch on the assembled robot. You do this once.

1. Download the [robot repository](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm): the green
   **Code** button, then **Download ZIP**. Unzip it, for example into your Documents folder.
2. Install [VS Code](https://code.visualstudio.com/). Open it, click the **Extensions** icon on the left, search
   for **PlatformIO IDE** and install it. Restart VS Code when it asks.
3. On Windows, install the ST-Link driver: unzip `en.stsw-link009.zip` from the robot repository and run
   `dpinst_amd64.exe` in it.
4. **Unplug the 24 V supply** from the robot. Plug the programming adapter onto the 2×5 header next to the USB
   port, and the ST-Link into the PC. The adapter powers the board's microcontroller, not the motors.
5. In VS Code: **File**, **Open Folder**, and choose `PAROL6 control board main software` inside the robot
   repository. The first time, PlatformIO downloads its tools for a few minutes: wait until the bar at the bottom
   is quiet.
6. Click the **→** arrow (Upload) in the bar at the bottom of VS Code.
7. When it has finished, unplug the programming adapter.

!!! success "Check"
    The terminal at the bottom of VS Code ends with `SUCCESS`. If not, see the [Firmware](board/08-firmware.md)
    page and [Control board troubleshooting](board/11-troubleshooting.md).

Read in more detail: [Firmware](board/08-firmware.md) · [Firmware and first run](build/firmware-and-first-run.md).

## 5. Install the robot software

Choose one, or install both: the **commander software** is a window with buttons, a program editor and a 3D
simulator; the **Python API** drives the robot from Python programs you write.

=== "Commander software"
    1. Download the [commander software](https://github.com/Source-Robotics/PAROL-commander-software): **Code**,
       then **Download ZIP**, and unzip it into Documents.
    2. In the terminal, go into its folder and install what it needs (a few minutes):
       ```
       cd Documents\PAROL-commander-software-main
       python -m pip install -r requirements.txt
       ```
       On Linux and macOS the folder is written `Documents/PAROL-commander-software-main`.

=== "Python API"
    1. Open the [Python API at version <!-- version: software.python_api -->](<!-- version-url: software.python_api -->)
       and download it: **Code**, then **Download ZIP**. Unzip it into Documents.
    2. In the terminal, go into its folder and install it (a few minutes):
       ```
       cd Documents\PAROL6-python-API-<!-- version: software.python_api -->
       python -m pip install .
       ```
       On Linux and macOS the folder is written with `/`, and a virtual environment is needed first:
       [Python API installation](programming/02-python-api/installation.md#install) has the commands.

!!! success "Check"
    The install ends without a red `ERROR` line. If one appears, see [Commander installation](gui/commander/installation.md)
    or [Python API installation](programming/02-python-api/installation.md).

## 6. Connect

1. The E-stop to the two E-stop terminals on the base. Without it the robot will not run.
2. The USB cable to the PC.
3. The 24 V supply to the power connector. Nothing happens yet: the board is off until the button is pressed.

Read in more detail: [Connecting](04-installation/connecting.md).

## 7. Switch on

Hold the arm by the forearm and press the power button on the base. The motors energise, you hear six clicks,
and the arm holds its position. Let go.

Read in more detail: [First power-on](04-installation/first-power-on.md) · [Switching on and off](05-operation/switching-on-off.md).

!!! success "Check"
    Six drivers initialise and the arm supports itself before you let go. If it does not, use
    [First power-on: if nothing happens](04-installation/first-power-on.md#if-nothing-happens).

## 8. Start the software

First find the robot's **serial port**, the name the PC gives the USB connection:

- **Windows**: open Device Manager (right-click the Start button), then **Ports (COM & LPT)**: the robot is a "USB
  Serial Device" with a number, for example `COM5`.
- **Linux**: `ls /dev/ttyACM*` in the terminal, usually `/dev/ttyACM0`. If the software later reports
  "permission denied", run `sudo usermod -aG dialout $USER`, then log out and in again.
- **macOS**: `ls /dev/cu.usbmodem*` in the terminal.

=== "Commander software"
    For the first run, write the port into the program. Open `GUI/files/Serial_sender_good_latest.py` in a text
    editor (VS Code: **File**, **Open File**) and find these lines near the top:
    ```python
    if my_os == "Windows": 
        STARTING_PORT = 8 # COM3
    else:   
        STARTING_PORT = 0
    ```
    On Windows, replace `8` with the number of your port, `5` for `COM5`. On Linux, `0` is `/dev/ttyACM0`; change
    it if yours has another number. Save the file. Then start the program in the terminal:
    ```
    cd Documents\PAROL-commander-software-main\GUI\files
    python Serial_sender_good_latest.py
    ```
    (Linux and macOS: `cd Documents/PAROL-commander-software-main/GUI/files`, then `python3`.)
    Two windows open: the commander and the simulator. At the bottom of the commander, check the serial port
    (`COM5` on Windows, `ttyACM0` on Linux) and press **Connect**, more than once if the first try fails.

=== "Python API"
    1. Start the **controller**, the program that talks to the robot, with your port, and leave its terminal open:
       ```
       parol6-server --serial COM5
       ```
       (Linux: `--serial /dev/ttyACM0`; macOS: `--serial` and the `/dev/cu.usbmodem…` name.)
    2. Open a **second** terminal, type `python` and press Enter. The prompt changes to `>>>`: Python now runs each
       line you type. Type these three lines:
       ```python
       from parol6 import RobotClient
       rbt = RobotClient()
       rbt.ping()
       ```
    Keep this second terminal open: the next steps type into it.

Read in more detail: [The commander software](gui/commander/index.md) · [The Python API](programming/02-python-api/index.md).

!!! success "Check"
    The commander's response log shows the robot's data, or `ping()` answers with `hardware_connected=1`. If it
    does not, use [Communication troubleshooting](08-troubleshooting/communication.md).

## 9. Jog each joint

Before homing, check that every joint turns the way the software thinks it does: each one briefly, a few degrees,
in its positive direction. The figure shows each joint's positive direction, in colour, over the pose in grey.

![Each joint turned 30 degrees in its positive direction, in colour, over the pose in grey](assets/kinematics/parol6_joint_directions.webp#only-light){ width="900" }
![Each joint turned 30 degrees in its positive direction, in colour, over the pose in grey](assets/kinematics/parol6_joint_directions_dark.webp#only-dark){ width="900" }

=== "Commander software"
    In the **Joint jog** menu, press each joint's left arrow briefly.

=== "Python API"
    ```python
    rbt.jog_j(0, speed=0.2, duration=0.5)     # joint 1, positive, half a second
    ```
    The first number is the joint: `0` is joint 1, `5` is joint 6.

A joint that turns the wrong way is fixed in the firmware, not by trial:
[Firmware and first run](build/firmware-and-first-run.md#a-joint-turns-the-wrong-way).

Read in more detail: [Jogging](05-operation/jogging.md) · [Joint limits and directions](03-technical-data/joint-limits.md).

!!! success "Check"
    Every joint turned the way the figure shows. If one did not, fix it before you home:
    [A joint turns the wrong way](build/firmware-and-first-run.md#a-joint-turns-the-wrong-way).

## 10. Home

Homing finds each joint's reference at its limit switch or sensor. Joints 1, 2 and 3 move to their switches
together, then 4, then 6, then 5, and the arm ends in the after-homing pose: the standby pose turned 90° about
joint 1. Stay at the E-stop: a joint that grinds at its end stop has a switch that does not trigger.

=== "Commander software"
    Press **Home**.

=== "Python API"
    ```python
    rbt.home(wait=True)
    ```

Read in more detail: [Homing](05-operation/homing.md) · [Homing failures](08-troubleshooting/homing-failures.md).

!!! success "Check"
    Homing finishes, the physical arm matches the simulator, and the witness marks agree. If a joint
    keeps travelling or the pose is wrong, stop and use [Homing failures](08-troubleshooting/homing-failures.md).

## 11. Move it

The robot now knows where it is. Three simple moves: bend the arm a little, turn the base, and come back.

=== "Commander software"
    Paste this program into the program window and press **Start**; **Stop** halts it.
    ```
    Begin()
    MoveJoint(90,-70,160,0,30,180,t=3)
    Delay(1)
    MoveJoint(60,-70,160,0,30,180,t=3)
    Delay(1)
    MoveJoint(90,-90,180,0,0,180,t=3)
    End()
    ```
    `MoveJoint` takes the six joint angles in degrees; `t=3` makes the move take three seconds. Jogging in the
    Cartesian jog menu moves the tool in straight lines instead.

=== "Python API"
    Type these lines at the `>>>` prompt, one at a time; each waits until its move is done:
    ```python
    rbt.move_j([90, -70, 160, 0, 30, 180], speed=0.3)   # bend the arm: six joint angles in degrees
    rbt.move_j([60, -70, 160, 0, 30, 180], speed=0.3)   # turn the base
    rbt.move_j([90, -90, 180, 0, 0, 180], speed=0.3)    # back to the after-homing pose
    rbt.move_l([0, 263, 242, 90, 0, 90], speed=0.3)     # a straight line to a tool pose: x, y, z in mm, then rotations
    ```
    `speed` is a fraction of the maximum: 0.3 is gentle. Type `exit()` to leave Python.

Read in more detail: [RBTscript](programming/03-commander/rbtscript.md) · [The Python API](programming/02-python-api/index.md).

## 12. Switch off

Hold the forearm, then press the power button. The arm goes limp the moment the motors lose power.

## 13. Where to go next

| You want to | Read |
|---|---|
| attach a gripper | [End effectors](end-effectors/index.md) |
| write programs | [Programming](programming/index.md), [RBTscript](programming/03-commander/rbtscript.md), [The Python API](programming/02-python-api/index.md) |
| use inputs, outputs, pneumatics | [Peripherals](06-peripherals/index.md) |
| understand what the robot does and does not protect against | [Safety functions](02-safety/safety-functions.md) |
| fix something | [Troubleshooting](08-troubleshooting/index.md) |
| look up a command | [API reference](reference/index.md) |
