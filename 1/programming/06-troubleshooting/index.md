# 6. Troubleshooting

## The Python API

| Symptom | Cause | Remedy |
|---|---|---|
| `ping()` returns `None` | No controller, wrong host or port, a firewall | Start `parol6-server`; check `--host`/`--port`; allow UDP 5001 |
| `ping()` says `hardware_connected=False` | No serial port given, or it failed to open | `--serial COM5`, or `connect_hardware("COM5")`; check the port is free |
| No status in `stream_status()` | Multicast blocked, or a different group | `PAROL6_STATUS_TRANSPORT=UNICAST` with `PAROL6_STATUS_UNICAST_HOST`; check `PAROL6_MCAST_IF` |
| `MotionError: MOTN_NOT_HOMED` | The robot is not referenced | `home(wait=True)` |
| `MotionError: SYS_ESTOP_ACTIVE` | The E-stop is pressed or a protective stop is latched | Release the button; `reset()` |
| `IK_TARGET_UNREACHABLE` on a pose that looks fine | Numerical IK, often around joint 4 | Change the orientation slightly; start from another posture; a joint move first |
| `COMM_VALIDATION_ERROR` or decode errors | Client and controller of different versions | The same version on both sides |
| `TimeoutError` on a blocking move | The move did not complete in `timeout` | Longer `timeout`; `stop()` to cancel the queued move |
| `loop overbudget by +N%` in the log | The PC cannot keep 100 Hz | Lower `PAROL6_CONTROL_RATE_HZ`; no DEBUG or TRACE logging; close other programs |
| Jittery motion | The same, or a long serial cable | As above; a short shielded USB cable |
| Motion refused with `SYS_SELF_COLLISION` where there is nothing | A declared shape, a held object, the tool's mesh | `shapes()`; the tool's variant; `PAROL6_COLLISION_CHECK=0` to confirm, then fix the world |
| A tool `move` fails with `MOTN_GRIPPER_*` | Not calibrated; no gripper answering on CAN | `tool.calibrate()`; the gripper's cable and manual |

## The commander software

| Symptom | Cause | Remedy |
|---|---|---|
| Connect does nothing | Wrong port; the port in use; Linux permissions | Try again; `COMx`/`ttyACMx`; `chmod 666` |
| The simulator shows a different pose | Not homed | Home |
| A command in the program does nothing | A typo in the name or the argument order; `End()` before it | The response log; the exact syntax on [RBTscript](https://docs.source-robotics.com/PAROL-docs/1/programming/03-commander/rbtscript/) |
| `MoveCart` stops half way | A singularity | A joint move, or another orientation |
| `Gripper()` does nothing | Not calibrated; an error latched; a value out of range | Gripper tab: **Clear gripper error**, then **Calibrate gripper**; whole numbers, current 150 to 1000 mA |
| The program runs once and stops | No `Loop()` | Add it, or `End()` is where you want it |
| Import errors at start | Wrong Python or package versions | Python 3.10 or 3.11 and the pinned versions, in the commander's own virtual environment, activated ([Installation](https://docs.source-robotics.com/PAROL-docs/1/gui/commander/installation/)) |
| `Time between 2 commands` far above 0.010 (seconds, despite the label) | The PC | [Communication](https://docs.source-robotics.com/PAROL-docs/1/08-troubleshooting/communication/) |

## Both

The control board answers in text when you expected packets: it runs the test firmware; upload the main one
([Firmware](https://docs.source-robotics.com/PAROL-docs/1/board/08-firmware/)). Two programs cannot share the port ([Control ownership](https://docs.source-robotics.com/PAROL-docs/1/theory/control-ownership/)).
