# About this manual

## Scope and audience

The PAROL6 Robot Manual covers the PAROL6 desktop robotic arm from the box, or the printer, to a robot that runs
programs: what the robot is, how to install it safely, how it is switched on, homed, jogged and run, which tools
and grippers it takes, its inputs, outputs and pneumatics, how it is maintained and what to do when something
fails. The Build guide, part of the same document, covers building one from the published files. Four more
documents live on this site: the [Control Board Manual](https://docs.source-robotics.com/PAROL-docs/1/board/), for the electronics inside the base; the
[End Effectors Guide](https://docs.source-robotics.com/PAROL-docs/1/end-effectors/), for the grippers and tools on the flange; the
[GUI Guide](https://docs.source-robotics.com/PAROL-docs/1/gui/), for the graphical programs; and the [Programming Guide](https://docs.source-robotics.com/PAROL-docs/1/programming/) with its
[API reference](https://docs.source-robotics.com/PAROL-docs/1/reference/), for everyone who writes programs for the robot. The list under *Related
documents* gives their numbers.

The manual is written for someone who has a PAROL6 or is building one: a maker, a student, a teacher or an engineer
who can run a Python script and tighten a belt. It does not assume robotics training; the concepts the robot's
software uses are explained in the [Theory corner](https://docs.source-robotics.com/PAROL-docs/1/theory/), which
anyone can read first. Read the [Safety](https://docs.source-robotics.com/PAROL-docs/1/02-safety/) chapter before you power anything. The
[Quick start](https://docs.source-robotics.com/PAROL-docs/1/quick-start/) is the first day on one page; the chapters are in the order you need them and go
deeper.

## Finding your way

The header has seven tabs. **PAROL6 Robot Manual** is the document you read from the start: the quick start, then
safety, technical data, installation, operation, peripherals, maintenance and troubleshooting, in numbered
chapters, followed by the build guide. **Control Board** is the manual of the electronics inside the base: the
connectors, the stepper drivers, the I/O wiring, the firmware, the serial protocol. **End effectors** is what goes
on the flange: the pneumatic and vacuum grippers, the SSG-48 and MSG electric grippers, a tool of your own, and
how each is mounted, connected and driven. **GUI interfaces** covers the graphical programs: the commander
software, Waldo Commander, Motor GUI. **Programming** is for everyone who writes programs for the robot: the
interfaces, the concepts, the Python API, RBTscript, ROS 2, and the reference where you look things up: every
method of the Python API, read from its source, the RBTscript commands, the serial protocol byte by byte, the
firmware parameters. **Theory corner** explains the robotics behind the software, from joint numbering and
units to kinematics, singularities and motion profiles, for anyone who wants to read first. **Support** says where
to get help and how to report a problem.

The whole site describes one PAROL6 release. The dropdown next to the site name switches between releases, and a
page from an older release says so in a bar at the top. The repository card on the right of the header opens the
repository the page belongs to; every page ends with a link to edit it and one to report a problem with it.
## Warnings and notes

Three kinds of warnings and notes appear in this documentation. Read every Danger and Notice before you act on
the step it belongs to. A green **Check** box after a setup step says what you should see when the step worked,
and where to go when it did not.

!!! note "Note"
    Points out something that is easy to miss or that changes what follows: a default, a limit, a side effect.

!!! warning "Notice"
    The robot, the tool, or data on the control board or the PC can be damaged or lost if this is ignored. Nobody is
    at risk.

!!! danger "Danger"
    Someone can be injured if this is ignored. Stop and read the whole box before acting on the step it belongs to.
## Related documents

| Document | Number | Covers |
|---|---|---|
| PAROL6 Robot Manual | SR-1002 | the robot: quick start, safety, technical data, installation, operation, peripherals, maintenance, troubleshooting, transport; the build guide |
| PAROL6 Control Board Manual | SR-2002 | the control board: features, technical data, connectors and pinout, stepper drivers, I/O and E-stop, CAN, firmware upload, the test firmware, the serial protocol |
| PAROL6 Programming Guide | SR-4004 | the ways to program the robot, the concepts behind them, the Python API, RBTscript, ROS 2; the reference: every method of the Python API, the RBTscript commands, the serial protocol, the firmware parameters |
| PAROL6 End Effectors Guide | SR-3004 | what goes on the flange: the pneumatic and vacuum grippers, the SSG-48 and MSG electric grippers, a tool of your own; mounting, connections, the joint 5 homing offset, driving them from the commander software and the Python API |
| PAROL6 GUI Guide | SR-4005 | the graphical programs: the commander software (installation, the windows, the tabs), Waldo Commander in the browser, Motor GUI for the grippers |

Every document describes PAROL6 release 1; the version selector in the header switches between releases. The compatibility table says which control board, firmware, Python API, commander and gripper versions work together.

The grippers made for PAROL6 are documented separately: the SSG-48 at
[docs.source-robotics.com/SSG48-gripper-docs](https://docs.source-robotics.com/SSG48-gripper-docs/), the MSG at
[docs.source-robotics.com/MSG-gripper-docs](https://docs.source-robotics.com/MSG-gripper-docs/). PAR6, the larger
arm, is documented at [docs.source-robotics.com/par6](https://docs.source-robotics.com/par6/).

## Document history

The documents on this site describe one PAROL6 release; one revision is kept per release, and the version selector
in the header switches between them. The Programming Guide and the API reference also name the Python API version
they describe, because the API is released more often than the robot.

The text and the images of this documentation are licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/),
the code examples under the [MIT licence](https://github.com/Source-Robotics/PAROL-docs/blob/main/LICENSE-CODE).
The robot's mechanical files, firmware and software are published under GPLv3 in their repositories. The Source
Robotics name, the product names and the logos are not covered by any of these.

| Document | Revision | Date | Changes |
|---|---|---|---|
| Robot Manual | 2026.A | 2026-11-03 | First version in this form: the numbered chapters, the build guide, from the pages of the previous site |
| Control Board Manual | 2026.A | 2026-11-03 | First version in this form, from the control board and peripherals pages of the previous site |
| End Effectors Guide | 2026.A | 2026-11-03 | First version: the flange, the pneumatic and vacuum grippers, the SSG-48 and MSG, your own tool |
| GUI Guide | 2026.A | 2026-11-03 | First version: the commander software, Waldo Commander, Motor GUI |
| Programming Guide | 2026.A | 2026-11-03 | First version: the concepts, the Python API 0.9.1, the commander software and RBTscript, ROS 2; the generated API reference |
