# Switching on and off

## Switching on

1. E-stop connected and released; power supply on; USB to the PC.
2. Hold the arm by the forearm.
3. Press the power button on the base. The fan starts, the six drivers initialise with a click each, and the
   motors hold the arm.
4. Start the PC software and connect. The robot is enabled and not homed; nothing moves until you command it.

The firmware energises the motors at the moment the 24 V stage comes up, whether or not a PC is connected, and
holds them with the holding current from then on.

## Switching off

!!! danger "Not while it moves"
    Never switch the robot off while it is running a program or carrying something. If it behaves unexpectedly,
    press the E-stop; if the E-stop has no effect, switch off the power supply. The power button is the last
    resort, and only with the arm held.

1. Stop the program and bring the arm to the **parked pose**, folded in over the base, where it has the least
   distance to fall. In the commander, **Park** writes a three-line program into the program window that moves
   there; press **Start** to run it. In the Python API,
   `rbt.move_j([90, -144.683, 108.171, 2.222, 25.003, 180], speed=0.3)` moves to the same pose.
2. Disconnect in the software, or stop the controller.
3. Hold the forearm.
4. Press the power button. The motors release at once and the arm goes limp in your hand.

## The button and the programming adapter

The button does not switch the power line: it tells the firmware to turn the 24 V stage on and off. The
microcontroller itself runs from 3.3 V derived from that stage, or from the programming header. **While an
ST-Link or the programming adapter is connected, the board has 3.3 V, turns on by itself when the supply is
plugged in, and cannot be switched off with the button.** Upload firmware with the 24 V supply disconnected, then
unplug the adapter, then plug the supply in and press the button ([Firmware](https://docs.source-robotics.com/PAROL-docs/1/board/08-firmware/)).

## After a power failure

The arm has fallen. Check that nothing is damaged and nothing is trapped under it, switch on as above, and home
before anything else: the position is lost.
