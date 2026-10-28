# Day 10, Period 3: The phase hunt: search every set, and verify

## Learning objectives

By the end of this period, each pair can:

- Search every set of phases with make and undo, as Remus searches moves. **Measured by:** The `search` tests pass: the phases list comes back unchanged, and the search scores 176 sets, one for each set of up to three phases.
- Verify a method against known answers, and say when the data cannot decide. **Measured by:** `uv run phase_hunt.py` shows the search making fewer wrong calls than greedy, and the pair names the extra measurement that would tell gold from silver.

## The files

Files that grow this period:

- `phase_hunt.py`
- `test_phase_hunt.py`

Functions the pairs write this period:

- `search()` in `phase_hunt.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `search()` in `phase_hunt.py`

Scores the set of phases it is given, keeps every set that ties for the best score, and calls itself on each set one phase larger, adding a phase with append and taking it back with pop. Phases go in library order only, so each set is scored once instead of once for every order, 176 sets instead of 821. Keeping every tied set lets the search say gold or silver when the pattern cannot tell them apart, as CrystalShift and Dara report every likely answer.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `phase_hunt.py` | `search()` | 187 | 13 | `test_phase_hunt.py::test_search_leaves_the_phases_as_it_found_them` |

Lines to type in all: 13. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
