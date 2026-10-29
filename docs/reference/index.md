# API reference

Where you look things up. The Python API pages are generated from the API's source at <!-- api-version -->: the
signature and the docstring of every public method of `RobotClient`, the tool methods, the registered tools, the
error codes, the environment variables and the controller's options, with notes written around them. The build
fails when a page names a method the API no longer has, and the tests fail when a method is on no page.

<div class="grid cards" markdown>

-   :material-language-python:{ .lg .middle } **Python API**

    ---

    [Every method by category](python/index.md): [motion](python/motion.md), [jogging and servoing](python/streaming.md),
    [control](python/control.md), [queries](python/queries.md), [synchronization](python/synchronization.md),
    [tools](python/tools.md), [I/O](python/io.md), [configuration](python/configuration.md), the
    [status fields](python/status.md), the [errors](python/errors.md), [the controller](python/controller.md).

-   :material-script-text:{ .lg .middle } **RBTscript**

    ---

    [Every command](rbtscript.md) of the commander's program language, with its arguments.

-   :material-swap-horizontal:{ .lg .middle } **The serial protocol**

    ---

    [The packets](serial-protocol.md) between the PC and the control board, byte by byte, and the command codes.

-   :material-tune:{ .lg .middle } **Firmware and test firmware**

    ---

    [The firmware's parameters](firmware-parameters.md) per joint, and [the test firmware's commands](test-firmware.md).

</div>
