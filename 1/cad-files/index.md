# Downloads and files

Everything to download for PAROL6, at the versions these pages describe. The versions come from one file,
`versions.yml`, so this page changes with them; which versions work together is in
[Versions and compatibility](https://docs.source-robotics.com/PAROL-docs/1/appendix/compatibility/).

## Firmware and software

| What | Version | Download | How to install |
|---|---|---|---|
| Control board firmware, a PlatformIO project | [V1](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/V1) | [PAROL6 control board main software](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/V1/PAROL6%20control%20board%20main%20software) | [Firmware](https://docs.source-robotics.com/PAROL-docs/1/board/08-firmware/) |
| Control board test firmware, and the CAN test | the same release | [PAROL6 control board test code](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/V1/PAROL6%20control%20board%20test%20code) | [The test firmware](https://docs.source-robotics.com/PAROL-docs/1/board/09-test-firmware/) |
| ST-Link USB driver, for uploading from Windows | | [STSW-LINK009](https://www.st.com/en/development-tools/stsw-link009.html) | [Firmware: tools](https://docs.source-robotics.com/PAROL-docs/1/board/08-firmware/#tools) |
| Python API (`parol6`) | [0.9.1](https://github.com/PCrnjak/PAROL6-python-API/tree/v0.9.1) (2026-10-03) | [PAROL6-python-API](https://github.com/PCrnjak/PAROL6-python-API) | [Installation](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/installation/) |
| Commander software | [main](https://github.com/Source-Robotics/PAROL-commander-software/tree/main) (2025-09-23) | [PAROL-commander-software](https://github.com/Source-Robotics/PAROL-commander-software) | [Installation](https://docs.source-robotics.com/PAROL-docs/1/gui/commander/installation/) |
| Robot model: URDF and MuJoCo, with the meshes and every tool | [2.15.1](https://github.com/Source-Robotics/robot_descriptions/tree/v2.15.1) | [robot_descriptions: PAROL6](https://github.com/Source-Robotics/robot_descriptions/tree/v2.15.1/guides/parol6.md) | |
| ROS 2 MoveIt configuration | main branch | [PAROL6-ROS2-MOVEIT](https://github.com/Source-Robotics/PAROL6-ROS2-MOVEIT) | [ROS 2](https://docs.source-robotics.com/PAROL-docs/1/programming/04-ros2/) |

The version links open the files at exactly that release. The commander software has no releases: its main
branch, as of the date given, is the one these pages describe. Known faults in each are on
[Known issues](https://docs.source-robotics.com/PAROL-docs/1/08-troubleshooting/known-issues/).

## CAD and build files

The latest files, on the main branch of the
[robot repository](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm).

| What | Where |
|---|---|
| Printable parts (STL), by link, with the small print bed variants | [STL](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL) |
| Mounting plates (STEP) | [STL/mounting plates](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL/mounting%20plates) |
| Bill of materials with purchase links and reference images | [BOM](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/BOM), and on this site: [Bill of materials](https://docs.source-robotics.com/PAROL-docs/1/build/bill-of-materials/) |
| Building instructions (PDF), small print bed modification, PETG notes | [Building instructions](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/Building%20instructions) |
| Print settings table | [Print table](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/Print%20table) |
| Assembly and setup videos | [YouTube playlist](https://www.youtube.com/playlist?list=PLSueoDrBt5MMTL9O8qAWZiJrNIf8-29Qz) |

## More

| What | Where |
|---|---|
| Safety warning and disclaimer | [SAFETY_WARNING_AND_DISCLAIMER.md](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/main/SAFETY_WARNING_AND_DISCLAIMER.md) |
| Community projects | [community_projects.md](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/main/community_projects.md) |
| Gripper documentation | [SSG-48](https://docs.source-robotics.com/SSG48-gripper-docs/), [MSG](https://docs.source-robotics.com/MSG-gripper-docs/) |
| This documentation | [PAROL-docs](https://github.com/Source-Robotics/PAROL-docs) |
| Shop | [source-robotics.com](https://source-robotics.com/) |
| Community | [Discord](https://discord.gg/prjUvjmGpZ), [Hackaday](https://hackaday.io/project/191860-parol6-desktop-robotic-arm), [blog](https://source-robotics.com/blogs/blog) |
