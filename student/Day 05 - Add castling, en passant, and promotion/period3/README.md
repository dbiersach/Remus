# Day 5, Period 3: En passant and the double step

## Learning objectives

By the end of this period, each pair can:

- Capture en passant on the very next move only. **Measured by:** The en passant tests pass, including the capture that is legal only once.
- Find the square of the pawn an en passant capture removes. **Measured by:** The pair names the removed pawn's square for exd6 (d5) on the printed board.

## The files

Files that grow this period:

- `make_move.py`
- `move_generation.py`
- `test_special_moves.py`

Functions the pairs write this period:

- `en_passant_victim_square()` in `make_move.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `en_passant_victim_square()` in `make_move.py`

Returns the square of the pawn that an en passant capture removes: the capturer's starting row and the landing column. It is the only capture where the victim is not on the landing square.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `make_move.py` | `en_passant_victim_square()` | 48 | 1 | `uv run pytest` |

Lines to type in all: 1. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` line. Delete those three lines and write the body in their place.
