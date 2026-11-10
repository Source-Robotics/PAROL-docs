# CAN bus

The control board has a CAN bus for the electric grippers, wired to the M8 connector at the forearm.

The board is the master. Every cycle it sends the gripper the command from the PC's packet: a move, a calibrate, a
clear error, or an empty status poll when nothing changed. Then it relays the gripper's answer back to the PC.

| | |
|---|---|
| **Bit rate** | 1 Mbit/s, the grippers' rate |
| **Node ID** | The gripper's CAN ID, 0 as shipped. The PC packet carries the ID the board addresses, so a gripper with another ID works if the software is told. |
| **Termination** | 120 Ω at each end of the bus |

The termination, at each end ([CAN bus](../board/07-can.md)):

| End | Termination |
|---|---|
| The board | The **CAN1 JUMPER** connects the board's 120 Ω resistor when it is on |
| The gripper | Its own termination switch, on as shipped |

## CAN 2, and more axes

- A second CAN controller is on the board, but its transceiver is not populated: CAN 2 is for your own
  experiments.
- More axes on the bus, a seventh axis or a second gripper, are not supported by the firmware or the software yet.
  The protocol the grippers speak is documented in the [STEPFOC](https://docs.source-robotics.com/STEPFOC-docs/)
  and [Spectral Micro](https://docs.source-robotics.com/Spectral-BLDC-docs/) references, for anyone who wants to
  extend it.

The electrical side is in [CAN bus](../board/07-can.md) of the Control Board Manual.
