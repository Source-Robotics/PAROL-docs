# 7. CAN bus

| | |
|---|---|
| CAN 1 | Transceiver fitted; terminals CAN H and CAN L; the gripper bus in PAROL6 |
| CAN 2 | Controller on the microcontroller, transceiver not populated |
| Bit rate | 1 Mbit/s, set by the firmware |
| Termination | None on the board; the gripper at the end of the bus has its own |

In PAROL6, CAN 1 runs with 24 V and GND to the M8 socket at the forearm. The firmware addresses one gripper at the
CAN ID the PC's packet names (0 as the grippers ship), sends it a move, a calibrate, a clear-error or an empty
status frame every cycle, and relays its answer to the PC: [CAN bus](../06-peripherals/can-bus.md) in the Robot
Manual, and the gripper manuals for the messages themselves.

A longer bus, with the gripper far from the board or more nodes on it, wants a 120 Ω terminator at the board end
as well: between CAN H and CAN L at the terminal block.
