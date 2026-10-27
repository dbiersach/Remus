# Day 7, Period 4: What makes a position good? Material and piece-square tables

## Learning objectives

By the end of this period, each pair can:

- Count material in centipawns. **Measured by:** The evaluation tests pass, and `uv run evaluation.py` prints -200 for a knight against a rook.
- Explain a piece-square table. **Measured by:** The pair says why a knight scores more on d4 than on a1, using the number of squares it attacks (8 and 2).

## The files

New files this period:

- `evaluation.py`
- `test_search.py`

Functions the pairs write this period:

- `material()` in `evaluation.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `material()` in `evaluation.py`

Adds up the pieces in centipawns (pawn 100, knight 300, bishop 300, rook 500, queen 900), plus for White and minus for Black. It is the first evaluation term, and the search uses it to tell good positions from bad ones.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
