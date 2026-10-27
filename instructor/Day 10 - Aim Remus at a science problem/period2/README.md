# Day 10, Period 2: The beamline problem: represent and evaluate

`uv run beam_time.py` spends 40 shots of beam time on 8 samples and counts the wrong calls over 200 sample holders.

## Learning objectives

By the end of this period, each pair can:

- Estimate a value and its error from noisy readings. **Measured by:** The `estimate` test passes: four readings cut the error in half.
- Score an experiment by the wrong calls to expect. **Measured by:** The `expected_wrong_calls` test passes, and the pair explains why an unmeasured sample counts as 0.5.

## The files

New files this period:

- `beam_time.py`
- `test_beam_time.py`

Functions the pairs write this period:

- `estimate()` in `beam_time.py`
- `expected_wrong_calls()` in `beam_time.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `estimate()` in `beam_time.py`

Averages a sample's readings and works out the error: the noise divided by the square root of the number of readings. Four readings cut the error in half, which is why some samples deserve more shots.

### `expected_wrong_calls()` in `beam_time.py`

Adds up the chance of a wrong call over all eight samples. It is the evaluation of the experiment, like `material()` for a chess position: a smaller total means a better plan.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
