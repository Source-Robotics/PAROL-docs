# Blending

A program with many waypoints stops at each one unless told otherwise, and every stop costs time and a jolt.
Blending lets the robot pass near a waypoint without stopping: when the tool comes within a radius of the
waypoint, it starts the next move, and the path rounds the corner.

- The tool does not pass **through** a blended waypoint; it cuts the corner inside the radius. A waypoint where
  the tool must be exactly, a pick or a place, is not blended.
- The blend radius is in millimetres of the tool's path.
- A blend needs the next move to be known when the current one starts: in the Python API the moves are queued,
  so the controller looks ahead and blends.

## In the Python API

`move_j`, `move_l` and `move_c` take `r`, the blend radius; `r=0` stops at the target. `move_p` is the
process move: a list of waypoints run at constant tool speed with automatic blending at every corner, for scan
and dispensing paths. A tool action or a `delay()` queued after a blended move ends the blend there: the arm
stops for it. The zig-zag example in the API's repository shows a raster scan with blends.

```python
rbt.move_l([200, 0, 250, 90, 0, 90], speed=0.5, r=15)
rbt.move_l([200, 160, 250, 90, 0, 90], speed=0.5, r=15)
rbt.move_l([250, 160, 250, 90, 0, 90], speed=0.5)          # stops here
```

## In the commander software

RBTscript has no blending: every move ends at rest. Make the path with fewer, longer moves, or with `MoveCart`
through points far enough apart that the stops do not matter.
