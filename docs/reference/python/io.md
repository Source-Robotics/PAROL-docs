# I/O

The control board's digital inputs and outputs. The firmware's I/O byte is `[in1, in2, out1, out2, estop, ...]`;
reads return the first five, writes take the logical output index 0 or 1. [I/O, delays and checkpoints](../../programming/02-python-api/io-and-delays.md)
in the guide.

<!-- api: write_io -->

The read side is `io()` under [Queries](queries.md#io), and `is_estop_pressed()`.
