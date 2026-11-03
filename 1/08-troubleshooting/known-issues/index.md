# Known issues

The faults in PAROL6's firmware and software that are known and not yet fixed, and what to do until they are. The
pages that describe each part say the same where it matters; this page collects them in one place. Which versions
work together is in [Versions and compatibility](https://docs.source-robotics.com/PAROL-docs/1/appendix/compatibility/).

### Control board firmware

Seen in: release 1.

| | What happens | What to do | More |
|---|---|---|---|
| KI-1 | Enforces the joint limits of the earlier robot model, which differ from those in these pages; a target between the two is accepted. | Keep to the limits in the Joint limits table. | [Joint limits](https://docs.source-robotics.com/PAROL-docs/1/03-technical-data/joint-limits/#limits) |

### Control board test firmware

Seen in: release 1.

| | What happens | What to do | More |
|---|---|---|---|
| KI-8 | Enables all six drivers when it boots and turns every motor slowly, without a command, with no limits and no homing, until the power is switched off; no command stops them. | Run it with the arm free to move or the motors unmounted, never on a robot folded against its stops. | [The test firmware](https://docs.source-robotics.com/PAROL-docs/1/board/09-test-firmware/) |
| KI-9 | Most command names the parser knows (`#STATUS`, `#STEP1` to `#STEP6`, `#FLASH`, `#CAN`) are answered with `Unknown command`: only `#IO`, `#LIMIT`, `#STOP` and `#start` do something. | Use the four commands that work; CAN has its own test program. | [Test firmware commands](https://docs.source-robotics.com/PAROL-docs/1/board/09-test-firmware/#commands) |

### Commander software

Seen in: main branch, 2025-09-23.

| | What happens | What to do | More |
|---|---|---|---|
| KI-2 | Enforces the joint limits of the earlier robot model, and computes with its dimensions (a5 = 176.35 mm, the pneumatic gripper's a6 = 62.8 mm), so its Cartesian positions are off by up to about 0.65 mm. | Keep to the limits in the Joint limits table; teach the poses that need accuracy on the robot. | [Kinematics](https://docs.source-robotics.com/PAROL-docs/1/03-technical-data/kinematics/) |
| KI-3 | `Output(2,HIGH)` and `Output(2,LOW)` are refused by a bug in the program check (`Invalid Output() command`), and the program stops. | Use output 1 in commander programs, or switch output 2 from the Python API. | [RBTscript, I/O](https://docs.source-robotics.com/PAROL-docs/1/programming/03-commander/rbtscript/#io) |
| KI-4 | `SpeedJoint()`, `Input()` and `Home()` pass the program check but have no action: the program stops on that line until you press **Stop**. | Leave them out of programs; home with the **Home** button before you start a program. | [RBTscript, SpeedJoint and SpeedCart](https://docs.source-robotics.com/PAROL-docs/1/programming/03-commander/rbtscript/#speedjoint-speedcart) |
| KI-5 | `SpeedCart()`, `Get_data` and `Timeouts` are in the command menu but fail the program check: a program that contains one is refused. | Leave them out of programs. | [RBTscript, SpeedJoint and SpeedCart](https://docs.source-robotics.com/PAROL-docs/1/programming/03-commander/rbtscript/#speedjoint-speedcart) |
| KI-6 | A move's profile written in quotes (`"trap"`) or as `func=trap` is ignored without a message, and the move gets the default profile. | Write the bare word, `trap` or `poly`, as the last argument. | [RBTscript](https://docs.source-robotics.com/PAROL-docs/1/programming/03-commander/rbtscript/) |
| KI-7 | The Cartesian rotation jog buttons do nothing in the world frame (WRF). | Rotate in the tool frame (TRF), the default. | [The GUI](https://docs.source-robotics.com/PAROL-docs/1/gui/commander/the-gui/) |

### Python API (parol6)

Seen in: 0.9.1.

| | What happens | What to do | More |
|---|---|---|---|
| KI-10 | Enforces the joint limits of the earlier robot model, and computes with its dimensions (a5 = 176.35 mm), so its Cartesian positions are off by up to about 0.65 mm from the model these pages use. | Keep to the limits in the Joint limits table; teach the poses that need accuracy on the robot. | [Kinematics](https://docs.source-robotics.com/PAROL-docs/1/03-technical-data/kinematics/) |

## Something that is not here

Check [By symptom](https://docs.source-robotics.com/PAROL-docs/1/08-troubleshooting/by-symptom/) first. If it is still not explained, [Report a problem](https://docs.source-robotics.com/PAROL-docs/1/support/report-a-problem/)
says what to include so it can be reproduced. A fixed issue stays on this page, under "Fixed", with the version
that fixes it.
