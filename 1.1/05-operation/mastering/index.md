# Mastering

Homing brings each joint to its switch and then a fixed number of steps to the after-homing pose. That number is in
the firmware, measured on the reference robot. Printers and parts differ, so on your robot the homed pose may be
off by a fraction of a degree per joint. Mastering measures the difference and corrects the number, so that a
homed robot stands exactly at its witness marks.

## Witness marks

Holes in neighbouring links that line up when the joint stands where homing should leave it, in the
after-homing pose (90°, −90°, 180°, 0°, 0°, 180°): a pin pushed through them proves the pose. PAROL6 has them on
every joint.

![Witness marks of PAROL6](https://docs.source-robotics.com/PAROL-docs/1.1/assets/parolw.webp){ width="800" }

## The procedure

1. Home the robot.
2. For each joint, jog it in small steps until the pin fits through its witness marks. Jog at the lowest speed
   and read the joint's position from the commander's position display or `rbt.angles()`.
3. Convert the angle you jogged by to motor steps with the joint's ratio ([Drives, ratios and resolution](https://docs.source-robotics.com/PAROL-docs/1.1/03-technical-data/drives-and-ratios/)),
   or read the step count from the firmware's telemetry.
4. For joints 1 to 4: in `motor_init.cpp`, add that number of steps to the joint's `homed_position` (subtract if
   you jogged in the negative direction), upload the firmware, and home again. The pin should now fit without
   jogging. Joints 5 and 6 work differently, below.

```cpp
/// @brief Number of steps from when the limit switch is hit to the standby position
Joint__->homed_position = 13500;   // joint 1: raise or lower by the steps you measured
```

The values of the reference robot are on [Firmware parameters](https://docs.source-robotics.com/PAROL-docs/1.1/reference/firmware-parameters/).

## Joint 5 and the tool

Joint 5 homes against a feature of the tool, so its number depends on the tool: 8900 steps with the pneumatic
gripper holder and 8035 with the SSG-48, set as `j5_homing_offset` in `main.cpp`. Master joint 5 by changing that
value, not its `homed_position`. A custom tool needs its own value, found the same way.

## Joint 6

Joint 6 has no offset to master in firmware 1. Its `homed_position` (15900) is only the position from which
joint 5 homes: when joint 5 is done, joint 6 turns back to the point where its sensor saw the homing pin, and that
point is its after-homing position. If joint 6 does not line up with its witness marks after homing, move its
sensor or its homing pin.

## When to master again

After replacing a belt, a switch, a sensor or a printed part of a joint, or when the robot's absolute accuracy
matters more than its repeatability. The repeatability does not depend on mastering: a homed robot returns to
the same place every time, whether or not that place is exactly the witness mark.
