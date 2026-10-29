# Planning the cell

A robot cell is the robot, what it works on, and the people around it. For a PAROL6 on a bench the plan fits on
a page, and it is worth writing.

## The person

One person runs the robot and sees all of it. Nobody else reaches into the workspace while it is enabled. The
E-stop is within that person's reach, and so is the power supply's switch.

## The space

- The arm's reach, 400 mm from the axis of joint 1 plus the tool, and a margin for the elbow, which swings
  behind the base when the arm folds: a sphere of about half a metre.
- Nothing fragile inside it, and nothing that the arm could knock onto the floor.
- The cables and tubes outside the sweep, or fixed so the arm cannot catch them.
- For a robot that runs unattended or near others, an enclosure: acrylic panels on the profile frame are enough
  to keep hands out; the robot cannot break them.

## The program

- Run every new program in the simulator first, at full speed, and watch for the arm folding into the base or
  the table.
- Start on the real robot at low speed. The commander's speed slider and the Python API's `speed` fraction scale
  every move.
- Put the first move of a program at a known pose from the standby pose, so that a restart from standby is
  always safe.
- Use `Delay()` and the inputs to wait for the world, rather than assuming it.

## The tool and the parts

- The payload includes the tool. A gripper and a camera together can be most of the 0.5 kg the arm carries at
  full reach.
- A pneumatic gripper needs 6 to 8 bar and a valve wired to an output; the valve's two tubes decide whether it is
  normally open or closed ([Pneumatics](../07-peripherals/pneumatics.md)).
- Fingers that can hold the part also when the power goes: the electric grippers hold their grip when the robot
  is E-stopped, the vacuum gripper does not.

## When something changes

Changing the tool, the base, the table height or the fixture changes the kinematics and the clearances. Update
the tool in the software, check the limits with a slow jog, and run the programs in the simulator again.
