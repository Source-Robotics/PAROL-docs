# PAROL6 End Effectors Guide

![The MSG gripper on PAROL6](https://docs.source-robotics.com/PAROL-docs/1.1/assets/MSG_and_camera.webp)

<div class="doc-meta" markdown>

**Document number:** SR-3004

**PAROL6 release:** 1.1

**Python API (parol6):** v0.9.1

**PAROL6 commander software:** main

**Revision:** 2026.B

**Published:** 2026-11-05

**Applies to:** PAROL6 release 1.1, Python API (parol6) v0.9.1, PAROL6 commander software main

*Original instructions*

</div>

What goes on PAROL6's flange and how to set it up: the pneumatic and vacuum grippers from the robot's own files,
Source Robotics' SSG-48 and MSG electric grippers, and a tool of your own. Each page says how the end effector
mounts, how it connects, what to tell the firmware and the software, and how the commander software and the
Python API drive it. The electric grippers have manuals of their own; here is only what is PAROL6-specific.

| End effector | Driven by | Mounts with | Commander | Python API | Manual |
|---|---|---|---|---|---|
| [Pneumatic gripper](https://docs.source-robotics.com/PAROL-docs/1.1/end-effectors/pneumatic-gripper/), SMC MHZ2-16D | a 5/2 valve on OUTPUT1, 5 to 7 bar | a printed holder on the joint 6 shaft coupler | `Output(1,HIGH)`, `Output(1,LOW)` | `select_tool("PNEUMATIC")` | this guide |
| [Vacuum gripper](https://docs.source-robotics.com/PAROL-docs/1.1/end-effectors/vacuum-gripper/) | the same valve and an ejector | a printed holder | `Output(1,HIGH)`, `Output(1,LOW)` | `select_tool("VACUUM")` | this guide |
| [SSG-48](https://docs.source-robotics.com/PAROL-docs/1.1/end-effectors/ssg-48/) adaptive electric gripper | CAN and 24 V through the M8 connector | `coupler_connector_PAROL6` | the Gripper tab, `Gripper()` | `select_tool("SSG-48")` | [SSG-48 manual](https://docs.source-robotics.com/SSG48-gripper-docs/) |
| [MSG](https://docs.source-robotics.com/PAROL-docs/1.1/end-effectors/msg/) compliant AI stepper gripper | CAN and 24 V through the M8 connector | `ring_cover-PAROL6` | the Gripper tab, `Gripper()` | `select_tool("MSG")` | [MSG manual](https://docs.source-robotics.com/MSG-gripper-docs/) |
| [Your own tool](https://docs.source-robotics.com/PAROL-docs/1.1/end-effectors/custom-tools/) | 24 V and CAN, two air lines, two inputs and two outputs | the shaft coupler, or the coupler template | `Output(1,HIGH)`, `Output(1,LOW)`; the inputs in the IO tab | `set_tcp_offset()`, a `ToolConfig` | this guide |

## In this guide

- [The flange](https://docs.source-robotics.com/PAROL-docs/1.1/end-effectors/flange/): the 8 mm shaft of joint 6, the connections at the forearm, the payload, the tool in
  the software
- [Pneumatic gripper](https://docs.source-robotics.com/PAROL-docs/1.1/end-effectors/pneumatic-gripper/)
- [Vacuum gripper](https://docs.source-robotics.com/PAROL-docs/1.1/end-effectors/vacuum-gripper/)
- [SSG-48](https://docs.source-robotics.com/PAROL-docs/1.1/end-effectors/ssg-48/)
- [MSG](https://docs.source-robotics.com/PAROL-docs/1.1/end-effectors/msg/)
- [Your own tool](https://docs.source-robotics.com/PAROL-docs/1.1/end-effectors/custom-tools/)

Get the robot working before you attach a gripper: troubleshooting both at once is hard.
