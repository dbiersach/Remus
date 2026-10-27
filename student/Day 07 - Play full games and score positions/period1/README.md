# Day 7, Period 1: Ending the game

## Learning objectives

By the end of this period, each pair can:

- Name every way a game ends: checkmate, stalemate, insufficient material, repetition, and the fifty-move rule. **Measured by:** Six-position quiz: each pair gets at least five right.
- Detect the end of a game in code. **Measured by:** The game-end tests in `test_game.py` pass for all five endings.

## The files

New files this period:

- `game_end.py`

Files that grow this period:

- `fen.py`
- `game_state.py`
- `make_move.py`
- `test_game.py`

Functions the pairs write this period:

- `insufficient_material()` in `game_end.py`
- `game_result()` in `game_end.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `insufficient_material()` in `game_end.py`

Returns True when neither side can ever checkmate: kings alone, a king with one bishop or knight, or bishops that all stand on squares of one color. The bishops' square colors come from (row + col) % 2.

### `game_result()` in `game_end.py`

Checks every way a game ends, in order: no legal moves (checkmate or stalemate), insufficient material, threefold repetition, and the fifty-move rule. It returns the result and the reason, so the console and the GUI can say why a game is over.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `game_end.py` | `insufficient_material()` | 17 | 15 | `test_game.py::test_insufficient_material` |
| `game_end.py` | `game_result()` | 42 | 12 | `test_game.py::test_checkmate_and_stalemate`, `test_game.py::test_threefold_repetition_and_undo`, `test_game.py::test_fifty_move_rule` |

Lines to type in all: 27. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` line. Delete those three lines and write the body in their place.
