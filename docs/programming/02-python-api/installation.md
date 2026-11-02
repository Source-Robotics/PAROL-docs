# Installation

## Requirements

- Python 3.11 or newer.
- Windows (x86-64), Linux (x86-64, ARM64) or macOS (ARM64): the kinematics backend, pinokin, ships wheels for
  these.
- The PC at the robot: the [minimum PC](../../01-overview/what-you-need.md#the-pc) of the Robot Manual. A client
  that only sends commands runs anywhere.

## Install

From a clone of [PAROL6-python-API](https://github.com/PCrnjak/PAROL6-python-API), in a virtual environment:

=== "Windows"
    ```
    git clone https://github.com/PCrnjak/PAROL6-python-API.git
    cd PAROL6-python-API
    git checkout <!-- api-version -->
    py -3.11 -m venv .venv
    .venv\Scripts\activate
    pip install .
    ```
    The robot's serial port is `COM` and a number: Device Manager lists it under **Ports (COM & LPT)**.

=== "Linux"
    ```
    git clone https://github.com/PCrnjak/PAROL6-python-API.git
    cd PAROL6-python-API
    git checkout <!-- api-version -->
    python3 -m venv .venv
    source .venv/bin/activate
    pip install .
    sudo usermod -aG dialout $USER     # access to the serial port; log out and in again once
    ```
    The robot's serial port is `/dev/ttyACM0` (`ls /dev/ttyACM*` lists it).

=== "macOS"
    ```
    git clone https://github.com/PCrnjak/PAROL6-python-API.git
    cd PAROL6-python-API
    git checkout <!-- api-version -->
    python3 -m venv .venv
    source .venv/bin/activate
    pip install .
    ```
    Apple silicon (ARM64) only. The robot's serial port is `/dev/cu.usbmodem` and a number
    (`ls /dev/cu.usbmodem*` lists it).

The package pulls numpy, msgspec, pinokin, Ruckig, python-can and the
waldoctl interface layer. `pip install -e .` installs it editable for development.

## Check

```
parol6-server --log-level=INFO
```

starts the controller in simulator mode when no serial port is given. In another terminal:

```python
from parol6 import RobotClient
with RobotClient() as rbt:
    print(rbt.ping())
```

!!! check "Check"
    It prints a `PingResult` with `hardware_connected=0`. Stop the server with Ctrl-C.

## Versions

The API is pre-1.0 and released often; a minor version can change an interface, and the controller and the
client must be the same version, since they share the wire protocol. The [release notes](../../appendix/release-notes.md)
list the changes; this site describes <!-- api-version -->.
