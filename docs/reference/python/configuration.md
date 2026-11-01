# Configuration

The hardware connection, the motion profile, the TCP corrections, the collision world and the status rate.
[Tools and the TCP](../../programming/02-python-api/tools-and-tcp.md) and [The controller](../../programming/02-python-api/controller.md)
in the guide.

<!-- api: connect_hardware -->

<!-- api: select_profile -->

!!! note
    The profiles of this version: <!-- api-profiles -->. [Motion profiles](../../theory/motion-profiles.md)
    says what each does.

<!-- api: set_tcp_offset -->

<!-- api: set_tcp_transform -->

<!-- api: tcp_offset -->

<!-- api: tcp_transform -->

!!! note
    `set_tcp_transform(x, y, z, roll, pitch, yaw)`: millimetres and intrinsic XYZ degrees relative to the
    registered tool. Both setters return a queued index; wait for it before relying on the correction. The TCP
    queries raise `TimeoutError` instead of returning a misleading zero when the controller does not answer.

<!-- api: set_shapes -->

!!! note
    Shapes are the program layer of the collision world: boxes and other primitives with a pose in metres and
    extrinsic XYZ radians, collision-enabled or visual only, attachable to the flange as held objects. The
    installation layer, from the robot's configuration, is not affected.

<!-- api: set_status_rate -->
