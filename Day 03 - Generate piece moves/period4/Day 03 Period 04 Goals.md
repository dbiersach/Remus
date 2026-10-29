# Day 3, Period 4: Pawns

## Learning objectives

By the end of this period, each student pair can:

- Generate pawn pushes, including the two-step first move. **Measured by:** The pawn tests pass, and the start position gives 20 pseudo-legal moves.
- Explain why White pawns move toward row 0. **Measured by:** Exit ticket: "Row 0 is rank 8, so a White pawn on row 6 moves to row ..."

## The files

Files that grow this period:

- `move_generation.py`
- `test_move_generation.py`

Functions the student pairs write this period:

- `pawn_pushes()` in `move_generation.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `pawn_pushes()` in `move_generation.py`

Moves a pawn one square forward if it is empty, and two squares from its starting row if both are empty. White pawns move toward row 0, because row 0 is rank 8. Pawns are the only pieces that move one way and capture another, which is why pushes get their own function.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Slides: pawns move forward toward row 0 for White, push one or two squares, and capture diagonally. The teacher writes the captures and the four promotion choices. |
| 3:15 to 3:55 | Student pairs write `pawn_pushes()`: the single step and the double step from the start rank. |
| 3:55 to 4:15 | Student pairs run the tests and the arrow picture on the start position. |
| 4:15 to 4:30 | Checkpoint: `pseudo_legal_moves()` finds 20 moves from the start. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `move_generation.py` | `pawn_pushes()` | 130 | 11 | `test_move_generation.py::test_pawn_pushes_from_the_start_rank`, `test_move_generation.py::test_blocked_pawn_has_no_pushes`, `test_move_generation.py::test_pawn_promotes_to_four_pieces` |

Lines to type in all: 11. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
