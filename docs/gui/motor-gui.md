# Motor GUI

[Motor GUI](https://motorgui.com/) is Source Robotics' browser tool for its motor drivers, and so for the SSG-48
and MSG grippers, whose driver sits inside. It reaches the hardware through the browser's serial port access:
nothing to install, a Chromium-based browser and the
[CANvas USB-to-CAN adapter](https://source-robotics.com/products/canvas-usb-to-can-adapter).

On PAROL6 the control board drives the gripper, so Motor GUI is not part of everyday use. It is the tool when
you:

- **update the gripper's firmware**, over CAN, from the driver's GitHub releases, through the gripper's
  bootloader;
- **set up a self-built gripper**, or restore a gripper's configuration: the setup page has presets for the SSG-48
  and for the three MSG steppers;
- **test a gripper off the robot**: calibrate, open and close it, watch its position and current, run a cycle
  test, in the gripper panel.

The control board polls the gripper continuously while the robot is on, so use Motor GUI with the gripper off
the robot's bus: the gripper on the CANvas adapter's CAN terminals and on a 24 V supply. Then follow the gripper
manual's Motor GUI page, [SSG-48](https://docs.source-robotics.com/SSG48-gripper-docs/latest/05-setup/motor-gui/)
or [MSG](https://docs.source-robotics.com/MSG-gripper-docs/latest/05-setup/motor-gui/); the firmware update is
on their Firmware pages ([SSG-48](https://docs.source-robotics.com/SSG48-gripper-docs/latest/08-firmware/),
[MSG](https://docs.source-robotics.com/MSG-gripper-docs/latest/08-firmware/)).
