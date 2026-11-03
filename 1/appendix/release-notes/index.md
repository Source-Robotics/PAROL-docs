# Release notes

## PAROL6

### V1 — 2025-03-08

Stable version of the PAROL6 mechanical files, code, documentation and BOM: the first tagged release of the
[robot repository](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/releases/tag/V1). The repository's
main branch continues with BOM updates, the small print bed variants and the community projects list; the
firmware is unchanged since.

## Python API

The releases of [PCrnjak/PAROL6-python-API](https://github.com/PCrnjak/PAROL6-python-API/releases), newest first,
as published on GitHub. The tags `v0.9.0` and `v0.9.1` have no release notes on GitHub; the reference on this
site describes v0.9.1.

### v0.8.1 — 2026-09-20

A patch on **v0.8.0**: PR #51, the Cartesian streaming executor. No API changes.

#### Fixes

- **MOVECART and SERVOL hold their straight line.** Ruckig's synchronization was never set, so it defaulted to `Time` — the six tangent components only *finish* together, each taking its own time-optimal route there, and the tangent bows. The executor now runs under `Phase`, one shared profile for all six.
- **A repeated target no longer costs that synchronization.** A servo stream sets the same target every tick, and each re-plan drops to time synchronization unless the current velocity and acceleration line up exactly with the fresh profile; once out of phase the state drifts further out and the next tick fails too. Setting a target Ruckig is already tracking is now a no-op. On a 160 mm diagonal: 4.7 mm off the line before, 0.000 mm after.
- **The speed ceilings are TCP speeds again.** Ruckig bounds each component on its own, so an isotropic envelope let a diagonal run the resultant up to sqrt(3) times the configured limit — 1.35x as measured. The per-component ceilings are now scaled by the motion direction's largest component over its norm, and the same move peaks at exactly the 0.160 m/s jog ceiling.

### v0.8.0 — 2026-09-19

Everything since **v0.7.0**: PRs #41–#48, the PAROL6 side of waldoctl v0.14.0's skill runtime, full TCP calibration, bounded I/O, execution speed, demonstration metadata, held-object geometry and supervised restart. Pre-1.0, so breaking changes bump the minor.

#### Breaking changes

- **The waldoctl pin moves v0.12.0 → v0.14.0.** `set_tcp_transform`/`tcp_transform` and `set_execution_speed`/`pause`/`resume` are required of every client there and implemented here.
- **Completion waits query the exact command result** (#47, #48), and client and controller must both speak the new query. A controller session change during a wait raises `ConnectionError`; unknown, cancelled and expired results stay unconfirmed instead of passing for success, and replies to timed-out queries are filtered by response type.
- **TCP queries fail explicitly when the controller does not answer** (#43) rather than returning a stale value.
- **Unconfirmed blocking motion completion raises `TimeoutError`** (#45); the queued motion stays until it completes or is stopped.

#### Skills

- **Python skills run on the connected client** (#41). Decorated skills go through the existing synchronous connection and event loop, can use the typed PAROL6 async client internally, compose nested calls, and run unchanged under Commander's stepping wrapper. Live and dry-run clients advertise their skill capabilities. Stopping a planned trajectory now clears the segment player's activity, so status no longer sits at EXECUTING after a cancel.
- **Gripper skills discover PAROL6 gripper support** on the live client and native preview (#42); the preview tool exposes its key and type as metadata, so a requirement check cannot dispatch a command. Streaming updates preserve unread configuration, query and stop packets across a polling batch boundary.

#### Setup and calibration

- **Full TCP transforms through planning and readback** (#43). Translation and intrinsic XYZ orientation are queued, applied and confirmed before use; earlier queued motion keeps its frame, cancelled corrections do not leak into planning, and a tool/variant change clears the correction. The XYZ API stays and clears user rotation. Tool status reports its applied variant, so a calibration cannot silently bind to different jaws.
- **Bounded digital I/O** (#44). Reads and writes take a per-call deadline covering endpoint setup and retries; a missing read returns `None`, an unconfirmed write raises `TimeoutError`, and neither is mistaken for cancellation. Both facades advertise `io.digital`; dry-run output writes use logical indices and report dispatch errors.

#### Motion

- **Queued execution speed and explicit pause/resume** (#45). `set_execution_speed(0.1..1.0)` retimes the planned joint path; `pause()` decelerates to a hold with the queue retained and `resume()` continues at the selected speed, and changing speed while paused keeps the hold. Rate changes are checked against acceleration derived from the emitted positions, with preallocated buffers in the control loop; queued dwell pauses, while jog and servo-stream timing stay separate. Preview retimes durations and reports paused operations as unresolved. Physical transition tuning is unverified.
- **Held-object geometry under the flange** (#47). Only declared contact pairs are exempt; attach/detach requires confirmed whole-world application and invalid contact names keep the previous geometry. Reference or controller-context changes invalidate declarations and gate arm motion until explicit reconciliation or removal. The controller retains 1024 successful indices, including every command consumed by a blend.

#### Status surface

- **Session and timing metadata on every status frame** (#46): a nonzero session id, publication sequence and monotonic snapshot timestamp, so a client can record observation cadence and detect a controller restart. Missing metadata is explicitly unavailable. The offline client's no-tool identity matches the native controller.
- **Queue readback includes accepted commands** still waiting for planning or paused (#48), and clears completed or cancelled indices, so a supervised restart can tell whether the controller still has pending work. Restart detection also watches status broadcasts when the command socket goes quiet after a peer reset.

#### Dependencies

- **interpolatepy is gone.** Both profiles it supplied were only ever asked for rest-to-rest motion, so the trapezoidal and quintic curves are now evaluated here in closed form, across a numpy array rather than one Python call per sample. Positions match the previous output to within a thousandth of a motor step. This also removes a compiled dependency that, as of its 3.3.0, ships no Windows or Python 3.14 wheels.

### v0.7.0 — 2026-09-04

Everything since **0.3.2**, the last release. Four tags landed in between without notes, so this collects them. Pre-1.0, so breaking changes bump the minor.

#### Breaking changes

- **`RobotError` comes from waldoctl** rather than being defined here. A frontend represents a refusal the same way whichever backend raised it. It is an exception now, not a frozen dataclass, so a client can raise it as-is; anything that built one positionally or called `dataclasses.replace` on it needs updating. Tool-error attribution rebuilds the error from its wire form for exactly that reason.
- **`stop`, `estop` and `reset` replace `halt` and `resume`**, and a stop cancels the whole motion pipeline rather than just the active command.
- **`home(calibrate=)` replaces the separate CALIBRATE command.** Unhomed, or with `calibrate=True`, the arm runs the full end-stop referencing sequence; already homed, it takes a planned collision-checked move back to standby.
- **Planned motion is refused while unhomed.** Jogging stays available.
- **The waldoctl pin moves v0.7.0 → v0.12.0**, which removes the `Plane` keep-out shape. Persisted worlds containing a plane now raise on load.

#### Status surface

- **The control loop broadcasts its own health.** The p99 period and the deadline-miss count ride every STATUS frame in a `loop_health` mapping, so a display no longer polls the loop-statistics query for them. `drive_health` sits beside it and stays empty on this backend: the drives report per-joint error flags, not analog registers, and empty distinguishes "no such sensor" from "all zero".
- **`StatusBuffer`, homing progress and loop statistics conform to waldoctl**, and homing progress now survives a cancel.
- **A hardware e-stop disables the controller**, rather than only halting motion.

#### Motion

- **Trajectory settling is gated on progress, not elapsed ticks.**
- **Fast-path home**: an already-referenced arm takes a planned return move instead of re-running the firmware seek.
- **Command indices stay monotonic across a reset.**
- **The dry-run snapshot carries the pending blend chain**, so a preview mid-blend matches what the runtime will execute.

#### Fixes and hygiene

- A system command's `Command_out` was clobbered in the same tick by the executor fallback.
- The MSG gripper is seated on the flange rather than inside the wrist, and its built-in camera mount is declared.
- Test fixes surfaced by loaded runners: the unreachable-client test takes a free port instead of adding to the live one, which overflowed past 65535; the loop-health comparison waits for a frame that has caught up instead of demanding two samples of a climbing counter be equal.
- Typing: scipy stubs pinned per Python version, stale suppressions dropped, sync tool wrappers typed as `SyncTool`.

### 0.3.2 — 2026-07-14

#### What's Changed
* Fix stale error poisoning unrelated wait_command calls by @Jepson2k in https://github.com/PCrnjak/PAROL6-python-API/pull/26

**Full Changelog**: https://github.com/PCrnjak/PAROL6-python-API/compare/v0.3.1...0.3.2

### v0.3.1 — 2026-07-09

#### What's Changed
* Bump waldoctl pin to v0.6.2 by @Jepson2k in https://github.com/PCrnjak/PAROL6-python-API/pull/25

**Full Changelog**: https://github.com/PCrnjak/PAROL6-python-API/compare/v0.3.0...v0.3.1

### v0.3.0 — 2026-07-09

#### What's Changed
* parol6: camera_spec in tool registry + StrEnum ToolType membership (commander-public-api base) by @Jepson2k in https://github.com/PCrnjak/PAROL6-python-API/pull/18
* parol6: plugin tools in every process registry + variant TCP rpy (panel-extensions stack) by @Jepson2k in https://github.com/PCrnjak/PAROL6-python-API/pull/19
* Panels → main: plugin tools + planner/status fixes by @Jepson2k in https://github.com/PCrnjak/PAROL6-python-API/pull/20
* fix: bump waldoctl pin to v0.4.0 (repairs red main) by @Jepson2k in https://github.com/PCrnjak/PAROL6-python-API/pull/22
* ci: scope push trigger to main (kill duplicate PR-branch runs) by @Jepson2k in https://github.com/PCrnjak/PAROL6-python-API/pull/23
* Collision checking: keep-out shapes, enablement gates, MoveIt-style invalidation by @Jepson2k in https://github.com/PCrnjak/PAROL6-python-API/pull/24
* chore: comment sweep (why-only comments) by @Jepson2k in https://github.com/PCrnjak/PAROL6-python-API/pull/21

**Full Changelog**: https://github.com/PCrnjak/PAROL6-python-API/compare/v0.2.7...v0.3.0

### v0.2.7 — 2026-05-14

First release with `setuptools_scm`-managed versioning. `pip install git+...@v0.2.7` now resolves to the matching version directly (no auto-bump dance, no tag/metadata drift).

#### Changes since v0.2.6

- Switch to `setuptools_scm` for dynamic versioning. The git tag is now the source of truth for the package version; `pyproject.toml` no longer carries a static `version = "..."` line. Removes `[tool.tbump]` and the `release.yml` workflow that auto-bumped on tag publish.

---

*Release notes written by Claude on the author's behalf.*

### v0.2.6 — 2026-05-14

#### Bug fixes

- Electric-gripper stall detection: terminate on stall when grasping, ignore PID hunting on clamped jaws, keep `move_active` set so subsequent commands don't short-circuit.
- `SetTcpOffset` now routes through the motion-planner subprocess (was applied controller-side only, leaving the planner with stale IK seeds).
- Failed tool actions clear stale error state and `command_index` so subsequent commands aren't blocked.
- `RobotClient.async_client` property removed (cross-loop foot-gun). Async users construct `AsyncRobotClient` directly. Minor API break.

#### Kinematics / motion

- TOPP-RA trajectory shake: njit'd IK-outlier smoother (median-filters IK output), denser IK sampling, sim-dt jitter fix.
- IK `max_iter` bumped 10 → 20 to help wrist-near-singular targets converge.
- Deterministic wrist-flip restart for IK branches that converge outside joint limits.

#### Dependencies

- pinokin pin bumped v0.1.5 → v0.1.6.

---

*Release notes written by Claude on the author's behalf.*
