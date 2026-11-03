# Steppers, open loop and backlash

## Actuators

Robots are moved by actuators: servo motors with encoders, stepper motors, brushless motors, pneumatic and
hydraulic cylinders. PAROL6 uses **stepper motors**, which move in discrete steps on command, hold position
with their current, and need no sensor to be positioned: the cheapest way to get six precise axes, and the
reason the robot has no encoders and no brakes.

## How a stepper works

A stepper has 50 pole pairs and two windings; energising the windings in sequence pulls the rotor one step,
1.8°, at a time, 200 steps per turn. The driver can set the currents to intermediate values and hold the rotor
between full steps: **microstepping**, 32 positions per step on PAROL6, 6400 per turn. A microstep is a real
position only while the torque against it is small; under load the rotor lags up to a full step behind the
commanded microstep, which is why the resolution on paper is finer than the accuracy in practice.

A stepper's torque falls as its speed rises, because the windings' inductance limits how fast the current can
reverse. Above a certain speed, at a certain load, it **stalls**: it stops following the steps, buzzes, and the
position is lost. The speed and acceleration limits of the software exist to stay below that.

## Open loop and closed loop

**Open loop**: the controller commands and assumes the result. Simple, cheap, no sensors, and no way to know
when something went wrong. **Closed loop**: a sensor measures the result and the controller corrects the
difference; accurate, robust against load, and more complex. PAROL6's joints are open loop: the step count is
the position, and a lost step is an error nobody sees. The safeguards are the margins in the limits, the homing
that resets the count, and the user's eyes.

The electric grippers are different: their drivers run the motor in closed loop with an encoder, a brushless
motor on the SSG-48's Spectral Micro and a stepper on the MSG's STEPFOC. That is what makes a force-controlled
gripper possible ([End effectors](../end-effectors/index.md)).

## Position, velocity and torque control

A joint can be controlled in **position** (go there and hold), **velocity** (turn at this speed) or **torque**
(push this hard). PAROL6's firmware offers velocity (the jog command) and a velocity-plus-position tracking (the
go-to command); the planner on the PC turns position targets into those. Torque control, which collaborative
robots use to be safe around people, is not possible with open-loop steppers: the robot cannot feel.

## Backlash

The play between gear teeth, in a belt's mesh and in a coupler: when a joint reverses, the motor turns a little
before the output follows. PAROL6's planetary gearboxes have 15 to 20 arc-minutes of it, the belts less. It
shows as a small position error that depends on the direction of the last move, and as a slight looseness at the
tool. The cure is preload (tight belts), approaching a pose always from the same direction, and keeping the
couplers tight ([Couplers and threadlocker](../07-maintenance/couplers.md)).

## Encoders

An encoder measures a shaft's rotation: incremental ones count from a start, absolute ones know the angle at
power-up. PAROL6 has none on its joints; adding them is a common modification, and the community has closed-loop
driver projects. The gripper drivers have an absolute magnetic encoder on their motor.
