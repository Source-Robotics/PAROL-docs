# Examples

Programs from the repository's `GUI/files/Programs` folder and the documentation. Paste one into the program
window, read it against the simulator, and press Start. The speed slider does not slow a program: for a first
run, lower `v=` or raise `t=` in the moves.

## A joint-space loop

Two poses, back and forth, with a timed first move.

```
Begin()
Delay(1)
MoveJoint(85.078,-111.195,143.513,-32.92,18.084,129.448,t=3)
Delay(1)
MoveJoint(66.129,-117.368,136.77,46.28,-29.588,149.293)
Delay(1)
Loop()
```

## Cartesian moves in the world frame

A joint move to a start pose, then straight-line moves: translations first, then rotations about each axis of the
tool. Watch the simulator to see the tool follow its axes.

```
Begin()
Delay(1)
MoveJoint(90.0,-90.0,180.001,0.0,0.0,180.0,t=4)
Delay(1)
MoveCart(0.0,263.23,161.241,-90.0,0.0,-89.499)
Delay(1)
MoveCart(81.565,262.804,161.047,-90.135,-0.029,-89.578)
Delay(1)
MoveCart(81.649,194.981,160.077,-90.14,-0.043,-89.593)
Delay(1)
MoveCart(83.598,194.356,161.493,-91.155,1.306,-80.28)
Delay(1)
MoveCart(84.56,194.131,162.347,-48.387,1.261,-80.188)
Delay(1)
MoveCart(82.89,191.698,162.369,-40.587,26.026,-107.028)
Delay(1)
End()
```

## A move relative to the tool

80 mm back along the tool's X axis from wherever the tool is.

```
Begin()
Delay(1)
MoveJoint(90.0,-90.0,180.001,0.0,0.0,180.0,t=4)
Delay(1)
MoveCartRelTRF(-80,0,0,0,0,0)
Delay(1)
End()
```

## Pick and place with the gripper

From the repository: a joint move over the part, a Cartesian descent, a grip, a transfer and a release. Note the
delays after each gripper command.

```
Begin()
Delay(1)
MoveJoint(89.209,-35.021,174.356,-1.463,-28.645,85.972,t=4)
Delay(1)
Gripper(255,20,120)
Delay(2)
MoveCart(-40.499,298.455,131.712,6.081,-0.739,-179.276)
MoveJoint(15.478,-56.126,178.673,-0.928,-54.084,85.5)
Delay(1)
Gripper(0,100,120)
MoveJoint(89.033,-49.402,174.486,-1.027,-43.341,85.596)
MoveCart(-41.535,300.316,17.635,6.141,-0.686,-179.224)
Delay(1)
Gripper(255,100,1000)
Delay(1)
MoveCart(-40.499,298.455,131.712,6.081,-0.739,-179.276)
MoveJoint(15.478,-56.126,178.673,-0.928,-54.084,85.5)
Gripper(0,100,100)
Delay(1)
End()
```

## Gripper test

Calibration, a few open and close cycles, then a small joint move and a Cartesian move.

```
Begin()
Gripper_cal()
Delay(3)
Gripper(100,60,600)
Delay(2)
Gripper(200,60,600)
Delay(2)
MoveJoint(85.192,-104.451,158.769,-1.983,-46.491,179.899,t=6)
Delay(1)
MoveCart(4.317,103.384,192.319,-84.465,1.447,-143.154)
Gripper(100,60,600)
Delay(2)
End()
```

## Toggling an output

A pneumatic gripper, or a lamp, once a second, forever.

```
Begin()
Output(1,HIGH)
Delay(1)
Output(1,LOW)
Delay(1)
Loop()
```

## A dance

Timed joint and Cartesian moves in quick succession: `example_dance_2.txt` in the repository, for a demo once the
robot is known to run every pose in it.
