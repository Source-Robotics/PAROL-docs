# 4. ROS 2 and MoveIt

[PAROL6-ROS2-MOVEIT](https://github.com/Source-Robotics/PAROL6-ROS2-MOVEIT) is a MoveIt 2 configuration for
PAROL6 with the URDF, a simulation demo and launch files, tested on Ubuntu 22.04 with ROS 2 Humble.

## Simulation

```
sudo apt install ros-humble-desktop ros-humble-moveit
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
git clone https://github.com/Source-Robotics/PAROL6-ROS2-MOVEIT.git
cd ~/ros2_ws && colcon build
source /opt/ros/humble/setup.bash && source install/setup.bash
LC_NUMERIC=en_US.UTF-8 ros2 launch parol6_moveit demo.launch.py
```

RViz opens with the robot, and MoveIt plans and executes on the mock hardware.

## The real robot

`real_robot.launch.py` brings up the same stack on `ros2_control`, with a hardware interface and a bridge that
talk to the Python API's controller, which must be running (`parol6-server --serial ...`, or its simulator mode).
The hardware interface lives in [parol6_ros2_control](https://github.com/grahas/parol6_ros2_control), a community
repository, cloned next to the MoveIt package:

```
cd ~/ros2_ws/src
git clone https://github.com/grahas/parol6_ros2_control.git
cd ~/ros2_ws && colcon build
ros2 launch parol6_moveit real_robot.launch.py bridge_python:=/path/to/venv/bin/python3
```

The `bridge_python` must have the `parol6` package installed. On Ubuntu 22.04 it does not install: the package
needs Python 3.11 or newer, and on Linux its kinematics backend ships wheels only for glibc 2.39 or newer
(Ubuntu 24.04), while 22.04 has Python 3.10 and glibc 2.35 ([Installation](https://docs.source-robotics.com/PAROL-docs/1.1/programming/02-python-api/installation/)). The
interface's README gives the way round it: run `parol6-server` and the bridge on another machine, or under WSL2,
where `parol6` installs, and point the hardware interface's `bridge_host` parameter at it over the network.

## The URDF

The robot description, URDF and MuJoCo with meshes and a version per tool, is in
[robot_descriptions](https://github.com/Source-Robotics/robot_descriptions/tree/v2.15.1/guides/parol6.md), and an earlier URDF is inside the Python API (`parol6/urdf_model`). The gripper repositories have URDF and MJCF descriptions of the SSG-48 and MSG for
attaching to it.

## Other ROS 2 projects

[parol6_commander](https://github.com/Lyczko0/parol6_commander), a web GUI on ROS 2 and MoveIt 2, and
[Parol6-firmware](https://github.com/Lyczko0/Parol6-firmware), alternative firmware with micro-ROS, are community
projects ([Community projects](https://docs.source-robotics.com/PAROL-docs/1.1/appendix/community/)).
