# Your own tool

## Mounting

Two ways to fix a tool to the 8 mm shaft of joint 6:

| Way | What you use |
|---|---|
| Clamp it | A shaft coupler from the BOM |
| Print a holder with a coupler connector | The SSG-48 repository's template, `STEP files/Couplers/coupler_connector_generic_STEP.STEP` (and `Print files/Couplers/connector_coupler_generic.STL`). The `STL/WRIST/wrist.STL` in the robot's files shows the mating geometry. |

Keep the tool within the payload, and short: every millimetre past the flange is leverage against joints 4 and 5.

## The joint 5 homing feature

Joint 5 finds its reference by driving the forearm's limit switch against a feature of the tool holder. Your
holder needs a surface in the same place as the pneumatic gripper holder's; compare with
`Pneumatic_gripper_holder.STL`.

Then measure the homing offset ([Mastering](../05-operation/mastering.md)):

1. Home.
2. Jog joint 5 until the pin fits the witness marks.
3. Set `j5_homing_offset` in `main.cpp` to the steps that gives.

## Connections

| What | Where |
|---|---|
| Up to 24 V and CAN | The M8 connector (its pins: [The gripper socket](flange.md#the-gripper-socket)) |
| Two air lines | At the forearm |
| The control board's two inputs and two outputs | At the base |

A tool that needs more, a camera's USB for instance, runs its cable outside the arm, with enough slack for joints
4, 5 and 6, and fixed so the arm cannot catch it.

## The tool frame

The software positions the tool centre point. In the Python API, register the tool once with its transform from
the flange, or set an offset at run time:

```python
rbt.select_tool("NONE")
rbt.set_tcp_offset(0, 0, -120)                 # the tip, 120 mm out from the flange: along the tool's -Z
index = rbt.set_tcp_transform(0, 0, -120, 0, 15, 0)  # with a rotation, intrinsic XYZ degrees
rbt.wait_command(index)
```

!!! warning "The Python API's tool frame has Y and Z the other way"
    In the Python API (version 0.9.1) the flange frame's Z points back into the wrist, the other way from the
    commander's and these pages' ([The flange frame](../theory/reference-frames.md#the-flange-frame)), so a tip in
    front of the flange has a negative z there ([known issue KI-11](../08-troubleshooting/known-issues.md)).

| Program | A permanent tool |
|---|---|
| Python API | Goes into the tool registry as a `ToolConfig` with its collision mesh, so that the collision checker knows its shape ([Tools and the TCP](../programming/02-python-api/tools-and-tcp.md)) |
| Commander software | Has no tool setting: its poses are for the standard pneumatic gripper, and a different tool means editing its robot model |

## Check before you run

Jog joint 5 and joint 6 through their ranges slowly with the tool mounted.

!!! success "Check"
    No contact with the forearm. The software's joint limits do not know the tool's shape.
