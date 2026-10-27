# Day 3, Period 4: Pawns

## Learning objectives

By the end of this period, each pair can:

- Generate pawn pushes, including the two-step first move. **Measured by:** The pawn tests pass, and the start position gives 20 pseudo-legal moves.
- Explain why White pawns move toward row 0. **Measured by:** Exit ticket: "Row 0 is rank 8, so a White pawn on row 6 moves to row ..."

## The files

Files that grow this period:

- `move_generation.py`
- `test_move_generation.py`

Functions the pairs write this period:

- `pawn_pushes()` in `move_generation.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `pawn_pushes()` in `move_generation.py`

Moves a pawn one square forward if it is empty, and two squares from its starting row if both are empty. White pawns move toward row 0, because row 0 is rank 8. Pawns are the only pieces that move one way and capture another, which is why pushes get their own function.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
