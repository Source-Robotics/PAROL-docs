# Errors

The error codes of the controller, with the catalog text a `MotionError` carries, from the source at
<!-- api-version -->. The number ranges: 10 to 19 inverse kinematics, 20 to 29 trajectory planning, 30 to 39
motion execution, 40 to 49 communication, 50 to 59 system and safety. `MOTN_CANCELLED` uses the number shared
with the waldoctl interface, so that a client sees one code for a discarded command whichever arm raised it.
[Errors](../../programming/02-python-api/errors.md) in the guide says how to recover.

<!-- api-errors-table -->

A `RobotError` has the fields `code`, `title`, `cause`, `effect` and `remedy`, and `str(error)` joins them.
