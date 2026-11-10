# 7. CAN bus

| | |
|---|---|
| CAN 1 | Transceiver fitted; terminals CAN H and CAN L; the gripper bus in PAROL6 |
| CAN 2 | Controller on the microcontroller, transceiver not populated |
| Bit rate | 1 Mbit/s, set by the firmware |
| Termination | One jumper per bus, **CAN1 JUMPER** and **CAN2 JUMPER**: with the jumper on, a 120 Ω resistor is connected between CAN H and CAN L; with it off, the bus is not terminated on the board |

## In PAROL6

CAN 1 runs with 24 V and GND to the M8 socket at the forearm.

The firmware addresses one gripper, at the CAN ID the PC's packet names (0 as the grippers ship). Every cycle it
sends it a move, a calibrate, a clear-error or an empty status frame, and relays its answer to the PC.

More: [CAN bus](../06-peripherals/can-bus.md) in the Robot Manual, and the gripper manuals for the messages
themselves.

## Termination

A CAN bus is terminated at both of its ends, 120 Ω at each.

| End of the bus in PAROL6 | Its termination |
|---|---|
| The board | Its CAN1 jumper |
| The gripper | Its own termination switch |

Nodes in the middle of a longer bus stay unterminated. The jumpers are on the board figure in
[Connectors and pinout](04-connectors.md).
