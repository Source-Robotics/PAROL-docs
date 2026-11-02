# Installation

## Requirements

- Python 3.10 or 3.11 (tested on 3.10.12 and 3.11.0; newer versions break some pinned dependencies).
- Windows or Linux. The current version does not run on macOS: it opens the serial port only on Windows
  (`COMn`) and Linux (`/dev/ttyACMn`), whatever the repository's README says.
- A PC that keeps the 100 Hz loop: [What you need](../../01-overview/what-you-need.md#the-pc).

## Install

=== "Windows"
    ```
    git clone https://github.com/Source-Robotics/PAROL-commander-software.git
    cd PAROL-commander-software
    pip install -r requirements.txt
    ```
    With Python 3.10 or 3.11 (`py -3.11 -m pip ...` picks it when several are installed). The robot's serial
    port is `COM` and a number: Device Manager lists it under **Ports (COM & LPT)**.

=== "Linux"
    ```
    sudo apt-get install python3-tk python3-pil python3-pil.imagetk
    git clone https://github.com/Source-Robotics/PAROL-commander-software.git
    cd PAROL-commander-software
    pip install -r requirements.txt
    sudo usermod -aG dialout $USER     # access to the serial port; log out and in again once
    ```
    The robot's serial port is `ttyACM0` (`ls /dev/ttyACM*` lists it).

=== "macOS"
    The current version does not run on macOS (known issue
    [KI-8](../../08-troubleshooting/known-issues.md)). Use a Windows or Linux PC, or the
    [Python API](../../programming/02-python-api/installation.md), which runs on macOS.

The repository's [Windows](https://github.com/Source-Robotics/PAROL-commander-software/blob/main/Windows_install.md)
and [Linux](https://github.com/Source-Robotics/PAROL-commander-software/blob/main/Linux_install.md) guides list the
packages one by one if `requirements.txt` fails: the robotics toolbox, swift, numpy and scipy are pinned to the
versions that work together, and the `Working dependency` folder has the full module lists of PCs on which the
software runs.

## Run

```
cd GUI/files
python Serial_sender_good_latest.py
```

Two windows open: the commander and the simulator. Enter the serial port at the bottom of the commander (`COM5`,
or `ttyACM0` on Linux) and press **Connect**, more than once if needed. On Linux, a permission error on the port
is fixed with `sudo chmod 666 /dev/ttyACM0`, or by joining the `dialout` group.

## Check the loop

The terminal the program runs in prints the robot's data; `Time between 2 commands in ms` should sit near
0.010 while you jog. If it is often much higher, the PC is too slow for the loop, and the robot will stutter
([Communication](../../08-troubleshooting/communication.md)).

!!! check "Check"
    The commander shows the robot's data after **Connect**, and the simulator moves with the robot when you
    jog. If not: [Communication](../../08-troubleshooting/communication.md).
