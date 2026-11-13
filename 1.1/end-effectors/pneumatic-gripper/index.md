# Pneumatic gripper

The standard tool: an SMC MHZ2-16D parallel gripper in a printed holder, driven by a 5/2 solenoid valve from one
of the control board's outputs.

## Parts

| | |
|---|---|
| Gripper | MHZ2-16D, two PC4-M5 push-in fittings |
| Holder | `GRIPPER_ATTACHMENTS/Pneumatic_gripper_holder.STL` (vertical) or `Pneumatic_gripper_holder_horizontal.stl`; `Gripper_ARMS.STL` for the fingers |
| Valve | 5/2 solenoid valve, 24 V, 4 mm tube ports |
| Tube | 4 × 2.5 mm pneumatic tube, 5 m |
| Air | 5 to 7 bar; stay below the lowest rating of the gripper, the valve and the fittings ([Pneumatics](https://docs.source-robotics.com/PAROL-docs/1.1/06-peripherals/pneumatics/)) |

## Connections

![Pneumatic gripper tubing from the valve to the base and on to the gripper](../assets/pneumatic connection_edit.webp){ width="700" }

1. Join the two tubes from the gripper, where they leave the forearm, to the two tubes that run through the arm to
   the base.
2. Connect the valve's two outputs to the two fittings at the base.
3. Wire the valve's coil between **GND_SEL** and **OUTPUT1** on the control board, with the output supply set to
   the robot's 24 V or an isolated one ([Inputs and outputs](https://docs.source-robotics.com/PAROL-docs/1.1/06-peripherals/io/)).

!!! note "Which way round the tubes go"
    **Swapping the two tubes swaps normally open and normally closed**: choose the state the gripper should take
    without power.

## Tool centre point

| | Pneumatic gripper |
|---|---|
| a6, from the joint 6 centre along the tool axis | 62.3 mm |
| a7, to the side | 45.25 mm |

The TCP is the reference point of the original MHZ2-10D gripper, not a newly measured grasp centre.

![PAROL6 with the pneumatic gripper: dimensions to the TCP and the DH table](https://docs.source-robotics.com/PAROL-docs/1.1/assets/kinematics/parol6_pneumatic.webp){ width="600" }
![PAROL6 with the pneumatic gripper: dimensions to the TCP and the DH table](https://docs.source-robotics.com/PAROL-docs/1.1/assets/kinematics/parol6_pneumatic_dark.webp){ width="600" }

The sheet is the robot's model from [robot_descriptions](https://github.com/Source-Robotics/robot_descriptions)
(version 2.15.1) with every joint at 0. Tell the software about the tool
([Tools and the
TCP](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/tools-and-tcp/)); every tool is compared on [Dimensions and
kinematics](https://docs.source-robotics.com/PAROL-docs/1.1/03-technical-data/kinematics/).

## Driving it

=== "RBTscript"
    ```
    Output(1,HIGH)    // the valve switches
    Delay(0.5)
    Output(1,LOW)     // and back
    ```

=== "Python API"
    ```python
    rbt.select_tool("PNEUMATIC")
    rbt.tool.close()              # output 1 low
    rbt.tool.open()               # output 1 high
    rbt.write_io(0, 1)            # the same as open(), as a plain output
    ```

    The tool's action lasts its estimated stroke, so a move queued after `close()` waits for the gripper.

    !!! note "Lay the tubes to match open() and close()"
        The API's `open()` switches output 1 high and `close()` switches it low: lay the tubes so that the
        gripper is open with the valve switched, or `open()` and `close()` come out the other way round.

## Orientation

| Holder | The gripper | Python API variant |
|---|---|---|
| Vertical | Along the axis of joint 6 | `vertical` |
| Horizontal | Turned 90°, which reaches a table from the side | `horizontal` |

With the commander, remember that the DH dimensions a6 and a7 assume the vertical holder.
