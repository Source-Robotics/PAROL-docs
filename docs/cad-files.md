# Downloads and files

Everything to download for PAROL6, at the versions these pages describe. The versions come from one file,
`versions.yml`, so this page changes with them; which versions work together is in
[Versions and compatibility](appendix/compatibility.md).

## Firmware and software

| What | Version | Download | How to install |
|---|---|---|---|
| Control board firmware, a PlatformIO project | <!-- version-link: firmware --> | [PAROL6 control board main software](<!-- version-url: firmware -->/PAROL6%20control%20board%20main%20software) | [Firmware](board/08-firmware.md) |
| Control board test firmware, and the CAN test | the same release | [PAROL6 control board test code](<!-- version-url: firmware -->/PAROL6%20control%20board%20test%20code) | [The test firmware](board/09-test-firmware.md) |
| ST-Link USB driver, for uploading from Windows | | [STSW-LINK009](https://www.st.com/en/development-tools/stsw-link009.html) | [Firmware: tools](board/08-firmware.md#tools) |
| Python API (`parol6`) | <!-- version-link: software.python_api --> | [PAROL6-python-API](https://github.com/PCrnjak/PAROL6-python-API) | [Installation](programming/02-python-api/installation.md) |
| Commander software | <!-- version-link: software.commander --> | [PAROL-commander-software](https://github.com/Source-Robotics/PAROL-commander-software) | [Installation](gui/commander/installation.md) |
| Robot model: URDF and MuJoCo, with the meshes and every tool | <!-- version-link: models.robot_descriptions --> | [robot_descriptions: PAROL6](<!-- version-url: models.robot_descriptions -->/guides/parol6.md) | |
| ROS 2 MoveIt configuration | main branch | [PAROL6-ROS2-MOVEIT](https://github.com/Source-Robotics/PAROL6-ROS2-MOVEIT) | [ROS 2](programming/04-ros2.md) |

The version links open the files at exactly that release. The commander software has no releases: its main
branch, as of the date given, is the one these pages describe. Known faults in each are on
[Known issues](08-troubleshooting/known-issues.md).

## CAD and build files

The latest files, on the main branch of the
[robot repository](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm).

| What | Where |
|---|---|
| Printable parts (STL), by link, with the small print bed variants | [STL](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL) |
| Mounting plates (STEP) | [STL/mounting plates](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL/mounting%20plates) |
| Bill of materials with purchase links and reference images | [BOM](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/BOM), and on this site: [Bill of materials](build/bill-of-materials.md) |
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
