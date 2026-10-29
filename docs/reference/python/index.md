# Python API reference

The public methods of `RobotClient` (the sync client; the async client has the same methods, awaited, plus the
two status streams), generated from the API's source at <!-- api-version -->. `rbt` in the signatures is a
client, `rbt = RobotClient()`.

The conventions, once: angles in degrees in order J1 to J6, poses as `[x, y, z, rx, ry, rz]` in millimetres and
degrees, `speed` and `accel` as fractions in (0, 1], `duration` in seconds, `r` a blend radius in millimetres,
joints indexed from 0 in jog calls. A motion call returns the command index (≥ 0) or −1 if refused; a query
returns `None` on a timeout; a refused or failed command raises `MotionError` ([Errors](errors.md)).

<!-- api-method-index -->
