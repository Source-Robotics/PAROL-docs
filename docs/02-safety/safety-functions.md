# What the robot protects against, and what not

Know what the hardware and the software catch, and what they do not, before you decide how the robot is guarded.

## What is protected

| Against | How | Where |
|---|---|---|
| A target outside the joint limits | The planner refuses it; a jog stops at the limit | Commander, Python API |
| A speed or acceleration above the limits | Clamped to the robot model's limits | Commander, Python API |
| A move through a singularity (Cartesian) | The commander stops the move; the API's IK fails and refuses the command | Commander, Python API |
| A pose the arm cannot reach | The IK fails and the command is refused | Commander, Python API |
| Self-collision and collision with declared obstacles | Collision checking of planned moves and jogs against the robot's meshes and your keep-out shapes | Python API ([set_shapes](../reference/python/configuration.md)) |
| The E-stop pressed | Reported by the board, acted on by the PC software ([Emergency stop](emergency-stop.md)) | Commander, Python API |
| A driver overheating | The TMC5160 driver warns at 100 °C and shuts down at 120 °C; the fan keeps it far below | Control board |
| A short or an open motor winding | The driver detects it at start-up | Control board |
| Lost communication with the PC | The firmware runs the last commanded speeds until the next packet; the Python API's controller stops streaming when targets stop | Firmware, Python API |

## What is not protected

| Not against | Why | What you do instead |
|---|---|---|
| **A collision with something the software does not know** | There are no joint encoders and no force sensing: the stepper pushes until it stalls, then loses steps silently | Keep the workspace clear; check programs in the simulator first; declare obstacles to the Python API's collision checker |
| **Lost steps** | Open-loop motors; the position is counted, not measured | After a stall or a collision, home again; keep speeds and payloads within the limits |
| **A fall on power loss** | No brakes | Switch off only in the standby pose; keep hands and objects out from under the arm |
| **A frozen PC** | The E-stop acts through the PC software; the firmware does not stop on its own | A mains switch on the power supply within reach |
| **Motor temperature** | Only the drivers are measured, not the motors | Reduce the current for long runs ([Currents and temperatures](../03-technical-data/operating-temperatures.md)) |
| **The tool** | The robot does not know what the tool does | Guard the tool as you would the robot |
| **A wrong joint direction on a new build** | The firmware trusts its configuration | Jog each joint briefly before homing |

The commander's safety functions are described in [Errors and recovery](../05-operation/errors-and-recovery.md);
the Python API's in [Errors](../programming/03-python-api/errors.md).
