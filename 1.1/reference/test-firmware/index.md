# Test firmware commands

The commands the test firmware (`PAROL6 control board test code`) acts on: `#` followed by the name, case as
written, and a line feed (a terminal that sends only a carriage return gets no answer). None takes an argument.
[The test firmware](https://docs.source-robotics.com/PAROL-docs/1.1/board/09-test-firmware/) in the Control Board Manual shows the output.

!!! danger "The motors turn from power-on"
    The test firmware turns all six motors slowly from the moment it boots until the power is switched off; no
    command stops them.

| Command | What it does |
|---|---|
| `#IO` | Prints, once a second, the E-stop input, input 1, input 2 and the supply voltage in mV |
| `#LIMIT` | Prints, once a second, `Joint N is pressed` for every triggered limit switch |
| `#STOP` | Ends the `#IO` or `#LIMIT` printout; the motors keep turning |
| `#start` | Toggles the two LEDs |

The parser (`SerialPacketParser.cpp`) also recognises `STATUS`, `STEP1` to `STEP6`, `INPUT`, `ESTOP`, `OUT1TOGGLE`,
`OUT2TOGGLE`, `LED1TOGGLE`, `LED2TOGGLE`, `SUPPLYV`, `ONOFF`, `CAN` and `FLASH`, but `main.cpp` has no action for
them (the `FLASH` test is commented out): each is answered with `Unknown command`. The driver report (`joint N
Connection is: GOOD` or `BAD`, the currents and fault flags) is printed once, about three seconds after power-on,
not on a command.
