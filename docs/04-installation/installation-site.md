# Installation site

What the place where the robot stands needs:

| You need | Why, and what is right |
|---|---|
| **A rigid table or frame** | The arm accelerates its 5.5 kg quickly; a wobbly table shakes and spoils the repeatability. An aluminium profile frame or a solid bench is right. |
| **Clearance** | The arm sweeps round the base, in front and behind it: [Clearance](#clearance), below. |
| **Room temperature, dry, dust-free** | The base draws air through its fan over the stepper drivers. |
| **The E-stop within reach** | Of the person at the PC, and reachable from where someone would stand to load the robot. |
| **Cables routed** | The power, USB and E-stop cables leave the base at the back. Route them so that nothing pulls on them and so that the arm cannot sweep over them. |
| **Pneumatics**, for the pneumatic gripper | A valve and an air supply at 5 to 7 bar near the base. Check your gripper's rating ([Pneumatics](../06-peripherals/pneumatics.md)). |
| **A mains switch within reach** | On the power supply's mains side, a switched socket strip for example: the stop for when the PC software has frozen ([Emergency stop](../02-safety/emergency-stop.md)). |

## Clearance

The flange reaches 408 mm from the axis of joint 1 in front of the base and 359 mm behind it, plus the tool. The
elbow swings behind the base when the arm folds ([Workspace](../03-technical-data/kinematics.md#workspace)).

![Where the pneumatic gripper's TCP can go, side and top view, in mm; the arm, the tool and the part need more room than this](../assets/figures/parol6_workspace_pneumatic.webp#only-light){ width="620" }
![Where the pneumatic gripper's TCP can go, side and top view, in mm; the arm, the tool and the part need more room than this](../assets/figures/parol6_workspace_pneumatic_dark.webp#only-dark){ width="620" }

Keep a free sphere around the base, with nothing fragile in it:

| Tool | Free sphere around the base |
|---|---|
| The pneumatic gripper | About 500 mm |
| The SSG-48 or the MSG | About 600 mm |

The simulator shows the sweep of a program before the robot runs it.

## Safety

The [Planning the cell](../02-safety/planning-the-cell.md) page covers the safety side: who can reach the robot,
guarding, and what the software can and cannot stop.
