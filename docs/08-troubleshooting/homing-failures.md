# Homing failures

Stop with the E-stop first; a joint driven against its stop strips a belt or cracks a part.

## A joint does not stop at its switch

- **Joints 2, 3, 5** use mechanical limit switches. Check that the lever is pressed by the moving part, that
  the switch clicks, and that it is wired to 24 V and its signal terminal (polarity does not matter). The test
  firmware's `#LIMIT` shows the state live.
- **Joints 1, 4, 6** use inductive sensors that detect a screw head. The sensor's LED lights when it sees metal.
  If it does not light as the joint passes, adjust the trigger screw closer; the 4 mm sensors see about 1 to 2
  mm. Wiring: brown 24 V, blue GND, black signal.
- A switch on the wrong joint's terminal: the firmware maps the LIMIT inputs to joints as in
  [Connectors and pinout](../board/04-connectors.md); the test firmware shows which input changes.

## A joint stops too early

The switch triggers before the joint reaches it: a wire shorted, a sensor too close to a screw it should not
see, or a switch lever caught. Also the reason a homed pose is far off on one joint.

## Joint 6 turns more than a turn

Its sensor never sees the homing pin. Before homing, turn joint 6 by hand so that the pin is just before the
sensor in the direction of rotation ([Homing](../05-operation/homing.md)), and check the sensor's gap.

## Joint 5 does not reach its switch

The tool's homing feature is missing or in the wrong place, or the firmware's `j5_homing_offset` is for another
tool ([Your own tool](../end-effectors/custom-tools.md)).

## The homed pose does not match the witness marks

By a fraction of a degree: master the joint. By more: the joint slipped, a belt or coupler, or the switch
moved. Inspect, then master.

## Homing never finishes in the software

The PC lost the packet stream, or the firmware is waiting for a joint that does not report. Check the log, press
Clear error or `reset()`, and home again.
