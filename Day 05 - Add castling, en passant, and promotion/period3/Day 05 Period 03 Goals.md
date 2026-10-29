# Day 5, Period 3: En passant and the double step

## Learning objectives

By the end of this period, each student pair can:

- Capture en passant on the very next move only. **Measured by:** The en passant tests pass, including the capture that is legal only once.
- Find the square of the pawn an en passant capture removes. **Measured by:** The student pair names the removed pawn's square for exd6 (d5) on the printed board.

## The files

Files that grow this period:

- `make_move.py`
- `move_generation.py`
- `test_special_moves.py`

Functions the student pairs write this period:

- `en_passant_victim_square()` in `make_move.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `en_passant_victim_square()` in `make_move.py`

Returns the square of the pawn that an en passant capture removes: the capturer's starting row and the landing column. It is the only capture where the victim is not on the landing square.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | Chess refresher: en passant is allowed only on the very next move after a two-square push, and the captured pawn is not on the destination square. |
| 1:15 to 1:30 | Slides: the double step sets the en passant target. The teacher walks through the en passant make and undo. |
| 1:30 to 1:55 | Student pairs write `en_passant_victim_square()`, then trace a capture and its undo on the printed board. |
| 1:55 to 2:20 | Student pairs run the en passant tests, including the rare capture that exposes the king along the rank. |
| 2:20 to 2:30 | Wrap-up: which square does the undo put the captured pawn back on? |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `make_move.py` | `en_passant_victim_square()` | 48 | 1 | `run_tests.py` |

Lines to type in all: 1. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
