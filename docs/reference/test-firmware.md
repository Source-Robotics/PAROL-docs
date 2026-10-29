# Test firmware commands

The commands the test firmware (`PAROL6 control board test code`) accepts on its serial port, as its parser
(`SerialPacketParser.cpp`) matches them: `#` followed by the name, case as written, Enter. None takes an
argument. [The test firmware](../board/09-test-firmware.md) in the Control Board Manual shows the output.

| Command | What it does |
|---|---|
| `#start` | Toggles the two LEDs and starts the motor spin test |
| `#STOP` | Stops the running test |
| `#STATUS` | Reads every driver over SPI: answering or not, and its flags |
| `#STEP1` to `#STEP6` | Turns the motor of driver position 1 to 6 slowly |
| `#LIMIT` | Prints the LIMIT inputs, live |
| `#IO` | Prints inputs, outputs, E-stop and the supply voltage in mV, repeatedly |
| `#INPUT` | Prints the two inputs |
| `#ESTOP` | Prints the E-stop input |
| `#OUT1TOGGLE`, `#OUT2TOGGLE` | Toggles output 1 or 2 |
| `#LED1TOGGLE`, `#LED2TOGGLE` | Toggles LED 1 or 2 |
| `#SUPPLYV` | Prints the supply voltage |
| `#ONOFF` | Toggles the 24 V power stage |
| `#CAN` | Sends a CAN test frame |
| `#FLASH` | Tests the SPI flash |

Driver positions are the board's slots, not joint numbers: position 2 is joint 5, 3 is joint 6, 5 is joint 3 and
6 is joint 2 ([Connectors and pinout](../board/04-connectors.md)).
