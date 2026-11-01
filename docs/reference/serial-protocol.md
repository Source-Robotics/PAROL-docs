# The serial protocol

The packets between the PC and the control board, from the firmware's `main.cpp` (`Unpack_data`, `Pack_data`).
Serial over USB at 3 000 000 baud; the PC sends one command packet per 10 ms cycle and the board answers each
valid packet with one telemetry packet. Multi-byte values are big-endian; positions and speeds are signed 24-bit
integers in motor microsteps and microsteps per second. [The serial protocol](../board/10-serial-protocol.md) in
the Control Board Manual explains the cycle.

## PC → board: the command packet

| Offset after the length byte | Size | Field | Meaning |
|---|---|---|---|
| — | 3 | Start bytes | `0xFF 0xFF 0xFF` |
| — | 1 | Length | 52: the number of bytes that follow, CRC and end bytes included |
| 0 | 18 | Joints[6] | Commanded position of each joint, 3 bytes each, signed, microsteps |
| 18 | 18 | Speed[6] | Commanded speed of each joint, 3 bytes each, signed, microsteps/s |
| 36 | 1 | Command | The command byte, below |
| 37 | 1 | Affected joint | Bit per joint; reserved |
| 38 | 1 | InOut | Bits from the MSB: bit 2 = output 1, bit 3 = output 2; the rest reserved |
| 39 | 1 | Timeout | Reserved |
| 40 | 2 | Gripper position | 0 to 255 |
| 42 | 2 | Gripper speed | 0 to 255 |
| 44 | 2 | Gripper current | mA |
| 46 | 1 | Gripper command | Bits from the MSB: 0 activate, 1 action, 2 E-stop, 3 release direction |
| 47 | 1 | Gripper mode | 0 operate, 1 calibrate, 2 clear error |
| 48 | 1 | Gripper ID | The gripper's CAN ID |
| 49 | 1 | CRC | Reserved: carried, not checked by firmware 1 |
| 50 | 2 | End bytes | `0x01 0x02` |

## Command bytes

| Value | Name | Effect |
|---|---|---|
| 255 | Idle (dummy) | The joints stand still (speeds are set, no joint is stepped). Continues a homing in progress |
| 123 | Jog | Runs each joint at its commanded speed |
| 156 | Go to position with speed | Runs each joint at the average of the commanded speed and the speed that closes the position error in one cycle |
| 100 | Home | Starts the homing sequence |
| 101 | Enable | Enables motion, resets the homing state |
| 102 | Disable | Disables motion; the motors hold |
| 103 | Clear error | Resets the homing state |
| 69 | Repeatability test | A built-in two-pose cycle |

The gripper fields are forwarded over CAN every cycle: a move frame when any of them changed, a calibrate for
mode 1, a clear error for mode 2, an empty status poll otherwise.

## Board → PC: the telemetry packet

| Offset after the length byte | Size | Field | Meaning |
|---|---|---|---|
| — | 3 | Start bytes | `0xFF 0xFF 0xFF` |
| — | 1 | Length | 56 |
| 0 | 18 | Position[6] | Actual position of each joint, 3 bytes each, signed, microsteps |
| 18 | 18 | Speed[6] | Actual speed of each joint |
| 36 | 1 | Homed | Bits from the MSB: joint 1 to joint 6 homed; bits 6 and 7 set |
| 37 | 1 | IO | Bits from the MSB: input 1, input 2, output 1, output 2, E-stop (1 = closed, not pressed); bits 5 to 7 set |
| 38 | 1 | Temperature error | Bits from the MSB: joint 1 to joint 6, reserved, reported cleared by firmware 1; bits 6 and 7 set |
| 39 | 1 | Position error | Bits from the MSB: joint 1 to joint 6, reserved; bits 6 and 7 set |
| 40 | 2 | Timing data | Ticks of 1.422 µs between the last two valid packets (90 MHz / 128); 7031 = 10 ms |
| 42 | 1 | Timeout error | Reserved |
| 43 | 1 | XTR2 | The last command byte received |
| 44 | 1 | Gripper ID | Always 0 in firmware 1 (not reported by the gripper) |
| 45 | 2 | Gripper position | 0 to 255 |
| 47 | 2 | Gripper speed | Always 1 in firmware 1 (not reported by the gripper) |
| 49 | 2 | Gripper current | mA |
| 51 | 1 | Gripper status | The gripper's status byte, bits from the MSB: activated, moving to a position, object detection (two bits: 0 moving, 1 object while closing, 2 object while opening, 3 at position), temperature error, timeout error, E-stop error, calibrated |
| 52 | 1 | Object detection | Always 1 in firmware 1; the real value is in the status byte's object-detection bits |
| 53 | 1 | CRC | Reserved |
| 54 | 2 | End bytes | `0x01 0x02` |

The gripper's status byte and object detection are as the gripper manuals define them.
