# Report a problem

A report that can be acted on says what you did, what happened, and what the robot said. Include:

1. **The robot**: bought or self-built; control board version (v2.0 with terminal blocks, or v1.2); the firmware
   (main, from which commit, and whether you changed `constants.h` or `motor_init.cpp`).
2. **The software**: commander (which commit, which Python version, which OS) or Python API (`pip show parol6`),
   or something else.
3. **What you did**: the exact steps, the program or script, the jog, the command.
4. **What happened**: and what you expected instead. A short video helps for anything mechanical.
5. **What the robot said**: the commander's response log and terminal output, or the API's exception text and the
   controller's log.
6. **The PC**: processor and OS, for anything about timing or communication.

Where to file it is on [Getting help](index.md). A problem with a gripper goes to the gripper's own repository,
with the same facts.
