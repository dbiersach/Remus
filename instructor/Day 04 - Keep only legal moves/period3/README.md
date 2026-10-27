# Day 4, Period 3: Check and the legal filter

## Learning objectives

By the end of this period, each pair can:

- Tell whether a king is in check. **Measured by:** The `in_check` tests pass in check and out of check.
- Keep only legal moves by making each move, testing the king, and undoing it. **Measured by:** The legal-move tests pass: 20 moves from the start, only escapes in check, and no moves for a pinned knight.

## The files

New files this period:

- `legal_moves.py`

Files that grow this period:

- `attacks.py`
- `test_legal_moves.py`

Functions the pairs write this period:

- `in_check()` in `attacks.py`
- `legal_moves()` in `legal_moves.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `in_check()` in `attacks.py`

Finds the king of one color and asks whether the other color attacks its square. Check decides which moves are legal, whether a game is over, and later how deep the search looks.

### `legal_moves()` in `legal_moves.py`

Tries every pseudo-legal move: makes it, keeps it if the mover's king is not in check, and undoes it. Testing after the move catches pins and discovered checks without any special rules, which is why the code is so short.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
