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

In the `student` folder these functions raise `NotImplementedError` until a pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `pawn_pushes()` in `move_generation.py`

Moves a pawn one square forward if it is empty, and two squares from its starting row if both are empty. White pawns move toward row 0, because row 0 is rank 8. Pawns are the only pieces that move one way and capture another, which is why pushes get their own function.

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).
