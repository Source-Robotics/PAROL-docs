# First power-on

The first time, and every time after that:

1. **Check the E-stop is connected** and released.
2. **Hold the arm by the forearm.** The motors energise with a jolt, and until they do the arm is limp.
3. **Press the power button** on the base. The 24 V stage switches on, each driver initialises with a click, six
   clicks, and the arm holds its position.
4. Let go. The robot is now enabled, not homed, and waiting for the PC.

!!! success "Check"
    Six clicks, the fan runs, and the arm holds when you let go. If not: [If nothing happens](#if-nothing-happens).

Nothing moves until the PC software commands it. Start the [commander software](https://docs.source-robotics.com/PAROL-docs/1.1/gui/commander/)
or the [Python API's controller](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/controller/), connect, check the jog directions
and home: the [Quick start](https://docs.source-robotics.com/PAROL-docs/1.1/quick-start/) walks through it.

## What the button does

The button is not a switch in the power line: it tells the firmware to turn the 24 V stage on, and the firmware
keeps it on. A short press while the robot is on turns it off. The board stays powered, and turns itself on, as
long as 3.3 V is present on the programming header, which is why a connected ST-Link keeps the robot on and the
button useless: [Switching on and off](https://docs.source-robotics.com/PAROL-docs/1.1/05-operation/switching-on-off/).

## If nothing happens

- No clicks, no fan: no 24 V. Check the supply, the GX16 cable and its polarity.
- Clicks, but the PC software does not connect: the serial port name, or the board runs the test firmware. See
  [Communication](https://docs.source-robotics.com/PAROL-docs/1.1/08-troubleshooting/communication/).
- The board turned on by itself when the supply was plugged in: something supplies 3.3 V to the programming
  header, or the arm was moved while unpowered ([Hazards](https://docs.source-robotics.com/PAROL-docs/1.1/02-safety/hazards/#stepper-induced-voltage)).
