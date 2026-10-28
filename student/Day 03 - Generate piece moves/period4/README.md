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

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `move_generation.py` | `pawn_pushes()` | 130 | 11 | `test_move_generation.py::test_pawn_pushes_from_the_start_rank`, `test_move_generation.py::test_blocked_pawn_has_no_pushes`, `test_move_generation.py::test_pawn_promotes_to_four_pieces` |

Lines to type in all: 11. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
