# Day 3, Period 2: Jumping pieces: knights and kings

`uv run show_board.py` draws an arrow for every move a generator returns.

## Learning objectives

By the end of this period, each pair can:

- Generate knight and king moves from a list of jumps. **Measured by:** The jumping-piece tests pass: a knight on a1 has 2 moves and a king on a1 has 3.
- See the moves a generator returns. **Measured by:** `uv run show_board.py` draws one arrow per king move, and the pair counts the arrows.

## The files

New files this period:

- `move_generation.py`
- `test_move_generation.py`

Files that grow this period:

- `show_board.py`

Functions the pairs write this period:

- `king_moves()` in `move_generation.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `king_moves()` in `move_generation.py`

Hands the king's eight one-step jumps to `jump_moves()`, which the knight uses too. Two pieces share one helper because both jump to fixed squares; only their list of jumps differs.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
