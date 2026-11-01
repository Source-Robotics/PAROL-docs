# Control

Commands that change what the controller is doing: stops, the protective stop and its reset, pause and execution
speed, simulator mode, teleport, and the state reset. They are system commands: immediate, not queued, accepted
also while the controller is disabled. [Control ownership](../../theory/control-ownership.md).

<!-- api: stop -->

<!-- api: estop -->

<!-- api: reset -->

<!-- api: reset_state -->

<!-- api: pause -->

<!-- api: resume -->

<!-- api: set_execution_speed -->

<!-- api: simulator -->

<!-- api: teleport -->

<!-- api: run_skill -->

!!! note
    Skills are decorated Python functions from the waldoctl skill runtime, run on the connected client; Waldo
    Commander uses them. A plain script does not need them.

<!-- api: close -->
