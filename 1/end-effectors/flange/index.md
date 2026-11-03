# The flange

Joint 6 ends in an 8 mm output shaft. Tools clamp onto it with a shaft coupler (8 mm bore, M4 set screws, three
in the BOM) that bolts to the tool's holder; the SSG-48 and MSG grippers use a printed coupler connector made for
this shaft. The coupler's set screws take blue threadlocker: joint 6 slipping on its shaft is the first thing to
check when a tool's orientation drifts ([Couplers and threadlocker](https://docs.source-robotics.com/PAROL-docs/1/07-maintenance/couplers/)).

## Connections at the forearm

| | |
|---|---|
| **M8 4-pin connector** | 24 V, GND, CAN H, CAN L for an electric gripper; wired from the control board's CAN 1 and 24 V |
| **Two pneumatic tubes**, 4 mm | From the two push-in fittings at the base, through the arm, to the forearm |

The tubes and the gripper cable run through the arm and come out at the forearm. Joint 5 is held inside its
limits by its stops. Joint 6 has no limit with the bare flange; with a tool, the tool's cable and tubes run from
the forearm to the tool and wrap as joint 6 turns, so keep joint 6 within the turn they allow
([Joint limits and directions](https://docs.source-robotics.com/PAROL-docs/1/03-technical-data/joint-limits/#limits)).

## The tool in the software

The software must know the tool to compute the pose of its tip. The commander's kinematic model is built for the
standard pneumatic gripper; the Python API has tool definitions with variants and a settable TCP offset
([Tools and the TCP](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/tools-and-tcp/)):

```python
rbt.select_tool("PNEUMATIC")                       # default variant: vertical
rbt.select_tool("PNEUMATIC", variant_key="horizontal")
rbt.select_tool("SSG-48", variant_key="pinch")
rbt.select_tool("MSG", variant_key="150mm")
rbt.select_tool("VACUUM")
rbt.select_tool("NONE")                            # the bare flange
```

## Tool centre point

The tool centre point (TCP) is a6 = 50.5 mm from the joint 6 centre along the tool axis and a7 = 0 mm to the side.
With nothing on the flange, the TCP is the flange's reference point. The sheet is the robot's model from
[robot_descriptions](https://github.com/Source-Robotics/robot_descriptions) (version 2.15.1) with every joint at 0.
Tell the software about the tool ([Tools and the TCP](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/tools-and-tcp/)); every tool
is compared on [Dimensions and kinematics](https://docs.source-robotics.com/PAROL-docs/1/03-technical-data/kinematics/).

![PAROL6 with the flange only: dimensions to the TCP and the DH table](https://docs.source-robotics.com/PAROL-docs/1/assets/kinematics/parol6_flange.webp){ width="600" }
![PAROL6 with the flange only: dimensions to the TCP and the DH table](https://docs.source-robotics.com/PAROL-docs/1/assets/kinematics/parol6_flange_dark.webp){ width="600" }

## Homing and the tool

Joint 5 homes against a feature of the tool holder. The pneumatic gripper holder and the SSG-48's coupler
connector have it; a tool of your own needs it too, and the firmware's joint 5 homing offset must match the tool
([Your own tool](https://docs.source-robotics.com/PAROL-docs/1/end-effectors/custom-tools/)).

## Payload

1 kg near the base, 0.5 kg at full reach, the tool included. A gripper with a camera and a cable can be most of
that. A short video shows the arm with a 1 kg payload:
[PAROL6 robot arm 1kg payload](https://www.youtube.com/shorts/3Co42vz91Tg).
