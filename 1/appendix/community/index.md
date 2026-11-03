# Community projects

Software, hardware modifications and experiments built around PAROL6 by its community. They are third-party
projects, not maintained by Source Robotics: use them at your own risk and check each one's licence and
documentation. The list is kept in the robot repository's
[community_projects.md](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/main/community_projects.md),
where a pull request adds yours.

## Control software and GUIs

| Project | What it is |
|---|---|
| [Waldo Commander](https://github.com/Jepson2k/Waldo-Commander) | A browser-based commander: Python programs with an editor and debugger, 3D simulation, teach by demonstration, and an MCP server so that an LLM can drive the arm. Built on the Python API through the waldoctl abstraction |
| [Parol6_Better_Command](https://github.com/thousands-star/Parol6_Better_Command) | The commander software refactored for easier editing, with vision |
| [PAROL6 Pilot](https://github.com/jointAxis77/pilot) | A web GUI |
| [PAROL6_GUI](https://github.com/jakubgrzebien1234-creator/PAROL6_GUI) | An alternative desktop GUI |
| [parol6_commander](https://github.com/Lyczko0/parol6_commander) | A web GUI on NiceGUI, ROS 2 and MoveIt 2, for calibrating, jogging and programming |
| [Parol6-firmware](https://github.com/Lyczko0/Parol6-firmware) | Alternative motion firmware for a Teensy 4.1 with ROS 2 over micro-ROS |
| [parol6_ros2_control](https://github.com/grahas/parol6_ros2_control) | The `ros2_control` hardware interface and bridge used by the MoveIt configuration's real-robot launch |

## Vision and AI

| Project | What it is |
|---|---|
| [PAROL6-Python-API-Gemini-Vision](https://github.com/AlvarEhr/PAROL6-Python-API-Gemini-Vision-Public) | Controlling PAROL6 with the Gemini LLM and a camera |
| [Tic-Tac-Toe-Robot-Project-Parol6](https://github.com/lennardkiebler-cryptoii/Tic-Tac-Toe-Robot-Project-Parol6) | A vision-guided tic-tac-toe player |

## Hardware

| Project | What it is |
|---|---|
| [parol6-printed-eg17](https://github.com/Pixelgamer4k/parol6-printed-eg17) | A printed gearbox alternative |

## The legacy Python API

[PAROL6-python-API-Alvar](https://github.com/PCrnjak/PAROL6-python-API-Alvar) is the first Python API, a
headless commander with a text-over-UDP client, kept as it is for the projects built on it. New work should use
the [current Python API](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/).
