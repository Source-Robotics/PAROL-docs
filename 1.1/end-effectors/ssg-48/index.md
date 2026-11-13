# SSG-48 adaptive electric gripper

![The SSG-48 gripper](https://docs.source-robotics.com/PAROL-docs/1.1/assets/ssg48_hero.webp)

Source Robotics' 48 mm electric gripper: a Spectral Micro BLDC driver in gripper mode. It plugs into the M8
connector at the forearm, and the control board drives it over CAN. The commander software and the Python API both
know it.

Its own manual, [SSG48-gripper-docs](https://docs.source-robotics.com/SSG48-gripper-docs/), covers the gripper;
this page covers PAROL6.

| | |
|---|---|
| Stroke | 48 mm |
| Grip force | about 54 N per ampere, 5 to 80 N; on PAROL6 up to about 54 N from the commander, 70 N from the Python API |
| Fingers | fin-ray or pinch, printed: `finger` and `pinch` in the Python API |
| Shop | [SSG-48](https://source-robotics.com/products/compliant-gripper) |

## Mounting

1. Fit `coupler_connector_PAROL6` from the gripper's repository to the gripper. It carries:
    - a shaft coupler with an 8 mm bore and two M4 clamp screws, for the joint 6 shaft;
    - the homing tab that joint 5 homes against. The tab goes on the same side as the gripper's cable connector,
      with an M3 × 12 screw in the marked hole, as the gripper's
      [assembly manual](https://github.com/Source-Robotics/SSG-48-adaptive-electric-gripper/blob/main/Assembly%20manual/Gripper_assembly_manual.pdf)
      shows on its last pages.
2. Slide the gripper onto the joint 6 shaft, and orient it.
3. Tighten the two clamp screws, one on each side, with blue threadlocker
   ([Couplers and threadlocker](https://docs.source-robotics.com/PAROL-docs/1.1/07-maintenance/couplers/)).
4. Connect the [PAROL6 gripper cable](https://source-robotics.com/products/gripper-cable) between the gripper and
   the M8 connector at the forearm.

![The gripper connector at the forearm](https://docs.source-robotics.com/PAROL-docs/1.1/assets/GRIP_CON.webp){ width="600" }

!!! danger "Only the PAROL6 cable"
    PAROL6 and PAR6 put the four signals on different pins. The PAR6 cable reverses the gripper's supply, and a
    self-made cable with a wrong pin can put 24 V on a CAN pin; either destroys the gripper's driver. The
    socket's pins are in [The gripper socket](https://docs.source-robotics.com/PAROL-docs/1.1/end-effectors/flange/#the-gripper-socket), the cable's in the gripper
    manual's cable page.

Leave the gripper's CAN node ID at 0 and its termination switch on: it is the last node on the robot's bus
([CAN bus](https://docs.source-robotics.com/PAROL-docs/1.1/06-peripherals/can-bus/)).

## Tool centre point

| | SSG-48, both jaw variants |
|---|---|
| a6, from the joint 6 centre along the tool axis | 134.3 mm |
| a7, to the side | 0 mm |

The TCP lies on the joint 6 axis, with no sideways offset, for both jaw variants.

=== "Solid jaws"

    ![PAROL6 with the SSG-48, solid jaws: dimensions to the TCP and the DH table](https://docs.source-robotics.com/PAROL-docs/1.1/assets/kinematics/parol6_ssg48.webp){ width="600" }
    ![PAROL6 with the SSG-48, solid jaws: dimensions to the TCP and the DH table](https://docs.source-robotics.com/PAROL-docs/1.1/assets/kinematics/parol6_ssg48_dark.webp){ width="600" }

=== "Fin-ray jaws"

    ![PAROL6 with the SSG-48, fin-ray jaws: dimensions to the TCP and the DH table](https://docs.source-robotics.com/PAROL-docs/1.1/assets/kinematics/parol6_ssg48_stock.webp){ width="600" }
    ![PAROL6 with the SSG-48, fin-ray jaws: dimensions to the TCP and the DH table](https://docs.source-robotics.com/PAROL-docs/1.1/assets/kinematics/parol6_ssg48_stock_dark.webp){ width="600" }

The sheet is the robot's model from [robot_descriptions](https://github.com/Source-Robotics/robot_descriptions)
(version 2.15.1) with every joint at 0. Tell the software about the tool
([Tools and the TCP](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/tools-and-tcp/)); every tool is compared on
[Dimensions and kinematics](https://docs.source-robotics.com/PAROL-docs/1.1/03-technical-data/kinematics/).

## The joint 5 homing offset

Joint 5 homes against the tool, and the SSG-48's coupler sits differently from the pneumatic gripper holder.

1. Set `j5_homing_offset` to **8035** in `main.cpp` of the control board firmware. The default, 8900, is for the
   pneumatic gripper.
2. Upload ([Firmware](https://docs.source-robotics.com/PAROL-docs/1.1/board/08-firmware/)).
3. After the first homing, check with the pin through the joint 5 witness marks. Master if needed
   ([Mastering](https://docs.source-robotics.com/PAROL-docs/1.1/05-operation/mastering/)).

## Driving it

The gripper must be calibrated after every power-up: it opens fully and closes fully to find its end stops, and
does not move before that.

1. Clear any error.
2. Calibrate.
3. Wait until the gripper reports itself calibrated before the first move: about 3 s.

=== "Commander software"

    In the **Gripper** tab, after homing the robot:

    1. Press **Clear gripper error**.
    2. Press **Calibrate gripper**, and wait until the tab shows `Calibration status is: 1`.
    3. Set position, speed and current with the sliders.
    4. Press **Move GoTo**.

    The feedback section shows the current, the position and the status ([The GUI](https://docs.source-robotics.com/PAROL-docs/1.1/gui/commander/the-gui/)).

    ![The gripper tab](https://docs.source-robotics.com/PAROL-docs/1.1/assets/parol_grip_gui.PNG){ width="700" }

    In RBTscript, after clearing the error in the tab: `Gripper_cal()`, `Delay(4)`, then
    `Gripper(position, speed, current)` ([RBTscript](https://docs.source-robotics.com/PAROL-docs/1.1/programming/03-commander/rbtscript/#gripper)).

=== "Python API"

    ```python
    rbt.select_tool("SSG-48")                             # or add variant_key="pinch"
    rbt.tool.calibrate()                                   # queued; the API counts it done after 2 s
    rbt.delay(2)                                           # the rest of the calibration, with a margin
    rbt.tool.set_position(0.8, speed=0.5, current=0.4)     # fractions of the ranges; 0.4 is 580 mA
    rbt.tool.close(current=0.6)
    rbt.tool.open()
    rbt.tool.release()                                     # drop the grip, the jaws stay
    rbt.tool.stop()                                        # immediate: halt where the jaws are
    ```

    - Tool actions are queued with the motion, so a move after `close()` waits for the grip.
    - A `move` on a gripper that was never calibrated is refused when its turn comes.
    - The API does not read the calibrated bit and has no clear-error action at this version: clear an error in the
      commander's Gripper tab or with Motor GUI ([Tools and the TCP](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/tools-and-tcp/#calibrating),
      [Tools](https://docs.source-robotics.com/PAROL-docs/1.1/reference/python/tools/)).

## Current and force

The current limit is the grip force, about 54 N per ampere:

| Current | Grip force |
|---|---|
| 300 mA | About 16 N |
| 1 A | About 54 N |

Start low and raise it for a firmer grip. A high current with a high speed slams the jaws into the part. The
gripper manual's [Force and speed](https://docs.source-robotics.com/SSG48-gripper-docs/latest/03-technical-data/force-and-speed/)
has the curve and the heat limits.

| Program | Takes the current as | Strongest grip |
|---|---|---|
| Commander software | Milliamps, 100 to 1000 mA | About 54 N |
| Python API | A fraction of 100 to 1300 mA: `current=1.0` is 1.3 A | About 70 N |

## Status

The robot passes the gripper's status byte through: calibrated, in motion, object detected (while closing, while
opening, or none), and its error bits.

| Program | Shows |
|---|---|
| Commander, Gripper tab | The calibrated and E-stop error bits, and the whole status byte as a number (labelled *Gripper object detection is*) |
| Python API, `tool.status()` | The jaw position and the current. Its `engaged` and `part_detected` do not follow the status byte's bits at this version ([Tool status](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/tools-and-tcp/#tool-status)) |

The gripper manual's errors page says what each error needs:
[Errors and recovery](https://docs.source-robotics.com/SSG48-gripper-docs/latest/06-operation/errors/).
