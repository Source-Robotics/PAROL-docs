# First power-on

The first time, and every time after that:

![The power (green), USB (blue) and E-stop (yellow and pink) connections, and the power button (red)](../assets/Connectors.webp){ width="560" }

1. **Check the E-stop is connected** and released.
2. **Hold the arm by the forearm.** The motors energise with a jolt, and until they do the arm is limp.
3. **Press the power button** on the base. The 24 V stage switches on, and each driver initialises with a click:
   six clicks. The arm holds its position.
4. Let go. The robot is now enabled, not homed, and waiting for the PC.

!!! success "Check"
    Six clicks, the fan runs, and the arm holds when you let go. If not: [If nothing happens](#if-nothing-happens).

Nothing moves until the PC software commands it. Next:

1. Start the [commander software](../gui/commander/index.md) or the
   [Python API's controller](../programming/02-python-api/controller.md), and connect.
2. Check the jog directions.
3. Home.

The [Quick start](../quick-start.md) walks through it.

## What the button does

The button is not a switch in the power line. It tells the firmware to turn the 24 V stage on, and the firmware
keeps it on. A short press while the robot is on turns it off.

The board stays powered, and turns itself on, as long as 3.3 V is present on the programming header. That is why a
connected ST-Link keeps the robot on and the button useless: [Switching on and off](../05-operation/switching-on-off.md).

## If nothing happens

| What you see | What it means, what to do |
|---|---|
| No clicks, no fan | No 24 V. Check the supply, the GX16 cable and its polarity. |
| Clicks, but the PC software does not connect | The serial port name, or the board runs the test firmware. See [Communication](../08-troubleshooting/communication.md). |
| The board turned on by itself when the supply was plugged in | Something supplies 3.3 V to the programming header, or the arm was moved while unpowered ([Hazards](../02-safety/hazards.md#stepper-induced-voltage)). |
