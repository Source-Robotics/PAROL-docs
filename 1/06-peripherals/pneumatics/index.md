# Pneumatics

Two 4 mm tubes run inside the arm from the push-in fittings at the base to the forearm, where the pneumatic or
vacuum gripper connects. A 5/2 solenoid valve at the base, driven by an output, switches the air.

## Pressure

5 to 7 bar; check your gripper's rating, and stay below the lowest rating of the gripper, the valve and the
fittings. The tubes and fittings are standard 4 mm pneumatic parts.

## The valve

A 5/2 valve, 24 V coil, 4 mm ports: one port from the compressor, two to the base fittings, the exhausts open.
The coil goes between **GND_SEL** and **OUTPUT1** ([Inputs and outputs](https://docs.source-robotics.com/PAROL-docs/1/06-peripherals/io/)). Which of the two outputs is
pressurised when the coil is off decides whether the gripper is normally open or normally closed: swap the two
tubes to change it.

![Valve, tubes and gripper](../assets/pneumatic connection_edit.webp){ width="700" }

## Routing

The arm's tubes run inside it from the base to the push-in fittings on the forearm; they are one reason for the
one-turn rule of the joints. From the forearm fittings, the gripper's own tubes cross joints 5 and 6 outside the
arm, like an electric gripper's cable: give them enough slack for the range you use, since they, not the flange,
limit joint 6. Outside the base, give the tubes a loop so the arm cannot pull them.

## A vacuum gripper

Needs one line only: block the valve's second port ([Vacuum gripper](https://docs.source-robotics.com/PAROL-docs/1/end-effectors/vacuum-gripper/)).

In the Python API, a pneumatic or vacuum tool's `open()` switches output 1 high and `close()` switches it low,
whatever the tubing does: lay the tubes so the two match ([Pneumatic gripper](https://docs.source-robotics.com/PAROL-docs/1/end-effectors/pneumatic-gripper/)).
