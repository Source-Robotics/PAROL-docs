# Installation

## Requirements

| You need | |
|---|---|
| Python 3.10 or 3.11 | Tested on 3.10.12 and 3.11.0; newer versions break some pinned dependencies |
| Windows, Linux or macOS | On macOS, follow the Linux steps, as the repository's README says |
| A PC that keeps the 100 Hz loop | [What you need](https://docs.source-robotics.com/PAROL-docs/1.1/01-overview/what-you-need/#the-pc) |

## Install

The commander goes into its own folder with its own virtual environment (`.venv`), on every operating system.

??? info "Why it needs its own virtual environment"
    It pins numpy 1.23.4 and the Python API needs numpy 2, so the two cannot share one Python: give each its own
    environment, as the [Quick start](https://docs.source-robotics.com/PAROL-docs/1.1/quick-start/) does.

=== "Windows"
    ```
    git clone https://github.com/Source-Robotics/PAROL-commander-software.git
    cd PAROL-commander-software
    py -3.11 -m venv .venv
    .venv\Scripts\activate
    python -m pip install -r requirements.txt
    ```

    - `py -3.11` picks Python 3.11 when several are installed; `py -3.10` works too.
    - The robot's serial port is `COM` and a number: Device Manager lists it under **Ports (COM & LPT)**.

=== "Linux"
    ```
    sudo apt install python3.11 python3.11-venv python3.11-tk
    git clone https://github.com/Source-Robotics/PAROL-commander-software.git
    cd PAROL-commander-software
    python3.11 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    sudo usermod -aG dialout $USER     # access to the serial port; log out and in again once
    ```

    - The robot's serial port is `ttyACM0` (`ls /dev/ttyACM*` lists it).

    ??? info "Which Python on Ubuntu"
        Ubuntu's own Python is 3.10 on 22.04 and 3.12 on 24.04. Where Python 3.11 is not in the distribution, the
        deadsnakes PPA has it (`sudo add-apt-repository ppa:deadsnakes/ppa` first). On 22.04 the system Python 3.10
        with `python3-venv` and `python3-tk` works as well.

=== "macOS"
    ```
    git clone https://github.com/Source-Robotics/PAROL-commander-software.git
    cd PAROL-commander-software
    python3.11 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    ```

    With Python 3.11 from python.org; the repository's README says the Linux steps work on macOS.

After the activate line the prompt starts with `(.venv)`. Activate the environment again in every new terminal
before you start the program.

??? info "If `requirements.txt` fails"
    The repository's [Windows](https://github.com/Source-Robotics/PAROL-commander-software/blob/main/Windows_install.md)
    and [Linux](https://github.com/Source-Robotics/PAROL-commander-software/blob/main/Linux_install.md) guides list
    the packages one by one. The robotics toolbox, swift, numpy and scipy are pinned to the versions that work
    together, and the `Working dependency` folder has the full module lists of PCs on which the software runs.

## Run

For the first run, write the robot's port into the program.

1. Open `GUI/files/Serial_sender_good_latest.py` in a text editor, and find these lines near the top:

    ```python
    if my_os == "Windows": 
        STARTING_PORT = 58 # COM3
    else:   
        STARTING_PORT = 0
    ```

2. Set the port:

    | On | Do |
    |---|---|
    | Windows | Replace `58` with the number of the robot's port (`5` for `COM5`; Device Manager, **Ports (COM & LPT)**, shows it) |
    | Linux | `0` means `/dev/ttyACM0` |

3. Save.
4. Start the program from the activated virtual environment:

    ```
    cd GUI/files
    python Serial_sender_good_latest.py
    ```

    Two windows open: the commander and the simulator.

5. Enter the serial port at the bottom of the commander (`COM5`, or `ttyACM0` on Linux).
6. Press **Connect**, more than once if needed.

![The connection bar](https://docs.source-robotics.com/PAROL-docs/1.1/assets/connect.PNG){ width="640" }

!!! note "A permission error on Linux"
    On Linux, a permission error on the port is fixed with `sudo chmod 666 /dev/ttyACM0`, or by joining the
    `dialout` group.

## Check the loop

The terminal the program runs in prints the robot's data. Watch `Time between 2 commands in ms` while you jog:

| It shows | Means |
|---|---|
| Near 0.010 | Right. The value is in seconds, whatever the label says: 0.010 is the 10 ms cycle. |
| Often much higher | The PC is too slow for the loop, and the robot will stutter ([Communication](https://docs.source-robotics.com/PAROL-docs/1.1/08-troubleshooting/communication/)) |

!!! success "Check"
    The commander shows the robot's data after **Connect**, and the simulator moves with the robot when you
    jog. If not: [Communication](https://docs.source-robotics.com/PAROL-docs/1.1/08-troubleshooting/communication/).
