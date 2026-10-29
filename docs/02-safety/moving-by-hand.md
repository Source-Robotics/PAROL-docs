# Moving the robot by hand

An unpowered PAROL6 can be moved by hand: the joints turn against the friction of their gearboxes and belts, and
the arm has no brakes to release. This is how you pose it for packing and how you lift it. Two rules:

!!! danger "Never more than one turn"
    **Joint 5** must never be turned more than one rotation, and **joint 6** and **joint 1** must never be spun a
    full turn. Cables and pneumatic tubes run through them: a second turn wraps and tears them. Joint 1 has
    printed blockers that stop it; if your build has none, the rule is yours to keep.

![The range of joint 5](../assets/Limits_j5.png){ width="700" }

!!! danger "Not while the supply is connected"
    A stepper turned by hand generates voltage, and a quick move can switch the board on with the arm in your
    hands. Unplug the power supply, or move slowly, and only to the standby pose.

## When the robot is powered

Do not force a powered joint. The motor holds it with its full holding current; what gives is a belt, a set
screw or a printed part, and afterwards the position the software reports is wrong. To move a powered robot,
jog it.

## After moving by hand

The robot does not know it was moved: the firmware counts steps and sees none. **Home again** before any program
or Cartesian move. The commander's position display and the simulator are wrong until you do.

## Lifting

Bring joints 2 and 3 toward their limit switches so that the arm folds over the base, then lift by the base, not
by the arm. [Transport, storage and disposal](../10-transport.md) has the packing.
