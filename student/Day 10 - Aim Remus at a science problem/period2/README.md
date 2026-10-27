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

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `beam_time.py` | `estimate()` | 70 | 3 | `test_beam_time.py::test_four_readings_halve_the_error` |
| `beam_time.py` | `expected_wrong_calls()` | 104 | 7 | `test_beam_time.py::test_unmeasured_samples_count_as_coin_flips` |

Lines to type in all: 10. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` line. Delete those three lines and write the body in their place.
