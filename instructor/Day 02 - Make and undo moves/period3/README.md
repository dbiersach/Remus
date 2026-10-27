# Day 2, Period 3: game_state.py and moves.py: a game state and a move record

## Learning objectives

By the end of this period, each pair can:

- Tell the color of a piece, and handle an empty square. **Measured by:** The `is_white` and `color_of` tests in `test_make_move.py` pass, including `None` for `.`.
- Write a move as UCI text and read it back. **Measured by:** `move_to_uci` and `move_from_uci` round-trip `e2e4` and `e7e8q`.
- Name the fields of a game state. **Measured by:** Exit ticket: list the six fields of the state dict and what each holds.

## The files

New files this period:

- `game_state.py`
- `moves.py`
- `test_make_move.py`

Files that grow this period:

- `board.py`

Functions the pairs write this period:

- `is_white()` in `game_state.py`
- `color_of()` in `game_state.py`
- `move_to_uci()` in `moves.py`
- `move_from_uci()` in `moves.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `is_white()` in `game_state.py`

Returns True for an uppercase letter. Remus follows FEN, where uppercase is White and lowercase is Black, so one call to `isupper()` tells the colors apart.

### `color_of()` in `game_state.py`

Returns "w", "b", or None for an empty square. Move generation asks this about every square a piece might land on: a friend blocks the move, an enemy can be captured, and None means the square is free.

### `move_to_uci()` in `moves.py`

Writes a move as text such as e2e4, adding a lowercase piece letter for a promotion (e7e8q). UCI is the language Lucas Chess speaks, so this is how Remus tells the GUI which move it chose.

### `move_from_uci()` in `moves.py`

Reads text such as e7e8q back into a Move. The promotion letter becomes uppercase for White and lowercase for Black, so the new piece gets the right color on the board.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
