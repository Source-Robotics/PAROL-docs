# Hazards

## Pinch and crush points

Every joint is a pinch point, and the elbow and wrist fold against the upper arm and forearm. The motors are
geared: a finger between two links when a joint closes is crushed, not pushed away. Keep hands, cables and tubes
out of the arm's path while it is enabled, and never reach into the workspace of a running program. Under the
elbow, the belt that drives joint 3 runs onto its pulley: a finger or a loose cable there is drawn in.

![The pinch points of PAROL6, after homing: the wrist, the elbow, the belt and pulley under the elbow, the shoulder and the base](https://docs.source-robotics.com/PAROL-docs/1.1/assets/figures/parol6_pinch_points.webp){ width="550" }
![The pinch points of PAROL6, after homing: the wrist, the elbow, the belt and pulley under the elbow, the shoulder and the base](https://docs.source-robotics.com/PAROL-docs/1.1/assets/figures/parol6_pinch_points_dark.webp){ width="550" }

## Clothing, hair and eyes

A joint that closes catches more than fingers: its belts and pulleys pull in hair, loose sleeves, scarves,
lanyards and jewellery. Tie back long hair and take those off before you work at a powered robot, and keep them
out of the arm's reach while it moves. Wear safety glasses with a pneumatic gripper, with a sharp or pointed
tool, and whenever the robot can drop or throw a part.

## The arm falls when the power goes

PAROL6 has no brakes. The moment the motors lose power, from the button, the supply, a blown fuse or a pulled
cable, the arm goes limp and falls under its own weight, with whatever it carries. The gearing slows the fall of
joints 2 and 3 a little; it does not stop it.

- Never switch the robot off while it is extended or carrying something: bring it to the parked pose first,
  folded in over the base, where it has the least distance to fall ([Switching on and off](https://docs.source-robotics.com/PAROL-docs/1.1/05-operation/switching-on-off/#switching-off)).
- Hold the forearm when you press the power button.
- Keep hands out from under the arm.
- Expect the fall during any power failure, and place nothing fragile under the arm.

## Motion you did not command

- **Homing moves every joint**, at speed, toward its limit switch, as soon as Home is pressed. The arm must be
  free to move and the switches must work ([Homing](https://docs.source-robotics.com/PAROL-docs/1.1/05-operation/homing/)).
- **A program restarts** where you told it to, and `Loop()` restarts it forever.
- **A lost step** makes the arm move to a different place than the one on the screen. After a collision or a
  stall, stop and home again.
- **A wrong joint direction** on a new build sends a joint the wrong way on the first jog, into its stop. Jog
  slowly and briefly the first time ([Firmware and first run](https://docs.source-robotics.com/PAROL-docs/1.1/build/firmware-and-first-run/)).

## Stepper-induced voltage

A stepper motor turned by hand is a generator. Moving the arm quickly while the supply is connected and the
board off can power the board on and energise the motors, with the arm wherever you left it. Move an unpowered
robot slowly, and only toward the parked pose or into its box.

## Hot motors

After hours of motion the wrist motors reach 70 °C ([Currents and temperatures](https://docs.source-robotics.com/PAROL-docs/1.1/03-technical-data/operating-temperatures/)).
That is hot to the touch and close to the limit of the plastic around them.

## Electricity

The robot runs on 24 V, which is safe to touch. The power supply you plug it into is connected to the mains:
use a closed, approved supply, never an open-frame one on the desk. A DIN-rail supply such as the one in the BOM
has open screw terminals: it belongs in a closed box, with an earthed cable, and if you are not sure how to wire
it, an electrician wires it ([The power supply](https://docs.source-robotics.com/PAROL-docs/1.1/04-installation/connecting/#the-power-supply)). The control
board has no reverse-polarity protection on its power input.

## The tool

A pneumatic gripper closes with the force of the compressed air behind it, whatever is between its fingers; the
electric grippers close with up to 80 N. A vacuum gripper drops its load the moment the air stops. Treat the tool
as part of the robot in every rule above.
