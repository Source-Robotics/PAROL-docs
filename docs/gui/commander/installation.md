# Installation

## Requirements

- Python 3.10 or 3.11 (tested on 3.10.12 and 3.11.0; newer versions break some pinned dependencies).
- Windows, Linux or macOS (macOS follows the Linux guide).
- A PC that keeps the 100 Hz loop: [What you need](../../01-overview/what-you-need.md#the-pc).

## Install

```
git clone https://github.com/Source-Robotics/PAROL-commander-software.git
cd PAROL-commander-software
pip install -r requirements.txt
```

On Linux, also:

```
sudo apt-get install python3-tk python3-pil python3-pil.imagetk
```

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
