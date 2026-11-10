# Quick start

From an assembled PAROL6 to a robot that is homed and moves on command, in four parts.

!!! danger "Read first"
    PAROL6 has no brakes: when the power goes, the arm falls. It has pinch points, it moves fast, and it moves by
    itself while homing. Anchor it to the table, keep the E-stop within reach, keep hands out of the arm's path, and
    read the [Safety](../02-safety/index.md) chapter: it is five minutes long.

## Before you start

Your robot is assembled and wired as in the [Build guide](../build/index.md)
([Mechanical assembly](../build/mechanical-assembly.md), [Electronics and wiring](../build/electronics-and-wiring.md)).

Nothing else is assumed. You need no firmware on the board, no software on your PC, and no experience with Python
or a terminal.

## The four parts

| Part | What you do | What you end with |
|---|---|---|
| [1. Install the software](1-software.md) | Put Python, Git and the robot software on your PC | A PC that is ready for the robot |
| [2. Upload the firmware](2-firmware.md) | Put the main firmware on the control board, once | A board that can run the robot |
| [3. Connect and switch on](3-connect.md) | Anchor the robot, connect it, switch it on and start the software | A robot that is on and talks to your PC |
| [4. First moves](4-first-moves.md) | Jog each joint, home the robot, run a first program, switch off | A homed robot that moves on command |

Each step links the page that explains it. Follow the link when a step is not clear or something fails.

## What you need

| You need | Notes |
|---|---|
| **Your PAROL6** | Assembled and wired, with the control board inside the base. See the [Build guide](../build/index.md). The parts are in the [BOM](../build/bill-of-materials.md), or come as kits from [the shop](https://source-robotics.com/). |
| **A 24 V power supply, 5 A** | The [BOM](../build/bill-of-materials.md) names one. Any 24 V 5 A supply works. A closed one with a mains cable needs no mains wiring ([The power supply](../04-installation/connecting.md#the-power-supply)). |
| **A mains switch within reach** | On the supply's mains side. A switched socket strip will do. It is the stop that still works when the PC software has frozen ([Emergency stop](../02-safety/emergency-stop.md)). |
| **An E-stop** | A normally closed button in its printed box. The [BOM](../build/bill-of-materials.md) names one. Any NC switch works. |
| **A USB cable** | Type B, to the PC. |
| **An ST-Link programmer and the programming adapter** | To upload the firmware once. The [programming adapter](https://source-robotics.com/products/parol6-programming-adapter) is in the shop. |
| **A PC** | Windows, Linux or macOS. See the [minimum PC](../01-overview/what-you-need.md#the-pc). |

More: [What you need](../01-overview/what-you-need.md).

[Start: 1. Install the software :material-arrow-right:](1-software.md){ .md-button .md-button--primary }
