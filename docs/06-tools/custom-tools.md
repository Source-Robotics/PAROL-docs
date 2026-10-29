# Your own tool

## Mounting

Clamp onto the 8 mm shaft of joint 6 with a shaft coupler from the BOM, or print a holder with a coupler
connector: the gripper repositories have a coupler connector template as a STEP file, and the `wrist.STL` in the
robot's files shows the mating geometry. Keep the tool within the payload and short: every millimetre past the
flange is leverage against joints 4 and 5.

## The joint 5 homing feature

Joint 5 finds its reference by driving the forearm's limit switch against a feature of the tool holder. Your
holder needs a surface in the same place as the pneumatic gripper holder's; compare with `Pneumatic_gripper_holder.STL`.
Then measure the homing offset: home, jog joint 5 until the pin fits the witness marks, and set
`j5_homing_offset` in `main.cpp` to the steps that gives ([Mastering](../05-operation/mastering.md)).

## Connections

Up to 24 V and CAN at the M8 connector, two air lines, and the control board's two inputs and two outputs at the
base. A tool that needs more, a camera's USB for instance, runs its cable outside the arm, with enough slack for
joints 4, 5 and 6 and fixed so the arm cannot catch it.

## The tool frame

The software positions the tool centre point. In the Python API, register the tool once with its transform from
the flange, or set an offset at run time:

```python
rbt.select_tool("NONE")
rbt.set_tcp_offset(0, 0, 120)                  # the tip, 120 mm along the tool's Z
index = rbt.set_tcp_transform(0, 0, 120, 0, 15, 0)   # with a rotation, intrinsic XYZ degrees
rbt.wait_command(index)
```

A permanent tool goes into the API's tool registry as a `ToolConfig` with its collision mesh, so that the
collision checker knows its shape ([Tools and the TCP](../programming/03-python-api/tools-and-tcp.md)). The
commander software has no tool setting: its poses are for the standard pneumatic gripper, and a different tool
means editing its robot model.

## Check before you run

Jog joint 5 and joint 6 through their ranges slowly with the tool mounted and watch for contact with the forearm:
the software's joint limits do not know the tool's shape.
