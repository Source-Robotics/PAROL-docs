# Motor GUI

[Motor GUI](https://motorgui.com/) is Source Robotics' browser tool for its motor drivers, and so for the SSG-48
and MSG grippers, whose driver sits inside.

| You need | |
|---|---|
| Nothing to install | It reaches the hardware through the browser's serial port access |
| A Chromium-based browser | |
| The [CANvas USB-to-CAN adapter](https://source-robotics.com/products/canvas-usb-to-can-adapter) | |

## When you need it

On PAROL6 the control board drives the gripper, so Motor GUI is not part of everyday use. It is the tool when you:

| Job | How |
|---|---|
| **Update the gripper's firmware** | Over CAN, from the driver's GitHub releases, through the gripper's bootloader |
| **Set up a self-built gripper**, or restore a gripper's configuration | The setup page has presets for the SSG-48 and for the three MSG steppers. They are applied over UART, with the [USB-to-serial adapter](https://source-robotics.com/products/usb-to-serial-adapter) on the driver's UART port, not over CAN. |
| **Test a gripper off the robot** | Calibrate, open and close it, watch its position and current, run a cycle test, in the gripper panel |

!!! warning "A preset writes CAN ID 6"
    A preset writes CAN ID 6, the PAR6 gripper's: change it to 0 before you apply it for PAROL6.

## Connect the gripper off the robot

The control board polls the gripper continuously while the robot is on, so use Motor GUI with the gripper off the
robot's bus:

1. Put the gripper on the CANvas adapter's CAN terminals.
2. Put it on a 24 V supply.
3. Follow the gripper manual's Motor GUI page:
   [SSG-48](https://docs.source-robotics.com/SSG48-gripper-docs/latest/05-setup/motor-gui/) or
   [MSG](https://docs.source-robotics.com/MSG-gripper-docs/latest/05-setup/motor-gui/).

The firmware update is on their Firmware pages
([SSG-48](https://docs.source-robotics.com/SSG48-gripper-docs/latest/08-firmware/),
[MSG](https://docs.source-robotics.com/MSG-gripper-docs/latest/08-firmware/)).
