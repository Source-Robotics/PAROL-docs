# 9. The test firmware

The test firmware turns the board into a bench instrument: it talks in plain text over USB and lets you exercise
each driver, each switch and sensor, the inputs, the outputs, the E-stop and the flash, one at a time. It is what
every board ships with, and the right tool for a freshly wired robot before the base is closed.

!!! danger
    `#start` spins all six motors at once, and `#STEPx` turns one, with no limits and no homing. Use the test
    firmware with the arm free to move or the motors unmounted, never on a robot folded against its stops.

## Connecting

Upload the firmware if the board does not have it ([Firmware](08-firmware.md)), then open a serial terminal on
the board's port at 115200 baud (PlatformIO's monitor, PuTTY, `screen`). Two ways to power the board for the
test:

- the programming adapter's 3.3 V, with the 24 V supply disconnected: the board talks, but the drivers have no
  power and report errors;
- the 24 V supply: the board is off until you hold the power button, or supply 3.3 V from the adapter as well.

Commands are `#` followed by the name, case as written, and Enter.

## Commands

| Command | What it does |
|---|---|
| `#start` | Toggles the LEDs and starts the motor spin test on all drivers |
| `#STOP` | Stops the running test |
| `#STATUS` | Reads each driver over SPI and prints whether it answers and its flags |
| `#STEP1` … `#STEP6` | Turns the motor of driver position 1 to 6 slowly (the positions, not the joints: [Connectors and pinout](04-connectors.md)) |
| `#LIMIT` | Prints the state of the six LIMIT inputs, live; press a switch and watch |
| `#IO` | Prints the inputs, the outputs, the E-stop and the supply voltage in millivolts, repeatedly |
| `#INPUT` | Prints the two inputs |
| `#ESTOP` | Prints the E-stop input |
| `#OUT1TOGGLE`, `#OUT2TOGGLE` | Toggles an output |
| `#LED1TOGGLE`, `#LED2TOGGLE` | Toggles an LED |
| `#SUPPLYV` | Prints the supply voltage |
| `#ONOFF` | Toggles the 24 V power stage |
| `#CAN` | Sends a CAN test frame |
| `#FLASH` | Tests the SPI flash memory |

[Test firmware commands](../reference/test-firmware.md) is the reference list.

## What good looks like

All six drivers answering:

![Serial output with all drivers responding](../assets/STEPPER_GOOD.PNG){ width="600" }

A driver missing or faulty:

![Serial output with a faulty driver](../assets/BAD_STEPPER_DRIVER.PNG){ width="600" }

With good drivers and the 24 V on, the motors spin slowly at 200 to 300 mA when the test runs. A triggered limit
switch:

![A limit switch triggered](../assets/LIMIT_GOOD.PNG){ width="550" }

The I/O report; change the E-stop or an input and the values follow:

![The IO report](../assets/GOOD_IO.PNG){ width="550" }

Outputs 1 and 2 toggle every second during the test, and the two LEDs blink.
