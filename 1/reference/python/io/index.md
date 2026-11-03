# I/O

The control board's digital inputs and outputs. The firmware's I/O byte is `[in1, in2, out1, out2, estop, ...]`;
reads return the first five, writes take the logical output index 0 or 1. [I/O, delays and checkpoints](https://docs.source-robotics.com/PAROL-docs/1/programming/02-python-api/io-and-delays/)
in the guide.

### `write_io` 

```python
rbt.write_io(index: int, value: int, *, timeout: float | None = None) -> int
```

Set digital output by logical index (0 = first output pin).

The firmware I/O byte layout is `[in0, in1, out0, out1, estop, ...]` so logical output index 0 maps to bit position 2.

Returns the command index (≥ 0) on success, -1 on failure.

`timeout` bounds command acceptance. TimeoutError leaves application unconfirmed; None uses the client defaults.

```python
rbt.write_io(0, 1)   # Set first output HIGH
```

The read side is `io()` under [Queries](https://docs.source-robotics.com/PAROL-docs/1/reference/python/queries/#io), and `is_estop_pressed()`.
