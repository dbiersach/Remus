# Day 10, Period 3: The beamline problem: look ahead and verify

## Learning objectives

By the end of this period, each pair can:

- Look ahead with pretend readings, the way Remus looks ahead with moves. **Measured by:** The `gain` test passes: a close call (52) gains more from a shot than a clear one (90).
- Verify a model by comparing its predictions with results. **Measured by:** `uv run beam_time.py` shows largest gain beating equal time, and the pair compares each expected count with the real count.

## The files

Files that grow this period:

- `beam_time.py`
- `test_beam_time.py`

Functions the pairs write this period:

- `gain()` in `beam_time.py`
- `choose_next_sample()` in `beam_time.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `gain()` in `beam_time.py`

Looks one shot ahead: tries three pretend readings (one noise step low, on the average, one step high), averages the chance of a wrong call after each, and returns how much the chance drops. Pretend readings are like the moves Remus makes and undoes while it searches.

### `choose_next_sample()` in `beam_time.py`

Returns the sample whose next shot has the largest gain. With it, the agent spends beam time where a call is still close, and makes fewer wrong calls than giving every sample equal time.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `beam_time.py` | `gain()` | 133 | 8 | `test_beam_time.py::test_gain_favors_a_close_call_over_a_safe_one` |
| `beam_time.py` | `choose_next_sample()` | 161 | 1 | `test_beam_time.py::test_the_agent_measures_every_sample_once_first`, `test_beam_time.py::test_largest_gain_beats_equal_time` |

Lines to type in all: 9. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` line. Delete those three lines and write the body in their place.
