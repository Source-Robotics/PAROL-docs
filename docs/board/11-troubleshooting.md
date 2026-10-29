# 11. Troubleshooting

| Symptom | Cause | Remedy |
|---|---|---|
| No life at all with 24 V connected | The button; the supply; a reversed XT30 | Check the supply's output, the JST button cable, the XT30 polarity. A reversed supply has usually destroyed the board |
| The board is on but cannot be switched off | 3.3 V on the programming header | Unplug the ST-Link or adapter |
| The board turns on when the supply is connected | The same, or a motor was turned by hand | Unplug the programmer; move an unpowered robot slowly |
| A driver reports no answer in `#STATUS` | Not seated; dead; wrong orientation | Power off, check the orientation against the DIAG pins, reseat. A driver that was powered the wrong way round is dead, and the board may be too |
| A motor hums but does not turn | A phase open; a motor wire loose in the terminal | Check the four wires of that joint's cable |
| A motor turns the wrong way | Normal for a new build | Flip `direction_reversed` in the main firmware |
| A switch does not show in `#LIMIT` | Wiring; the switch; the wrong terminal | Check 24 V to the switch and the signal wire; try the other terminals to find which input changes |
| An inductive sensor never triggers | Gap; no 24 V; the sensor is PNP | NPN NO sensors only; brown 24 V, blue GND, black signal; gap of a millimetre or two |
| The E-stop reads pressed with the button released | Wiring open; the button is NO | NC contact between the E-stop terminals |
| The drivers are hot and shut down | The fan | The fan must run; 5 V, not PWM |
| No serial port on the PC | The board has no power; the cable; the driver (Windows) | The board enumerates only when powered; try another cable and port |
| The main firmware does not upload | ST-Link driver; the adapter; the target not powered | Install STSW-LINK009; check the adapter's 3.3 V; disconnect the 24 V supply |

For anything the firmware reports to the PC, the robot-side pages apply: [Troubleshooting](../09-troubleshooting/index.md)
in the Robot Manual.
