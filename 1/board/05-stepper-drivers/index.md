# 5. Stepper drivers

![Four ways to destroy the control board](https://docs.source-robotics.com/PAROL-docs/1/assets/board_warning.svg){ width="1000" }

The board takes six TMC5160 driver modules in the StepStick format, configured over SPI by the firmware.

!!! danger "Orientation"
    A driver module inserted the wrong way round destroys the board the moment power is applied, permanently.
    The orientation is given by the two DIAG pins: they must point at the red arrows in the figure. Check all six
    before every power-on after the drivers were touched.

![Driver orientation: the DIAG pins at the red arrows](https://docs.source-robotics.com/PAROL-docs/1/assets/img_parol2.webp){ width="800" }

## Which drivers

Only the TMC5160 modules listed in the [BOM](https://docs.source-robotics.com/PAROL-docs/1/build/bill-of-materials/) are tested; a board bought with
drivers has them fitted. A module from elsewhere must have the pinout in the figure, and:

- **Remove the two DIAG pins** if they are soldered: the capacitors on the board are in their way and the
  module will not seat.
- **Cement the heatsink** to the driver with thermal cement (not paste, not tape); a driver without a bonded
  heatsink overheats and fails, and takes the board with it.

![The TMC5160 module pinout](https://docs.source-robotics.com/PAROL-docs/1/assets/stick.webp){ width="450" }

## Current

The firmware sets each driver's running and holding current for its joint ([Currents and temperatures](https://docs.source-robotics.com/PAROL-docs/1/03-technical-data/operating-temperatures/)
and [Firmware parameters](https://docs.source-robotics.com/PAROL-docs/1/reference/firmware-parameters/)). The modules' potentiometer, if they have one, is
not used.

## Cooling

The fan over the heatsinks must run whenever the motors are energised. A driver that gets too hot shuts its outputs
down and its joint goes limp, and firmware 1 does not tell the PC; in PAROL6's base with the fan they stay far
below that.

## Checking a driver

The test firmware reads every driver over SPI about three seconds after power-on and prints whether it answers
(`joint N Connection is: GOOD` or `BAD`) with its currents and fault flags, then turns every motor slowly
([The test firmware](https://docs.source-robotics.com/PAROL-docs/1/board/09-test-firmware/)). A driver that does not answer is not seated, dead, or in the wrong
slot.
