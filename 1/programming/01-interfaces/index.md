# 1. The interfaces at a glance

Every way of programming PAROL6 ends at the same place: a packet to the control board every 10 ms with the
joint speeds and positions to execute. What differs is who computes those packets and how you tell it what you
want.

| | Commander software | Python API | ROS 2 + MoveIt | Waldo Commander (community) |
|---|---|---|---|---|
| What it is | A desktop GUI with a simulator and a program editor | A controller process and a Python client library | A MoveIt configuration and a `ros2_control` interface on top of the Python API's controller | A browser GUI on top of the Python API, with an MCP server for LLMs |
| You write | RBTscript, one command per line | Python | ROS 2 nodes, MoveIt plans | Python, in the browser, or prompts |
| Motion | Joint and Cartesian moves, trapezoidal or quintic profiles, teach by jogging | Planned moves (joint, linear, circular, spline, process), streamed jogs and servo targets, blending, five profiles, collision checking | MoveIt planning | What the API offers, plus teach by demonstration |
| Tools | SSG-48 and MSG gripper tab, outputs | Registered tools with variants, TCP transforms, tool actions in the motion queue | Through the bridge | Through the API |
| Simulator | 3D window, needs the robot connected | Simulator mode and a dry-run client, no robot needed | RViz | 3D preview, no robot needed |
| Runs on | The PC at the robot | The controller at the robot; clients anywhere on the network | Ubuntu 22.04 with ROS 2 Humble | Any browser; the server at the robot |
| Python | 3.10 or 3.11 | 3.11 to 3.14 | | 3.11 or newer |
| Maturity | Stable, no releases, main branch | Pre-1.0, released often, interfaces can change between minors | Demo and real-robot launch files | Community project |
| Best for | The first day; teaching points; demos; simple sequences | Everything else | ROS users | Remote use; AI-driven control |

## Which one

- **You have never run the robot**: the commander software. The GUI shows the robot, the jog buttons check the
  wiring, and a three-line program is a minute's work.
- **You want to write programs**: the Python API. Its controller runs the robot; your script, or several, talk
  to it; the dry-run client tests the script without a robot.
- **You have a ROS 2 stack**: the MoveIt configuration, with the Python API's controller underneath.
- **You want to drive the arm from a browser or an LLM**: Waldo Commander, a community project on the API.

## What they share

- The [serial protocol](https://docs.source-robotics.com/PAROL-docs/1/board/10-serial-protocol/) to the control board, at 100 Hz.
- The robot model: the joint limits, the gear ratios, the standby pose, the kinematics
  ([Theory corner](https://docs.source-robotics.com/PAROL-docs/1/theory/)).
- The rule that **one program owns the board**: the commander and the API's controller cannot be connected at
  the same time ([Control ownership](https://docs.source-robotics.com/PAROL-docs/1/theory/control-ownership/)).
- Homing after every power-up, and the E-stop handled by the PC software ([Emergency stop](https://docs.source-robotics.com/PAROL-docs/1/02-safety/emergency-stop/)).

## What they do not share

Poses and programs do not transfer between the commander and the API without care: the commander's kinematic
model assumes the pneumatic gripper, the API's assumes the tool you select, and the two have different speed
limits and profiles. A pose taught in one is a starting point in the other, not a result.
