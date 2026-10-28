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
