# Day 10, Period 2: The beamline problem: represent and evaluate

`uv run beam_time.py` spends 40 shots of beam time on 8 samples and counts the wrong calls over 200 sample holders.

New files this period:

- `beam_time.py`
- `test_beam_time.py`

Functions the pairs write this period:

- `estimate()` in `beam_time.py`
- `expected_wrong_calls()` in `beam_time.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
