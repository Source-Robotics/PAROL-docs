# Inputs and outputs

The control board has two isolated inputs and two isolated outputs on screw terminals at the side of the board,
reachable through the base. They are isolated from the robot's electronics through optocouplers, and they share
a supply that you choose.

## The supply

- **Isolated**: connect an external supply's negative to **GND_SEL** and positive to **HV_SEL**. The inputs and
  outputs then work at that voltage, 12 or 24 V (the inputs need at least 12 V), and a fault on them cannot reach
  the robot.
- **Not isolated**: link the robot's own 24 V and GND to HV_SEL and GND_SEL. Simpler, and the valve of the
  pneumatic gripper is usually wired this way. A 2 A fuse protects the outputs in this mode.

![Isolated supply wiring](https://docs.source-robotics.com/PAROL-docs/1/assets/Ext_supply.webp){ width="650" }

![Non-isolated wiring from the robot's 24 V](https://docs.source-robotics.com/PAROL-docs/1/assets/Internal_24V.webp){ width="650" }

The E-stop is not part of this: it is wired to the robot's own supply whichever option you choose.

## Inputs

Switches, push buttons, light barriers and sensors. A switch goes between **HV_SEL** and **IN1** or **IN2**; a
three-wire sensor takes HV_SEL and GND_SEL for its supply and gives its signal to the input. Input voltage 12 to
50 V, 24 V nominal.

The robot reports the inputs in every packet: the commander's **IO** tab shows them, and the Python API's `io()`
returns `[in1, in2, out1, out2, estop]`. RBTscript's `Input()` has no action yet: a program stops on it
([Known issues](https://docs.source-robotics.com/PAROL-docs/1/08-troubleshooting/known-issues/)).

## Outputs

Relays, valves, lamps, small actuators, up to 0.5 A each (1 A peak), 48 V maximum. A load goes between
**GND_SEL** and **OUT1** or **OUT2**; the output switches it to the supply. An inductive load, a valve or a relay
coil, gets a flyback diode across it.

=== "RBTscript"
    ```
    Output(1,HIGH)
    Output(1,LOW)
    ```

    Only output 1: in the current commander version `Output(2,...)` is refused by a bug in its check and stops
    the program ([RBTscript](https://docs.source-robotics.com/PAROL-docs/1/programming/03-commander/rbtscript/)).

=== "Python API"
    ```python
    rbt.write_io(0, 1)       # output 1 high (logical index 0)
    rbt.write_io(1, 0)
    ```

The commander's **IO** tab switches the outputs by hand.

![The IO tab of the commander software](https://docs.source-robotics.com/PAROL-docs/1/assets/IO_tab.PNG){ width="700" }
