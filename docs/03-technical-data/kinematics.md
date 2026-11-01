# Dimensions and kinematics

<div class="arm-viewer" data-base="../../assets/models/parol6/" markdown="0">
  <canvas class="arm-viewer__canvas" aria-label="PAROL6 in 3D: drag to turn, scroll to zoom"></canvas>
  <div class="arm-viewer__controls">
    <div class="arm-viewer__joints"></div>
    <label class="arm-viewer__field">Printed parts <span class="arm-viewer__swatches" data-target="body"></span><input type="color" name="body" value="#c9c9c6" title="Any colour"></label>
    <button type="button" name="reset" class="md-button">Reset</button>
  </div>
  <p class="arm-viewer__hint">Drag to turn the robot, scroll to zoom, move each joint with its slider, try a colour for the printed parts. The model is the
robot's <a href="https://github.com/Source-Robotics/robot_descriptions/blob/main/guides/parol6.md">URDF</a>; the sliders run over its joint limits.</p>
</div>

## Dimensions

The sheets below come from PAROL6's models in
[robot_descriptions](https://github.com/Source-Robotics/robot_descriptions) (version 2.13.0). Each shows the robot's
own meshes with every joint at 0, in one orthographic side view at one scale, with the dimensions taken from the
URDF, not measured from the picture, and the standard DH table to the tool centre point (TCP) of that
configuration. Click a sheet to enlarge it.

=== "Flange only"

    ![PAROL6 with nothing on the flange: dimensions and the DH table to the TCP](../assets/kinematics/parol6_flange.webp){ width="700" }

=== "Pneumatic gripper"

    ![PAROL6 with the standard pneumatic gripper: dimensions and the DH table to the TCP](../assets/kinematics/parol6_pneumatic.webp){ width="700" }

=== "SSG-48"

    ![PAROL6 with the SSG-48 gripper, solid jaws: dimensions and the DH table to the TCP](../assets/kinematics/parol6_ssg48.webp){ width="700" }

=== "SSG-48 fin-ray"

    ![PAROL6 with the SSG-48 gripper, fin-ray jaws: dimensions and the DH table to the TCP](../assets/kinematics/parol6_ssg48_stock.webp){ width="700" }

=== "MSG"

    ![PAROL6 with the MSG gripper, solid jaws: dimensions and the DH table to the TCP](../assets/kinematics/parol6_msg.webp){ width="700" }

=== "MSG soft jaws"

    ![PAROL6 with the MSG gripper, soft TPU jaws: dimensions and the DH table to the TCP](../assets/kinematics/parol6_msg_tpu_glue.webp){ width="700" }

| Dimension | What it is | Value |
|---|---|---|
| a1 | Base height: the floor to the joint 2 axis | 110.5 mm |
| a2 | Shoulder offset: the joint 1 axis to the joint 2 axis | 23.42 mm |
| a3 | Upper arm: joint 2 to joint 3 | 180 mm |
| a4 | Elbow offset | 43.5 mm |
| a5 | Forearm: the joint 3 axis to the wrist centre | 177 mm |
| a6 | The joint 6 centre to the TCP, along the tool axis | depends on the tool, below |
| a7 | Sideways offset of the TCP | depends on the tool, below |

| Tool | a6 | a7 |
|---|---|---|
| Flange only (the TCP is the flange face) | 50.5 mm | 0 |
| Pneumatic gripper | 62.3 mm | 45.25 mm |
| SSG-48, solid or fin-ray jaws | 134.3 mm | 0 |
| MSG, solid or soft jaws | 134.3 mm | 28.35 mm |

A riser under the base changes a1, and a tool of your own changes a6 and a7: tell the software about the tool
([Tools and the TCP](../programming/02-python-api/tools-and-tcp.md)), or the poses it reports will be wrong.

!!! note "The software computes with the earlier model"
    The Python API (its built-in URDF) and the commander software use a5 = 176.35 mm, the value of the earlier
    model, and the commander uses a6 = 62.8 mm for the pneumatic gripper. The models above use 177 mm and 62.3 mm.
    A pose the software reports can therefore differ from these sheets by up to about 0.65 mm.

## Kinematic structure

The first three joints place the wrist centre; the axes of joints 4, 5 and 6 intersect in one point, a
spherical wrist, which is what makes the inverse kinematics tractable. The
[Theory corner](../theory/kinematics.md) explains forward and inverse kinematics, and
[Configurations and singularities](../theory/configurations-and-singularities.md) the eight ways the arm can
reach one pose.

## Denavit-Hartenberg parameters

Standard DH, each joint's transform being `A_i = Rz(theta_i) Tz(d_i) Tx(a_i) Rx(alpha_i)`, from the base to the
TCP. `q1` to `q6` are the model's joint angles; the theta column already contains the joint offsets, so do not add
them twice. The sheets above give the same table for each tool.

| Joint | Link | theta | alpha | a | d |
|---|---|---|---|---|---|
| 1 | Base | q1 | -90° | a2 = 23.42 mm | a1 = 110.5 mm |
| 2 | Shoulder | q2 - 90° | 180° | a3 = 180 mm | 0 |
| 3 | Elbow | q3 + 180° | 90° | -a4 = -43.5 mm | 0 |
| 4 | Wrist 1 | q4 | -90° | 0 | -a5 = -177 mm |
| 5 | Wrist 2 | q5 | 90° | 0 | 0 |
| 6 | Wrist 3, to the TCP | q6 + 180° | 180° | -a7 | -a6 |

The models were checked at 128 poses including the joint limits: the DH table, the URDF and the MuJoCo model agree
to within 0.006 mm and 0.002°. The Python API does not use the table directly: it loads its URDF and computes the
kinematics numerically. The commander software uses a Robotics Toolbox DH model.

## Mounting holes

Six holes in the base, on a pattern made for 30×30 mm aluminium profiles. The mounting plates folder of the
repository has STEP drawings of a small and a big base plate: [Mounting the robot](../04-installation/mounting.md).
