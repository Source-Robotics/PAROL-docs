# 5. Stepper drivers

The board takes six TMC5160 driver modules in the StepStick format, configured over SPI by the firmware.

!!! danger "Orientation"
    A driver module inserted the wrong way round destroys the board the moment power is applied, permanently.
    The orientation is given by the two DIAG pins: they must point at the red arrows in the figure. Check all six
    before every power-on after the drivers were touched.

![Driver orientation: the DIAG pins at the red arrows](../assets/img_parol2.png){ width="800" }

## Which drivers

Only the TMC5160 modules listed in the [BOM](../build/bill-of-materials.md) are tested; a board bought with
drivers has them fitted. A module from elsewhere must have the pinout in the figure, and:

- **Remove the two DIAG pins** if they are soldered: the capacitors on the board are in their way and the
  module will not seat.
- **Cement the heatsink** to the driver with thermal cement (not paste, not tape); a driver without a bonded
  heatsink overheats and fails, and takes the board with it.

![The TMC5160 module pinout](../assets/stick.png){ width="450" }

## Current

The firmware sets each driver's running and holding current for its joint ([Currents and temperatures](../03-technical-data/operating-temperatures.md)
and [Firmware parameters](../reference/firmware-parameters.md)). The modules' potentiometer, if they have one, is
not used.

## Cooling

The fan over the heatsinks must run whenever the motors are energised. The drivers warn at 100 °C and shut down at
120 °C; in PAROL6's base with the fan they stay far below.

## Checking a driver

The test firmware's `#STATUS` reads every driver over SPI and reports whether it answers and its flags; `#STEPx`
turns its motor slowly ([The test firmware](09-test-firmware.md)). A driver that does not answer is not seated,
dead, or in the wrong slot.
