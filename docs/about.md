# About this manual

## Scope and audience

The PAROL6 Robot Manual covers the PAROL6 desktop robotic arm from the box, or the printer, to a robot that runs
programs: what the robot is, how to install it safely, how it is switched on, homed, jogged and run, which tools
and grippers it takes, its inputs, outputs and pneumatics, how it is maintained and what to do when something
fails. The Build guide, part of the same document, covers building one from the published files. Two more
documents live on this site: the [Control Board Manual](board/index.md), for the electronics inside the base, and
the [Programming Guide](programming/index.md) with its [API reference](reference/index.md), for everyone who writes
programs for the robot.

The manual is written for someone who has a PAROL6 or is building one: a maker, a student, a teacher or an engineer
who can run a Python script and tighten a belt. It does not assume robotics training; the concepts the robot's
software uses are explained in the [Theory corner](theory/index.md), which
anyone can read first. Read the [Safety](02-safety/index.md) chapter before you power anything. The
[Quick start](quick-start.md) is the first day on one page; the chapters are in the order you need them and go
deeper.

## Finding your way

--8<-- "navigation.md"

## Warnings and notes

Three kinds of highlighted text appear in this documentation. Read every Danger and Notice before you act on the
step it belongs to.

--8<-- "symbols.md"

## Related documents

<!-- documents-table -->

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
| Robot Manual | 2026.A (draft) | — | First version in this form: the numbered chapters, the build guide, from the pages of the previous site |
| Control Board Manual | 2026.A (draft) | — | First version in this form, from the control board and peripherals pages of the previous site |
| Programming Guide | 2026.A (draft) | — | First version: the concepts, the Python API 0.9.1, the commander software and RBTscript, ROS 2; the generated API reference |
