# Day 2, Period 3: game_state.py and moves.py: a game state and a move record

## Learning objectives

By the end of this period, each pair can:

- Tell the piece color of a piece, and handle an empty square. **Measured by:** The `is_white` and `color_of` tests in `test_make_move.py` pass, including `None` for `.`.
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

In the `student` folder these functions raise `NotImplementedError` until a pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `is_white()` in `game_state.py`

Returns True for an uppercase letter. Remus follows FEN, where uppercase is White and lowercase is Black, so one call to `isupper()` tells the piece colors apart.

### `color_of()` in `game_state.py`

Returns "w", "b", or None for an empty square. Move generation asks this about every square a piece might land on: a friend blocks the move, an enemy can be captured, and None means the square is free.

### `move_to_uci()` in `moves.py`

Writes a move as text such as e2e4, adding a lowercase piece letter for a promotion (e7e8q). UCI is the language Lucas Chess speaks, so this is how Remus tells the GUI which move it chose.

### `move_from_uci()` in `moves.py`

Reads text such as e7e8q back into a Move. The promotion letter becomes uppercase for White and lowercase for Black, so the new piece gets the right piece color on the board.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | Slides: the game state dict in `new_game()` and the `Move` dataclass with `from_square`, `to_square`, and `promotion`. |
| 1:15 to 2:05 | Pairs write `is_white()` and `color_of()` in `game_state.py`, then `move_to_uci()` and `move_from_uci()` in `moves.py`, running `run_tests.py` after each. |
| 2:05 to 2:15 | Pairs run `game_state.py` and `moves.py` and compare the printouts with the expected answers. |
| 2:15 to 2:30 | Show and choose: the class picks one `move_from_uci()` for the class repository. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `game_state.py` | `is_white()` | 38 | 1 | `run_tests.py` |
| `game_state.py` | `color_of()` | 45 | 5 | `test_make_move.py::test_colors` |
| `moves.py` | `move_to_uci()` | 28 | 4 | `test_make_move.py::test_uci_round_trip` |
| `moves.py` | `move_from_uci()` | 47 | 6 | `test_make_move.py::test_uci_round_trip`, `test_make_move.py::test_move_record_holds_squares` |

Lines to type in all: 16. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
