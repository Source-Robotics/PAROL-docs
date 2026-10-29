# Versions and compatibility

<!-- compatibility-table -->

## Reading the table

- **Control board** v2.0 has pluggable terminal blocks; v1.2 had spring-loaded contacts. They are functionally
  identical and run the same firmware.
- **Control board firmware** is released with the robot (`#define VERSION 1`). The serial protocol it speaks is
  the one every PC program on this site uses.
- **Python API**: the reference on this site is read from the version named on the Programming landing page.
  Older 0.x versions have fewer commands; the API is pre-1.0, so a minor version can change an interface, as the
  [release notes](release-notes.md) say.
- **Commander software** has no releases; the main branch is what you clone. The `experimental_kinematics` branch
  fixes most Cartesian jogging errors but can make dangerous moves: main is the safe one.
- **Grippers**: the firmware's gripper protocol works with every released firmware of both grippers.
