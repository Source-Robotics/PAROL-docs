# 5. Other interfaces

## Waldo Commander (web)

A community browser interface on the Python API, with a simulator, programs in the browser, teaching by
demonstration and an MCP server for LLMs: [Waldo Commander](../gui/waldo-commander.md) in the GUI Guide.

## The serial protocol directly

Anything that frames the packets of [the serial protocol](../board/10-serial-protocol.md) and keeps the 100 Hz
cadence can drive the control board from any language. The Python API's serial transport and the commander's
`Serial_sender_good_latest.py` are the two reference implementations.

## The legacy Python API

[PAROL6-python-API-Alvar](https://github.com/PCrnjak/PAROL6-python-API-Alvar) was the first Python API: a
headless commander (`headless_commander.py`) on the PC at the robot, listening for text commands over UDP on
port 5001, and a thin client (`robot_api.py`) with functions like `move_robot_joints`, `move_robot_pose`,
`control_electric_gripper`. It is frozen and kept for the projects built on it, including the Gemini vision
demo. New work belongs on the current API.

## AI agents

The current API's typed client, its dry-run preview and the MCP server in Waldo Commander are the paths for
LLM-driven control: an agent writes Python against the client, previews it dry, and runs it with a human at the
E-stop. The community list has examples ([Community projects](../appendix/community.md)).
