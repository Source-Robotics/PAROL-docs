# Reference frames

A frame is a coordinate system: an origin and three axes, X, Y and Z, at right angles. A position is three
numbers in a frame; the same point has different numbers in different frames. PAROL6's software uses two frames
you choose between, the world frame and the tool frame, and several it keeps to itself, the flange frame among
them.

## The right-hand rule

All frames are right-handed: with the right hand's thumb along X and the index finger along Y, the middle finger
points along Z. For rotations, the thumb along the axis, the fingers curl in the positive direction. Every
orientation angle in the software follows this rule.

## The frames on the robot

=== "Flange only"

    ![The world frame (WRF) at the base and the tool frame (TRF) at the flange, in the standby pose; with nothing on the flange the TRF is the flange frame](../assets/figures/parol6_frames_flange.webp#only-light){ width="640" }
    ![The world frame (WRF) at the base and the tool frame (TRF) at the flange, in the standby pose; with nothing on the flange the TRF is the flange frame](../assets/figures/parol6_frames_flange_dark.webp#only-dark){ width="640" }

=== "Pneumatic gripper"

    ![The world frame (WRF) at the base and the tool frame (TRF) at the pneumatic gripper's TCP, in the standby pose](../assets/figures/parol6_frames_pneumatic.webp#only-light){ width="640" }
    ![The world frame (WRF) at the base and the tool frame (TRF) at the pneumatic gripper's TCP, in the standby pose](../assets/figures/parol6_frames_pneumatic_dark.webp#only-dark){ width="640" }

=== "SSG-48"

    ![The world frame (WRF) at the base and the tool frame (TRF) at the SSG-48's TCP, in the standby pose](../assets/figures/parol6_frames_ssg48.webp#only-light){ width="640" }
    ![The world frame (WRF) at the base and the tool frame (TRF) at the SSG-48's TCP, in the standby pose](../assets/figures/parol6_frames_ssg48_dark.webp#only-dark){ width="640" }

=== "MSG"

    ![The world frame (WRF) at the base and the tool frame (TRF) at the MSG's TCP, in the standby pose](../assets/figures/parol6_frames_msg.webp#only-light){ width="640" }
    ![The world frame (WRF) at the base and the tool frame (TRF) at the MSG's TCP, in the standby pose](../assets/figures/parol6_frames_msg_dark.webp#only-dark){ width="640" }

The pictures show the frames as the Python API defines them, drawn on the robot's model: X red, Y green, Z blue.
The arcs at the tool frame are the positive rotations RX, RY and RZ. An axis is dashed where it runs inside the
robot. The directions in the table are those of the standby pose.

| Frame | Origin | X | Y | Z |
|---|---|---|---|---|
| WRF | On the joint 1 axis, at the base's mounting surface | Forward: the way the arm points in the standby pose, away from the electronics case | To the left, seen from behind the robot: the way the arm points after homing | Up, along the joint 1 axis |
| Flange frame | On the joint 6 axis, at the flange | Up; it turns with joint 6 | To the robot's left | Back along the joint 6 axis, into the wrist |
| TRF | At the tool centre point (TCP) | As the flange frame | As the flange frame | As the flange frame: back along the tool, away from the part |

## WRF, the world reference frame

Fixed to the robot's base, as in the table: X the way the arm points in the standby pose, Y the way it points
after homing, Z up. Everything that does not move with the arm is described in it: the table, the parts, the
positions a program teaches. `MoveCart` in RBTscript and `move_l` in the API take WRF poses by default. The
commander software and the Python API agree on it.

## TRF, the tool reference frame

Fixed to the tool: the origin at the tool centre point, the axes those of the flange frame. It moves with the
arm. In the Python API, **Z points back along the tool, towards the wrist**, so the direction towards the part is
−Z. A move **in** the TRF is relative to where the tool is now: "100 mm towards the part, along the tool" is
`move_l([0, 0, -100, 0, 0, 0], frame="TRF", rel=True)`, and it goes in a different world direction every time,
depending on the tool's orientation. Approaching a part along the gripper's axis, retreating after a grip, and
rotating the tool about its own axis are TRF moves.

!!! warning "The commander's tool frame is turned half a turn"
    The commander software computes the tool frame from its own model of the pneumatic gripper. Its X is the same,
    but its Y and Z point the other way: Z points out of the tool, towards the part. In the commander,
    `MoveCartRelTRF(0,0,100,0,0,0)` moves the tool 100 mm towards the part; the same numbers in the Python API
    move it 100 mm away. Jog slowly in the TRF before you run a TRF move written for the other program.

## The flange frame

![The flange frame on the flange face, in the standby pose: X up, Y to the robot's left, Z back along the joint 6 axis into the wrist](../assets/figures/parol6_flange_frame.webp#only-light){ width="520" }
![The flange frame on the flange face, in the standby pose: X up, Y to the robot's left, Z back along the joint 6 axis into the wrist](../assets/figures/parol6_flange_frame_dark.webp#only-dark){ width="520" }

Every tool is measured from the flange frame. Its origin is on the joint 6 axis, and its Z axis points back along
that axis into the wrist. X and Y turn with joint 6: in the standby pose, with joint 6 at 180°, X points up. The
picture puts the origin on the flange face, where the robot's model has it, 50.5 mm from the wrist centre (the
point where the axes of joints 4, 5 and 6 meet). The Python API's built-in model puts it 37 mm from the wrist
centre, 13.5 mm short of the face, and measures its tool offsets from there.

## The TCP of each tool

| Tool | `select_tool` key, variants | TCP in the API's flange frame, x, y, z | From the wrist centre, along the tool and beside it: API | The same in the model: a6, a7 | Jaws close along |
|---|---|---|---|---|---|
| Bare flange | `NONE` | 0, 0, 0 mm | 37 mm, 0 | 50.5 mm, 0 | |
| Pneumatic gripper | `PNEUMATIC`, `vertical` (the default) | −55, 0, −27 mm | 64 mm, 55 mm | 62.3 mm, 45.25 mm | Y |
| Pneumatic gripper | `PNEUMATIC`, `horizontal` | 0, 0, −82 mm | 119 mm, 0 | not in the model | X |
| SSG-48 | `SSG-48`, `finger`, `pinch` | 0, 0, −105 mm | 142 mm, 0 | 134.3 mm, 0 | Y |
| MSG | `MSG`, `100mm`, `150mm`, `200mm` | −29, 0, −109.5 mm | 146.5 mm, 29 mm | 134.3 mm, 28.35 mm | Y |
| Vacuum gripper | `VACUUM` | 0, 0, −37 mm | 74 mm, 0 | not in the model | |

Every tool frame has the flange frame's axes: the Python API's tool definitions are offsets, with no rotation. A
TCP beside the tool axis lies along the flange frame's −X, below the joint 6 axis in the standby pose. The API's
offsets come from the earlier model and differ from the robot's model by up to about 14 mm; the pictures above
are drawn at the model's TCP. `set_tcp_offset()` and `set_tcp_transform()` move the TCP for a correction or a tool
of your own ([Tools and the TCP](../programming/02-python-api/tools-and-tcp.md)).

## Jogging in a frame

The commander's Cartesian jog and the API's `jog_l` take the frame: WRF jogs move the tool along the base's
axes, TRF jogs along the tool's own. Switch to TRF to go straight in or out of a part whatever its angle.

| Jog | In the WRF | In the TRF |
|---|---|---|
| X, Y, Z | The TCP moves along the base's X, Y or Z; the tool keeps its orientation | The TCP moves along the tool's own X, Y or Z, as the tool stands; the tool keeps its orientation |
| RX, RY, RZ | The tool turns about a line through the TCP, parallel to the base's X, Y or Z; the TCP stays where it is. The Python API only: the commander's WRF rotation buttons do nothing | The tool turns about its own X, Y or Z, through the TCP; the TCP stays where it is |

## Orientation

A pose gives the tool frame's orientation in the world frame as three angles in degrees. The Python API reads
them as intrinsic XYZ rotations, R = Rx · Ry · Rz: after homing, with the tool horizontal and pointing away from
the base, a pose ends in 90, 0, 90. [Pose and orientation](pose-and-orientation.md) explains the angles.

## The frames inside

The kinematic model keeps a frame at every joint, each defined relative to the previous one by the
Denavit-Hartenberg parameters, and the flange frame. The tool frame is the flange frame moved by the tool's
transform; the Python API's tool definitions and `set_tcp_transform()` set that transform
([Tools and the TCP](../programming/02-python-api/tools-and-tcp.md)). The commander's model has the pneumatic gripper's
transform built in.
