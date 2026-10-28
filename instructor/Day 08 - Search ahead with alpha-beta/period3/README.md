# Day 8, Period 3: The horizon effect and quiescence

## Learning objectives

By the end of this period, each pair can:

- Explain the horizon effect. **Measured by:** The pair explains why depth 2 takes a defended pawn with the queen.
- List the moves quiescence searches. **Measured by:** The `quiescence` tests pass, and the pair explains what "stand pat" means with the defended-pawn position.

## The files

Files that grow this period:

- `search.py`
- `test_search.py`

Functions the pairs write this period:

- `quiescence()` in `search.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `quiescence()` in `search.py`

Keeps searching captures after the depth runs out, so Remus never judges a position in the middle of a trade. The mover may "stand pat" and take the evaluation as it is, or try a capture that does better. Without it, a search that stops after queen takes pawn misses the pawn that takes the queen back.

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).
