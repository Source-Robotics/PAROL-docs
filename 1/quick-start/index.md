# Quick start

From the PAROL6 you have just built to one that is homed and moves on command, on one page. It assumes the robot
is assembled and wired as in the [Build guide](https://docs.source-robotics.com/PAROL-docs/1/build/) ([Mechanical assembly](https://docs.source-robotics.com/PAROL-docs/1/build/mechanical-assembly/),
[Electronics and wiring](https://docs.source-robotics.com/PAROL-docs/1/build/electronics-and-wiring/)), and nothing more: no firmware uploaded yet, no software
on your PC, and no experience with Python or a terminal. Every step ends with a link to the page that explains it;
follow it when a step is not clear or something fails.

!!! danger "Read first"
    PAROL6 has no brakes: when the power goes, the arm falls. It has pinch points, it moves fast, and it moves by
    itself while homing. Anchor it to the table, keep the E-stop within reach, keep hands out of the arm's path, and
    read the [Safety](https://docs.source-robotics.com/PAROL-docs/1/02-safety/) chapter: it is five minutes long.

## 1. What you need

| | Where to get it |
|---|---|
| **Your PAROL6**, assembled and wired, with the control board inside the base | the [Build guide](https://docs.source-robotics.com/PAROL-docs/1/build/); the parts in the [BOM](https://docs.source-robotics.com/PAROL-docs/1/build/bill-of-materials/), or as kits from [the shop](https://source-robotics.com/) |
| **A 24 V power supply**, 5 A | the [BOM](https://docs.source-robotics.com/PAROL-docs/1/build/bill-of-materials/) names one; any 24 V 5 A supply works |
| **A mains switch within reach**, on the supply's mains side: a switched socket strip will do | it is the stop that still works when the PC software has frozen ([Emergency stop](https://docs.source-robotics.com/PAROL-docs/1/02-safety/emergency-stop/)) |
| **An E-stop**, a normally closed button on the base | the [BOM](https://docs.source-robotics.com/PAROL-docs/1/build/bill-of-materials/) names one; any NC switch works |
| **A USB cable**, type B, to the PC | |
| **An ST-Link programmer and the programming adapter**, to upload the firmware once | the [programming adapter](https://source-robotics.com/products/parol6-programming-adapter) in the shop |
| **A PC** with Windows, Linux or macOS | see the [minimum PC](https://docs.source-robotics.com/PAROL-docs/1/01-overview/what-you-need/#the-pc) |

Read in more detail: [What you need](https://docs.source-robotics.com/PAROL-docs/1/01-overview/what-you-need/).

## 2. Anchor the robot

Bolt the base to the table through its six holes, or clamp it to the edge. A free-standing PAROL6 tips over when
it extends.

!!! success "Check"
    Push the top of the base sideways, firmly: it must not lift or slide.

Read in more detail: [Mounting the robot](https://docs.source-robotics.com/PAROL-docs/1/04-installation/mounting/).

## 3. Install Python and Git, and open a terminal

The PC software is written in Python, and Git downloads it. A **terminal** is the window where you type commands:
type one line, press Enter, wait until it finishes.

=== "Windows"
    1. Download **Python 3.11.9** from [python.org](https://www.python.org/downloads/release/python-3119/): the
       "Windows installer (64-bit)". 3.11.9 is the last 3.11 release with an installer.
    2. Run it. On its first screen tick **Add python.exe to PATH**, then press **Install Now**.
    3. Download **Git** from [git-scm.com](https://git-scm.com/downloads/win) and install it with the settings it
       proposes.
    4. Open a terminal: press the Windows key, type `cmd` and press Enter. A black window opens.
    5. Type `python --version` and press Enter, then `git --version`.

    The commands on this page start with `cd %USERPROFILE%\Documents`, which takes the terminal to your Documents
    folder. If Windows answers that it cannot find the path, your Documents folder is kept in OneDrive: type
    `cd %USERPROFILE%\OneDrive\Documents` instead. To open a terminal in any folder, open the folder in File
    Explorer, click the address bar, type `cmd` and press Enter.

=== "Linux"
    1. Open a terminal: Ctrl+Alt+T on Ubuntu, or Terminal in the applications menu.
    2. Install Git: `sudo apt install git` (it asks for your password).
    3. The software needs **Python 3.11**: the commander runs on 3.10 or 3.11 only, the Python API on 3.11 or
       newer. Ubuntu's own Python is 3.10 on Ubuntu 22.04 and 3.12 on Ubuntu 24.04, so install 3.11 next to it,
       with its virtual environments and its window toolkit:
       ```
       sudo add-apt-repository ppa:deadsnakes/ppa
       sudo apt install python3.11 python3.11-venv python3.11-tk
       ```
    4. Type `python3.11 --version` and press Enter, then `git --version`. Each program below gets its own
       virtual environment made with Python 3.11; inside it, `python` is that Python 3.11.

=== "macOS"
    1. Download **Python 3.11.9** from [python.org](https://www.python.org/downloads/release/python-3119/): the
       "macOS 64-bit universal2 installer". Run it.
    2. Open a terminal: press Cmd+Space, type `Terminal` and press Enter.
    3. Install Git with the Xcode command line tools: type `xcode-select --install`, press Enter and confirm the
       window that opens.
    4. Type `python3.11 --version` and press Enter, then `git --version`. Each program below gets its own
       virtual environment made with Python 3.11; inside it, `python` is that Python 3.11.

!!! success "Check"
    The terminal answers `Python 3.11` and a number, and `git version` and a number. If it says a command is not
    found, install that program again (on Windows, tick **Add python.exe to PATH**), then open a new terminal.

## 4. Upload the main firmware

A control board from the shop comes with the **test firmware**, which turns all six motors as soon as the board
starts. Put the **main firmware** on it before you switch on the assembled robot. You do this once.

1. Download the [robot repository](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm) into your
   Documents folder:
   ```
   cd %USERPROFILE%\Documents
   git clone https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm.git
   ```
   On Linux and macOS, the first line is `cd ~/Documents`.
2. Install [VS Code](https://code.visualstudio.com/). Open it, click the **Extensions** icon on the left, search
   for **PlatformIO IDE** and install it. Restart VS Code when it asks.
3. On Windows, install the ST-Link driver: in File Explorer, open `PAROL6-Desktop-robot-arm` in your Documents
   folder, right-click `en.stsw-link009.zip`, choose **Extract All**, and run `dpinst_amd64.exe` from the
   extracted folder.
4. **Unplug the 24 V supply** from the robot. Plug the programming adapter onto the 2×5 header next to the USB
   port, and the ST-Link into the PC. The adapter powers the board's microcontroller, not the motors.
5. In VS Code: **File**, **Open Folder**, and choose `PAROL6 control board main software` inside
   `PAROL6-Desktop-robot-arm`. The first time, PlatformIO downloads its tools for a few minutes: wait until the bar
   at the bottom is quiet.
6. Click the **→** arrow (Upload) in the bar at the bottom of VS Code.
7. When it has finished, unplug the programming adapter.

!!! success "Check"
    The terminal at the bottom of VS Code ends with `SUCCESS`. If not, see the [Firmware](https://docs.source-robotics.com/PAROL-docs/1/board/08-firmware/)
    page and [Control board troubleshooting](https://docs.source-robotics.com/PAROL-docs/1/board/11-troubleshooting/).

Read in more detail: [Firmware](https://docs.source-robotics.com/PAROL-docs/1/board/08-firmware/) · [Firmware and first run](https://docs.source-robotics.com/PAROL-docs/1/build/firmware-and-first-run/).

## 5. Install the robot software

Choose one, or install both: the **commander software** is a window with buttons, a program editor and a 3D
simulator; the **Python API** drives the robot from Python programs you write. Each one goes into its own folder
with its own **virtual environment** (`.venv`), a private copy of Python for that program: the two need different
versions of the same packages, so they cannot share one.

=== "Commander software"
    In the terminal, download the [commander software](https://github.com/Source-Robotics/PAROL-commander-software),
    make its virtual environment and install what it needs (a few minutes):

    ```
    cd %USERPROFILE%\Documents
    git clone https://github.com/Source-Robotics/PAROL-commander-software.git
    cd PAROL-commander-software
    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install -r requirements.txt
    ```

    On Linux and macOS:

    ```
    cd ~/Documents
    git clone https://github.com/Source-Robotics/PAROL-commander-software.git
    cd PAROL-commander-software
    python3.11 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    ```

    After the activate line the prompt starts with `(.venv)`.

=== "Python API"
    In the terminal, download the [Python API](https://github.com/PCrnjak/PAROL6-python-API), switch to version
    0.9.1, make its virtual environment and install it (a few minutes):

    ```
    cd %USERPROFILE%\Documents
    git clone https://github.com/PCrnjak/PAROL6-python-API.git
    cd PAROL6-python-API
    git checkout v0.9.1
    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install .
    ```

    On Linux and macOS:

    ```
    cd ~/Documents
    git clone https://github.com/PCrnjak/PAROL6-python-API.git
    cd PAROL6-python-API
    git checkout v0.9.1
    python3.11 -m venv .venv
    source .venv/bin/activate
    python -m pip install .
    ```

    After the activate line the prompt starts with `(.venv)`. Git reports a "detached HEAD" after the checkout:
    that is expected.

!!! success "Check"
    The install ends without an `ERROR` line. If one appears, see [Commander installation](https://docs.source-robotics.com/PAROL-docs/1/gui/commander/installation/)
    or [Python API installation](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/installation/).

## 6. Connect

1. The E-stop to the two E-stop terminals on the base. Without it the robot will not run.
2. The USB cable to the PC.
3. The 24 V supply to the power connector, and the supply's mains plug into the switched socket strip, or behind
   the mains switch, within your reach. Nothing happens yet: the board is off until the button is pressed.

Read in more detail: [Connecting](https://docs.source-robotics.com/PAROL-docs/1/04-installation/connecting/).

## 7. Switch on

Hold the arm by the forearm and press the power button on the base. The motors energise, you hear six clicks,
and the arm holds its position. Let go.

!!! success "Check"
    Six drivers initialise and the arm supports itself before you let go. If it does not, use
    [First power-on: if nothing happens](https://docs.source-robotics.com/PAROL-docs/1/04-installation/first-power-on/#if-nothing-happens).

Read in more detail: [First power-on](https://docs.source-robotics.com/PAROL-docs/1/04-installation/first-power-on/) · [Switching on and off](https://docs.source-robotics.com/PAROL-docs/1/05-operation/switching-on-off/).

## 8. Start the software

First find the robot's **serial port**, the name the PC gives the USB connection:

- **Windows**: open Device Manager (right-click the Start button), then **Ports (COM & LPT)**: the robot is a "USB
  Serial Device" with a number, for example `COM5`.
- **Linux**: `ls /dev/ttyACM*` in the terminal, usually `/dev/ttyACM0`. If the software later reports
  "permission denied", run `sudo usermod -aG dialout $USER`, then log out and in again.
- **macOS**: `ls /dev/cu.usbmodem*` in the terminal.

=== "Commander software"
    For the first run, write the port into the program. Open
    `PAROL-commander-software/GUI/files/Serial_sender_good_latest.py` in a text editor (VS Code: **File**,
    **Open File**) and find these lines near the top:
    ```python
    if my_os == "Windows": 
        STARTING_PORT = 8 # COM3
    else:   
        STARTING_PORT = 0
    ```
    On Windows, replace `8` with the number of your port, `5` for `COM5`. On Linux, `0` is `/dev/ttyACM0`; change
    it if yours has another number. Save the file. Then start the program in the terminal:
    ```
    cd %USERPROFILE%\Documents\PAROL-commander-software
    .venv\Scripts\activate
    cd GUI\files
    python Serial_sender_good_latest.py
    ```
    On Linux and macOS:
    ```
    cd ~/Documents/PAROL-commander-software
    source .venv/bin/activate
    cd GUI/files
    python Serial_sender_good_latest.py
    ```
    Two windows open: the commander and the simulator. At the bottom of the commander, type the serial port in
    the port field (`COM5` on Windows, `ttyACM0` on Linux) and press **Connect**, more than once if the first try
    fails.

=== "Python API"
    1. Start the **controller**, the program that talks to the robot, with your port, and leave its terminal open:
       ```
       cd %USERPROFILE%\Documents\PAROL6-python-API
       .venv\Scripts\activate
       parol6-server --serial COM5
       ```
       On Linux and macOS: `cd ~/Documents/PAROL6-python-API`, then `source .venv/bin/activate`, then
       `parol6-server --serial /dev/ttyACM0` (macOS: the `/dev/cu.usbmodem…` name).
    2. Open a **second** terminal and activate the same virtual environment in it:
       ```
       cd %USERPROFILE%\Documents\PAROL6-python-API
       .venv\Scripts\activate
       python
       ```
       (Linux and macOS: `cd ~/Documents/PAROL6-python-API`, `source .venv/bin/activate`, `python`.) The prompt
       changes to `>>>`: Python now runs each line you type. Type these three lines:
       ```python
       from parol6 import RobotClient
       rbt = RobotClient()
       rbt.ping()
       ```
    Keep this second terminal open: the next steps type into it.

Read in more detail: [The commander software](https://docs.source-robotics.com/PAROL-docs/1/gui/commander/) · [The Python API](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/).

!!! success "Check"
    The commander's response log shows the robot's data, or `ping()` answers with `hardware_connected=True`. If
    it does not, use [Communication troubleshooting](https://docs.source-robotics.com/PAROL-docs/1/08-troubleshooting/communication/).

## 9. Jog each joint

Before homing, check that every joint turns the way the software thinks it does: each one briefly, a few degrees.
The figure shows each joint's positive direction, in colour, over the pose in grey.

![Each joint turned 30 degrees in its positive direction, in colour, over the pose in grey](https://docs.source-robotics.com/PAROL-docs/1/assets/kinematics/parol6_joint_directions.webp){ width="900" }
![Each joint turned 30 degrees in its positive direction, in colour, over the pose in grey](https://docs.source-robotics.com/PAROL-docs/1/assets/kinematics/parol6_joint_directions_dark.webp){ width="900" }

Before homing, both programs check each jog against the joint limits with a position count that starts at 0
when the board is switched on. That count puts joint 2 past its positive limit and joints 3 and 6 at or below
their negative limits. So, until the robot is homed:

- **Joint 2** jogs only in its **negative** direction. Check that it turns opposite to the figure.
- **Joints 3 and 6** jog only in their positive direction, which is the one to check.
- **Joints 1, 4 and 5** jog both ways.

A refused jog does not move: the commander logs `Error: Robot jog -> Position out of range`, the Python API
stops the joint before it starts.

=== "Commander software"
    In the **Joint jog** menu, press the left arrow (positive) of joints 1 and 3 to 6 briefly, and the right arrow
    (negative) of joint 2.

=== "Python API"
    ```python
    rbt.jog_j(0, speed=0.2, duration=0.5)     # joint 1, positive, half a second
    rbt.jog_j(1, speed=-0.2, duration=0.5)    # joint 2, negative
    ```
    The first number is the joint: `0` is joint 1, `5` is joint 6. A negative `speed` jogs the negative way.

A joint that turns the wrong way is fixed in the firmware, not by trial:
[Firmware and first run](https://docs.source-robotics.com/PAROL-docs/1/build/firmware-and-first-run/#a-joint-turns-the-wrong-way).

Read in more detail: [Jogging](https://docs.source-robotics.com/PAROL-docs/1/05-operation/jogging/) · [Joint limits and directions](https://docs.source-robotics.com/PAROL-docs/1/03-technical-data/joint-limits/).

!!! success "Check"
    Joints 1 and 3 to 6 turned the way the figure shows, and joint 2 turned the opposite way on its negative jog.
    If one did not, fix it before you home:
    [A joint turns the wrong way](https://docs.source-robotics.com/PAROL-docs/1/build/firmware-and-first-run/#a-joint-turns-the-wrong-way).

## 10. Home

Homing finds each joint's reference at its limit switch or sensor. Joints 1, 2 and 3 move to their switches
together, then 4, then 6, then 5, and the arm ends in the after-homing pose: the standby pose turned 90° about
joint 1. Stay at the E-stop: a joint that grinds at its end stop has a switch that does not trigger.

Before you press Home:

- **Joint 6** stands so that it finds its sensor within one turn in the negative direction, with the tool's
  cables and tubes not wound up. The figure shows the pose: the gripper as drawn, the sensor (blue) and the homing
  pin (red); joint 6 turns along the green arrow.
- **The tool** is mounted, and the firmware's joint 5 homing offset matches it. Joint 5 homes against a feature
  of the tool holder; `j5_homing_offset` in `main.cpp` is 8900 for the pneumatic gripper holder (as shipped) and
  8035 for the SSG-48. If you change it, upload the firmware again as in step 4
  ([Joint 5 and the tool](https://docs.source-robotics.com/PAROL-docs/1/05-operation/mastering/#joint-5-and-the-tool)).

![Joint 6 before homing: the sensor, the homing pin and the direction of rotation](https://docs.source-robotics.com/PAROL-docs/1/assets/J6_home.webp){ width="700" }

=== "Commander software"
    Press **Home**.

=== "Python API"
    ```python
    rbt.home(wait=True)
    ```

Read in more detail: [Homing](https://docs.source-robotics.com/PAROL-docs/1/05-operation/homing/) · [Homing failures](https://docs.source-robotics.com/PAROL-docs/1/08-troubleshooting/homing-failures/).

!!! success "Check"
    Homing finishes, the physical arm matches the simulator, and the pin passes through the witness marks of each
    joint, which line up in the after-homing pose ([Witness marks](https://docs.source-robotics.com/PAROL-docs/1/05-operation/mastering/#witness-marks)). If a
    joint keeps travelling or the pose is wrong, stop and use [Homing failures](https://docs.source-robotics.com/PAROL-docs/1/08-troubleshooting/homing-failures/).

## 11. Move it

The robot now knows where it is. Three simple moves: bend the arm a little, turn the base, and come back. The
Python API adds a short straight line down and up from the bent pose.

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
    rbt.move_j([90, -70, 160, 0, 30, 180], speed=0.3)       # bend the arm: six joint angles in degrees
    rbt.move_l([0, 0, -30, 0, 0, 0], rel=True, speed=0.3)   # a straight line 30 mm down
    rbt.move_l([0, 0, 30, 0, 0, 0], rel=True, speed=0.3)    # and 30 mm back up
    rbt.move_j([60, -70, 160, 0, 30, 180], speed=0.3)       # turn the base
    rbt.move_j([90, -90, 180, 0, 0, 180], speed=0.3)        # back to the after-homing pose
    ```
    `speed` is a fraction of the maximum: 0.3 is gentle. With `rel=True`, `move_l` takes a change from where the
    tool is: x, y and z in mm in the world frame, then three rotations in degrees.

Read in more detail: [RBTscript](https://docs.source-robotics.com/PAROL-docs/1/programming/03-commander/rbtscript/) · [The Python API](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/).

## 12. Switch off

Bring the arm to the **parked pose** first, folded in over the base, so that it has the least distance to fall:

=== "Commander software"
    Press **Park**: it writes a three-line program into the program window. Press **Start** to run it.

=== "Python API"
    ```python
    rbt.move_j([90, -144.683, 108.171, 2.222, 25.003, 180], speed=0.3)   # the commander's park pose
    ```
    Type `exit()` to leave Python.

Then hold the forearm and press the power button. The arm goes limp the moment the motors lose power.

## 13. Where to go next

| You want to | Read |
|---|---|
| attach a gripper | [End effectors](https://docs.source-robotics.com/PAROL-docs/1/end-effectors/) |
| write programs | [Programming](https://docs.source-robotics.com/PAROL-docs/1/programming/), [RBTscript](https://docs.source-robotics.com/PAROL-docs/1/programming/03-commander/rbtscript/), [The Python API](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/) |
| use inputs, outputs, pneumatics | [Peripherals](https://docs.source-robotics.com/PAROL-docs/1/06-peripherals/) |
| understand what the robot does and does not protect against | [Safety functions](https://docs.source-robotics.com/PAROL-docs/1/02-safety/safety-functions/) |
| fix something | [Troubleshooting](https://docs.source-robotics.com/PAROL-docs/1/08-troubleshooting/) |
| look up a command | [API reference](https://docs.source-robotics.com/PAROL-docs/1/reference/) |
