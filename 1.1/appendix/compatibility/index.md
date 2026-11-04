# Versions and compatibility

| PAROL6 release | Released | Control board | Control board firmware | Python API (parol6) | Commander software | Grippers | Docs |
|---|---|---|---|---|---|---|---|
| 1.1 | 2026-11-04 | v2.0 (pluggable terminal blocks); v1.2 (spring contacts) is functionally identical | 1 (VERSION 1 in constants.h), unchanged since release 1 | 0.2.6 to 0.9.1 (the reference describes 0.9.1); Python 3.11 or newer | main branch (Python 3.10 or 3.11) | SSG-48 (Spectral Micro firmware 101 or newer), MSG (STEPFOC firmware 103 or newer), pneumatic MHZ2-16D, vacuum | 1.1 |
| 1 | 2025-03-08 | v2.0 (pluggable terminal blocks); v1.2 (spring contacts) is functionally identical | 1 (VERSION 1 in constants.h), main branch | 0.2.6 to 0.9.1 (the reference describes 0.9.1); Python 3.11 or newer | main branch (Python 3.10 or 3.11) | SSG-48 (Spectral Micro firmware 101 or newer), MSG (STEPFOC firmware 103 or newer), pneumatic MHZ2-16D, vacuum | 1 |

## Reading the table

- **Control board** v2.0 has pluggable terminal blocks; v1.2 had spring-loaded contacts. They are functionally
  identical and run the same firmware.
- **Control board firmware** is released with the robot (`#define VERSION 1`). The serial protocol it speaks is
  the one every PC program on this site uses.
- **Python API**: the reference on this site is read from the version named on the Programming landing page.
  Older 0.x versions have fewer commands; the API is pre-1.0, so a minor version can change an interface, as the
  [release notes](https://docs.source-robotics.com/PAROL-docs/1.1/appendix/release-notes/) say.
- **Commander software** has no releases; the main branch is what you clone. The `experimental_kinematics` branch
  fixes most Cartesian jogging errors but can make dangerous moves: main is the safe one.
- **Grippers**: the firmware's gripper protocol works with every released firmware of both grippers.
