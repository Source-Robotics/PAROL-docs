# 3. Connect and switch on

The firmware is on the board and the software is on your PC. Now connect the robot, switch it on and start the
software.

!!! danger "Read first"
    PAROL6 has no brakes: when the power goes, the arm falls. It has pinch points, it moves fast, and it moves by
    itself while homing. Anchor it to the table, keep the E-stop within reach, keep hands out of the arm's path, and
    read the [Safety](https://docs.source-robotics.com/PAROL-docs/1.1/02-safety/) chapter: it is five minutes long.

## 1. Anchor the robot

Bolt the base to the table through its six holes, or clamp it to the edge. A free-standing PAROL6 tips over when
it extends.

![The six holes in the base](https://docs.source-robotics.com/PAROL-docs/1.1/assets/base2.webp){ width="300" }

!!! success "Check"
    Push the top of the base sideways, firmly: it must not lift or slide.

More: [Mounting the robot](https://docs.source-robotics.com/PAROL-docs/1.1/04-installation/mounting/).

## 2. Connect

![The power (green), USB (blue) and E-stop (yellow and pink) connections, and the power button (red)](https://docs.source-robotics.com/PAROL-docs/1.1/assets/Connectors.webp){ width="640" }

1. Connect the E-stop to the two E-stop terminals on the base. Without it the robot will not run.
2. Connect the USB cable to the PC.
3. Connect the 24 V supply to the power connector.
4. Plug the supply's mains plug into the switched socket strip, or behind the mains switch. Keep the switch
   within your reach.

Nothing happens yet: the board is off until the button is pressed.

!!! info "A DIN-rail supply"
    A DIN-rail supply is wired and checked first: [The power supply](https://docs.source-robotics.com/PAROL-docs/1.1/04-installation/connecting/#the-power-supply).

More: [Connecting](https://docs.source-robotics.com/PAROL-docs/1.1/04-installation/connecting/).

## 3. Switch on

1. Hold the arm by the forearm.
2. Press the power button on the base.

3. The motors energise, you hear six clicks, and the arm holds its position. Let go.

!!! success "Check"
    Six drivers initialise and the arm supports itself before you let go. If it does not, use
    [First power-on: if nothing happens](https://docs.source-robotics.com/PAROL-docs/1.1/04-installation/first-power-on/#if-nothing-happens).

More: [First power-on](https://docs.source-robotics.com/PAROL-docs/1.1/04-installation/first-power-on/) · [Switching on and off](https://docs.source-robotics.com/PAROL-docs/1.1/05-operation/switching-on-off/).

## 4. Find the serial port

The **serial port** is the name the PC gives the USB connection.

=== "Windows"

    1. Right-click the Start button and open **Device Manager**.
    2. Open **Ports (COM & LPT)**.
    3. The robot is a "USB Serial Device" with a number, for example `COM5`.

        ![Device Manager with Ports (COM & LPT) open: the robot is the USB Serial Device, here COM5. A drawing; the other entries depend on the PC](https://docs.source-robotics.com/PAROL-docs/1.1/assets/quick-start/device-manager.svg){ width="500" }
        ![Device Manager with Ports (COM & LPT) open: the robot is the USB Serial Device, here COM5. A drawing; the other entries depend on the PC](https://docs.source-robotics.com/PAROL-docs/1.1/assets/quick-start/device-manager_dark.svg){ width="500" }

=== "Linux"

    Type this in the terminal. The port is usually `/dev/ttyACM0`:

    ```
    ls /dev/ttyACM*
    ```

    If the software later reports "permission denied", run this, then log out and in again:

    ```
    sudo usermod -aG dialout $USER
    ```

=== "macOS"

    Type this in the terminal:

    ```
    ls /dev/cu.usbmodem*
    ```

## 5. Start the software

=== "Commander software"

    For the first run, write the port into the program.

    1. Open `PAROL-commander-software/GUI/files/Serial_sender_good_latest.py` in a text editor. In VS Code:
       **File**, then **Open File**.
    2. Find these lines near the top:

        ```python
        if my_os == "Windows": 
            STARTING_PORT = 58 # COM3
        else:   
            STARTING_PORT = 0
        ```

    3. On Windows, replace `58` with the number of your port: `5` for `COM5`. On Linux, `0` is `/dev/ttyACM0`;
       change it if yours has another number.
    4. Save the file.
    5. Start the program in the terminal:

        === "Windows"

            ```
            cd %USERPROFILE%\Documents\PAROL-commander-software
            .venv\Scripts\activate
            cd GUI\files
            python Serial_sender_good_latest.py
            ```

        === "Linux"

            ```
            cd ~/Documents/PAROL-commander-software
            source .venv/bin/activate
            cd GUI/files
            python Serial_sender_good_latest.py
            ```

        === "macOS"

            ```
            cd ~/Documents/PAROL-commander-software
            source .venv/bin/activate
            cd GUI/files
            python Serial_sender_good_latest.py
            ```

        Two windows open: the commander and the simulator.

    6. At the bottom of the commander, type the serial port in the port field: `COM5` on Windows, `ttyACM0` on
       Linux.

        ![The connection bar](https://docs.source-robotics.com/PAROL-docs/1.1/assets/connect.PNG){ width="640" }

    7. Press **Connect**. Press it again if the first try fails.

=== "Python API"

    1. Start the **controller**, the program that talks to the robot, with your port:

        === "Windows"

            ```
            cd %USERPROFILE%\Documents\PAROL6-python-API
            .venv\Scripts\activate
            parol6-server --serial COM5
            ```

        === "Linux"

            ```
            cd ~/Documents/PAROL6-python-API
            source .venv/bin/activate
            parol6-server --serial /dev/ttyACM0
            ```

        === "macOS"

            ```
            cd ~/Documents/PAROL6-python-API
            source .venv/bin/activate
            parol6-server --serial /dev/cu.usbmodem…
            ```

            Type the full `/dev/cu.usbmodem…` name you found in step 4.

    2. Leave that terminal open.
    3. Open a **second** terminal. Activate the same virtual environment in it and start Python:

        === "Windows"

            ```
            cd %USERPROFILE%\Documents\PAROL6-python-API
            .venv\Scripts\activate
            python
            ```

        === "Linux"

            ```
            cd ~/Documents/PAROL6-python-API
            source .venv/bin/activate
            python
            ```

        === "macOS"

            ```
            cd ~/Documents/PAROL6-python-API
            source .venv/bin/activate
            python
            ```

        The prompt changes to `>>>`: Python now runs each line you type.

    4. Type these three lines:

        ```python
        from parol6 import RobotClient
        rbt = RobotClient()
        rbt.ping()
        ```

    5. Keep this second terminal open: the next steps type into it.

!!! success "Check"
    The commander's response log shows the robot's data, or `ping()` answers with `hardware_connected=True`. If
    it does not, use [Communication troubleshooting](https://docs.source-robotics.com/PAROL-docs/1.1/08-troubleshooting/communication/).

More: [The commander software](https://docs.source-robotics.com/PAROL-docs/1.1/gui/commander/) · [The Python API](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/).
