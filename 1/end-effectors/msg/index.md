# MSG compliant AI stepper gripper

![The MSG gripper](https://docs.source-robotics.com/PAROL-docs/1/assets/msg_hero.webp)

Source Robotics' modular stepper gripper: a STEPFOC driver in gripper mode, three rail lengths, three stepper
lengths and a camera mount. It plugs into the M8 connector at the forearm and the control board drives it over
CAN with the same commands as the SSG-48. Its own manual, [MSG-gripper-docs](https://docs.source-robotics.com/MSG-gripper-docs/),
covers the gripper; this page covers PAROL6.

| | |
|---|---|
| Stroke | 55, 105 or 155 mm, with the 100, 150 or 200 mm rail |
| Grip force | about 20, 25 or 36 N per ampere with the 21.5, 40 or 60 mm stepper; up to about 31, 50 or 76 N |
| Mass | about 380 g plus the camera: mind the [payload](https://docs.source-robotics.com/PAROL-docs/1/end-effectors/flange/#payload) at full reach |
| Shop | [MSG gripper](https://source-robotics.com/products/msg-gripper) |

## Mounting

1. Replace the gripper's `ring_cover` with `ring_cover-PAROL6` from the repository's `Common parts`: it bolts to
   the robot's last joint, and the coupler plate's shaft coupler (8 mm bore, two M4 clamp screws) takes the
   joint 6 shaft ([Mounting on a robot](https://docs.source-robotics.com/MSG-gripper-docs/latest/04-installation/mounting/)).
2. Slide the gripper onto the shaft, orient it with the camera looking down between the jaws, and tighten the
   two clamp screws with blue threadlocker ([Couplers and threadlocker](https://docs.source-robotics.com/PAROL-docs/1/07-maintenance/couplers/)).
3. Connect the [PAROL6 gripper cable](https://source-robotics.com/products/gripper-cable) between the gripper
   and the M8 connector at the forearm.
4. The camera is a plain USB camera with its own cable: route it outside the arm, with slack for joints 4, 5
   and 6, and fix it so the arm cannot catch it.

!!! danger "Only the PAROL6 cable"
    PAROL6 and PAR6 put the four signals on different pins. The PAR6 cable, or a self-made cable with a wrong
    pin, puts 24 V on the CAN pins and destroys the gripper's driver. The gripper manual's cable page has the
    pinout to check your own against.

Leave the gripper's CAN node ID at 0 and its termination switch, reachable through the stepper cover, on: it is
the last node on the robot's bus ([CAN bus](https://docs.source-robotics.com/PAROL-docs/1/06-peripherals/can-bus/)).

## Tool centre point

The tool centre point (TCP) is a6 = 134.3 mm from the joint 6 centre along the tool axis and a7 = 28.35 mm to the
side. Both jaw variants share one TCP: an operating point, not a measured grasp centre. The sheet is the robot's
model from [robot_descriptions](https://github.com/Source-Robotics/robot_descriptions) (version 2.15.1) with every
joint at 0. Tell the software about the tool ([Tools and the TCP](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/tools-and-tcp/));
every tool is compared on [Dimensions and kinematics](https://docs.source-robotics.com/PAROL-docs/1/03-technical-data/kinematics/).

=== "Solid jaws"

    ![PAROL6 with the MSG, solid jaws: dimensions to the TCP and the DH table](https://docs.source-robotics.com/PAROL-docs/1/assets/kinematics/parol6_msg.webp){ width="600" }
    ![PAROL6 with the MSG, solid jaws: dimensions to the TCP and the DH table](https://docs.source-robotics.com/PAROL-docs/1/assets/kinematics/parol6_msg_dark.webp){ width="600" }

=== "Soft TPU jaws"

    ![PAROL6 with the MSG, soft TPU jaws: dimensions to the TCP and the DH table](https://docs.source-robotics.com/PAROL-docs/1/assets/kinematics/parol6_msg_tpu_glue.webp){ width="600" }
    ![PAROL6 with the MSG, soft TPU jaws: dimensions to the TCP and the DH table](https://docs.source-robotics.com/PAROL-docs/1/assets/kinematics/parol6_msg_tpu_glue_dark.webp){ width="600" }

## The joint 5 homing offset

Joint 5 homes against the tool, and the MSG's ring cover is not the pneumatic gripper holder that the firmware's
default offset (8900) assumes. After the first homing, check joint 5 with the pin through the witness marks; if
it is off, measure the offset and set `j5_homing_offset` in `main.cpp` as [Mastering](https://docs.source-robotics.com/PAROL-docs/1/05-operation/mastering/)
describes.

## Driving it

The gripper must be calibrated after every power-up: it opens fully and closes fully to find its end stops, and
does not move before that. Clear any error first, then calibrate, then wait until the gripper reports itself
calibrated before the first move: about 5 to 6 s on the longer rails.

=== "Commander software"
    The **Gripper** tab: after homing the robot press **Clear gripper error**, then **Calibrate gripper**, and
    wait until the tab shows `Calibration status is: 1`. Then set position, speed and current with the sliders
    and press **Move GoTo**. The feedback section shows the current, the position and the status
    ([The GUI](https://docs.source-robotics.com/PAROL-docs/1/gui/commander/the-gui/)). In RBTscript, after clearing the error in the tab:
    `Gripper_cal()`, `Delay(7)`, then `Gripper(position, speed, current)`
    ([RBTscript](https://docs.source-robotics.com/PAROL-docs/1/programming/03-commander/rbtscript/#gripper)).

=== "Python API"
    ```python
    rbt.select_tool("MSG", variant_key="150mm")           # 100mm, 150mm or 200mm: the rail
    rbt.tool.calibrate()                                   # queued; the API counts it done after 2 s
    rbt.delay(5)                                           # the rest of the calibration, with a margin
    rbt.tool.set_position(0.8, speed=0.5, current=0.4)     # fractions of the ranges; 0.4 is 1180 mA
    rbt.tool.close(current=0.4)
    rbt.tool.open()
    rbt.tool.release()                                     # drop the grip, the jaws stay
    rbt.tool.stop()                                        # immediate: halt where the jaws are
    ```
    Tool actions are queued with the motion, so a move after `close()` waits for the grip; a `move` on a gripper
    that was never calibrated is refused when its turn comes. The API does not read the calibrated bit and has
    no clear-error action at this version: clear an error in the commander's Gripper tab or with Motor GUI
    ([Tools and the TCP](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/tools-and-tcp/#calibrating),
    [Tools](https://docs.source-robotics.com/PAROL-docs/1/reference/python/tools/)).

## Current and force

The current limit is the grip force, and the slope depends on the stepper: about 20 N per ampere with the
21.5 mm stepper, 25 with the 40 mm, 36 with the 60 mm. Stay within the stepper's maximum, 1.5 A, 2.0 A or 2.1 A.
The gripper manual's [Force and speed](https://docs.source-robotics.com/MSG-gripper-docs/latest/03-technical-data/force-and-speed/)
has the curves.

The commander takes the current in milliamps, 100 to 1000 mA, which is within every stepper's maximum. The
Python API takes it as a fraction of 100 to 2800 mA, a range above every stepper's maximum, so keep the fraction
at or below the value for your stepper:

| Stepper | Maximum current | Highest `current=` fraction |
|---|---|---|
| 21.5 mm | 1.5 A | 0.51 |
| 40 mm | 2.0 A | 0.70 |
| 60 mm | 2.1 A | 0.74 |

## Status

The robot passes the gripper's status byte through: calibrated, in motion, object detected (while closing, while
opening, or none), and its error bits. The commander's Gripper tab shows the calibrated and E-stop error
bits, and the whole status byte as a number (labelled *Gripper object detection is*). The Python API's `tool.status()` gives the jaw position and the current; its
`engaged` and `part_detected` do not follow the status byte's bits at this version
([Tool status](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/tools-and-tcp/#tool-status)). The gripper manual's errors page says
what each error needs: [Errors and recovery](https://docs.source-robotics.com/MSG-gripper-docs/latest/06-operation/errors/).
