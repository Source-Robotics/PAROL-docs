# CAN bus

The control board has a CAN bus for the electric grippers, wired to the M8 connector at the forearm. The board
is the master: it sends the gripper the command from the PC's packet every cycle (a move, a calibrate, a clear
error, or an empty status poll when nothing changed) and relays the gripper's answer back to the PC.

- **Bit rate**: 1 Mbit/s, the grippers' rate.
- **Node ID**: the gripper's CAN ID, 0 as shipped; the PC packet carries the ID the board addresses, so a gripper
  with another ID works if the software is told.
- **Termination**: 120 Ω at each end of the bus. At the board end, the **CAN1 JUMPER** connects the board's
  120 Ω resistor when it is on; at the other end, the gripper has its own termination switch, on as shipped
  ([CAN bus](https://docs.source-robotics.com/PAROL-docs/1.1/board/07-can/)).

A second CAN controller is on the board, but its transceiver is not populated: CAN 2 is for your own
experiments. More axes on the bus, a seventh axis or a second gripper, are not supported by the firmware or the
software yet; the protocol the grippers speak is documented in the [STEPFOC](https://docs.source-robotics.com/STEPFOC-docs/)
and [Spectral Micro](https://docs.source-robotics.com/Spectral-BLDC-docs/) references for anyone who wants to
extend it.

The electrical side is in [CAN bus](https://docs.source-robotics.com/PAROL-docs/1.1/board/07-can/) of the Control Board Manual.
