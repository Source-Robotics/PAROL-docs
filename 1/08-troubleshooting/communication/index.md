# Communication

## The serial port

The control board appears on the PC as a serial port over USB: `COMx` on Windows, `/dev/ttyACMx` on Linux and
`/dev/cu.usbmodem…` on macOS. The commander takes `COM5` or `ttyACM0` in its connection field; the Python API's controller takes
`--serial COM5` or `--serial /dev/ttyACM0`, or finds the port from `PAROL6_COM_PORT`.

- **Windows**: Device Manager, Ports, shows the number. If the board is missing, try another cable or port; the
  board enumerates only when it has power.
- **Linux**: `ls /dev/ttyACM*`. Permission denied: `sudo chmod 666 /dev/ttyACM0`, or add yourself to the
  `dialout` group and log in again.
- **Connect fails the first time** in the commander: press Connect again; two or three tries are normal.
- **The port is busy**: another program has it, often a previous instance of the controller.

## The test firmware answers, the main firmware does not

A board from the shop carries the test firmware, which talks in text. Upload the main firmware ([Firmware](https://docs.source-robotics.com/PAROL-docs/1/board/08-firmware/)).

## The 100 Hz loop

The PC must send a packet every 10 ms. The commander prints `Time between 2 commands in ms` in its terminal
output; it should sit near 0.010. The number is in seconds, despite the label: 0.010 is 10 ms. If it is often
higher, the robot stutters and the position tracking suffers.

- Close browsers and other heavy programs; disable power saving on the USB port and the CPU.
- A faster PC: six cores from 2017 or newer ([What you need](https://docs.source-robotics.com/PAROL-docs/1/01-overview/what-you-need/#the-pc)).
- The Python API's controller logs `loop overbudget by +N%` when its loop runs late, and shows the figures in
  `loop_stats()`; it also accepts a lower `PAROL6_CONTROL_RATE_HZ`, at the cost of smoothness, and runs worse
  with TRACE or DEBUG logging on.

## The connection drops

A USB cable without ferrite near the motors, a hub, or a long cable: use a short, shielded cable straight into
the PC. When packets stop, the firmware keeps executing the last one: after a move to a position the joints stop
near that target and hold, but a joint that was jogging in the commander keeps turning until it reaches its
blocker. Keep the mains switch of the power supply within reach ([Emergency stop](https://docs.source-robotics.com/PAROL-docs/1/02-safety/emergency-stop/)).
