# 8. Firmware

Two firmware programs exist for the board, both in the robot repository as PlatformIO projects:

| | Folder | For |
|---|---|---|
| **Main firmware** | `PAROL6 control board main software` | Running the robot with the commander software or the Python API |
| **Test firmware** | `PAROL6 control board test code` | Checking the board and the wiring from a serial terminal ([The test firmware](https://docs.source-robotics.com/PAROL-docs/1.1/board/09-test-firmware/)) |

A board from the shop carries the test firmware. Upload the main firmware before you use the robot.

## Tools

1. [VS Code](https://code.visualstudio.com/) with the **PlatformIO** extension from its marketplace.
2. A clone of the [robot repository](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm).
3. An **ST-Link** programmer and the [PAROL6 programming adapter](https://source-robotics.com/products/parol6-programming-adapter),
   or an ST-Link whose cable carries exactly SWCLK, SWDIO, GND and 3V3 to the pins of the 2×5 header in the
   table below.
4. On Windows, the [ST-Link USB driver (STSW-LINK009)](https://www.st.com/en/development-tools/stsw-link009.html)
   if PlatformIO cannot find the programmer.

!!! danger
    Use the programming adapter, or the four named pins only. An ST-Link wired to the header with jumper wires
    without the adapter has destroyed boards: other pins of the header are not for it.

The 2×5 programming header, as labelled in the side view of the [connections figure](https://docs.source-robotics.com/PAROL-docs/1.1/board/04-connectors/), left to
right, the header to the left of the USB port:

| Row | | | | | |
|---|---|---|---|---|---|
| Top | RESET | BOOT0 | **SWDIO** | none | **3V3** |
| Bottom | **GND** | GND | **CLK** (SWCLK) | none | 3V3 |

An ST-Link needs four of them: SWDIO, CLK, GND and 3V3. Leave RESET and BOOT0 unconnected.

## Uploading

1. **Disconnect the 24 V supply** from the robot.
2. Connect the adapter to the 2×5 header next to the USB port, and the ST-Link to the PC. The adapter supplies
   3.3 V, which powers the microcontroller (not the motors) and turns the board on.
3. In VS Code, **Open Folder** on the firmware's folder. PlatformIO downloads the toolchain the first time.
4. Build and **Upload** (the arrow in PlatformIO's toolbar). The upload takes a few seconds.
5. Disconnect the adapter. With it connected, the board cannot be switched off with the button and turns on by
   itself when the supply is connected.
6. Reconnect the 24 V supply and press the power button.

!!! success "Check"
    PlatformIO ends the upload with `SUCCESS`, and after step 6 the drivers click and the PC software
    connects. If not: [Troubleshooting](https://docs.source-robotics.com/PAROL-docs/1.1/board/11-troubleshooting/).

## Version

`#define VERSION 1` in `constants.h`. The firmware is released with the robot (tag V1) and has not changed since: release V1.1 ships the same firmware;
the protocol it speaks is on [The serial protocol](https://docs.source-robotics.com/PAROL-docs/1.1/board/10-serial-protocol/).
