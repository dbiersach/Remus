# Day 9, Period 4: The mate solver

## Learning objectives

By the end of this period, each pair can:

- Solve mate puzzles with a yes-or-no search. **Measured by:** The mate-solver tests pass on all ten GameWorks puzzles.

## The files

New files this period:

- `mate_solver.py`

Files that grow this period:

- `test_search.py`

Functions the pairs write this period:

- `mating_move()` in `mate_solver.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `mating_move()` in `mate_solver.py`

Looks for a move after which every defense still loses to a mate in one move fewer. On the last move only checks are tried, because only a check can be mate. A yes-or-no question is much faster to answer than a full search with scores.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `mate_solver.py` | `mating_move()` | 29 | 22 | `test_search.py::test_mate_solver_solves_all_gameworks_puzzles`, `test_search.py::test_mate_solver_finds_no_mate_when_there_is_none` |

Lines to type in all: 22. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
