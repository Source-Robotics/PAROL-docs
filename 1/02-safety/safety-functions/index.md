# What the robot protects against, and what not

Know what the hardware and the software catch, and what they do not, before you decide how the robot is guarded.

## What is protected

| Against | How | Where |
|---|---|---|
| A target outside the joint limits | The planner refuses it; a jog stops at the limit. Firmware 1, the commander and the Python API check the earlier, partly wider limits ([Joint limits](https://docs.source-robotics.com/PAROL-docs/1/03-technical-data/joint-limits/#limits)) | Commander, Python API |
| A speed or acceleration above the limits | Clamped to the robot model's limits | Commander, Python API |
| A move through a singularity (Cartesian) | The commander stops the move; the API's IK fails and refuses the command | Commander, Python API |
| A pose the arm cannot reach | The IK fails and the command is refused | Commander, Python API |
| Self-collision and collision with declared obstacles | Collision checking of planned moves and jogs against the robot's meshes and your keep-out shapes | Python API ([set_shapes](https://docs.source-robotics.com/PAROL-docs/1/reference/python/configuration/)) |
| The E-stop pressed | Reported by the board, acted on by the PC software ([Emergency stop](https://docs.source-robotics.com/PAROL-docs/1/02-safety/emergency-stop/)) | Commander, Python API |
| A driver overheating | The TMC5160 shuts its outputs down when it gets too hot; the fan keeps it far below that. The joint then goes limp, and firmware 1 does not tell the PC | Control board |
| A short on a motor output | The TMC5160 switches the output off. Firmware 1 reads the driver's short and open-load flags once at start-up and does not report them | Control board |

## What is not protected

| Not against | Why | What you do instead |
|---|---|---|
| **A collision with something the software does not know** | There are no joint encoders and no force sensing: the stepper pushes until it stalls, then loses steps silently | Keep the workspace clear; check programs in the simulator first; declare obstacles to the Python API's collision checker |
| **Lost steps** | Open-loop motors; the position is counted, not measured | After a stall or a collision, home again; keep speeds and payloads within the limits |
| **A fall on power loss** | No brakes | Switch off only in the parked pose; keep hands and objects out from under the arm |
| **A frozen PC** | The E-stop acts through the PC software; the firmware does not stop on its own | A mains switch on the power supply within reach |
| **Lost communication with the PC** | The firmware has no timeout: it keeps executing the last packet until the next one arrives. After a move to a position (programs, the Python API) the joint stops near that target. After a jog in the commander the joint keeps turning at the jog speed until it reaches its blocker | Keep the mains switch within reach; a short, direct USB cable |
| **Motor temperature** | Only the drivers are measured, not the motors | Reduce the current for long runs ([Currents and temperatures](https://docs.source-robotics.com/PAROL-docs/1/03-technical-data/operating-temperatures/)) |
| **The tool** | The robot does not know what the tool does | Guard the tool as you would the robot |
| **A wrong joint direction on a new build** | The firmware trusts its configuration | Jog each joint briefly before homing |

The commander's safety functions are described in [Errors and recovery](https://docs.source-robotics.com/PAROL-docs/1/05-operation/errors-and-recovery/);
the Python API's in [Errors](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/errors/).
