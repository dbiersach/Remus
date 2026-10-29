# Day 7, Period 1: Ending the game

## Learning objectives

By the end of this period, each student pair can:

- Name every way a game ends: checkmate, stalemate, insufficient material, repetition, and the fifty-move rule. **Measured by:** Six-position quiz: each student pair gets at least five right.
- Detect the end of a game in code. **Measured by:** The game-end tests in `test_game.py` pass for all five endings.

## The files

New files this period:

- `game_end.py`

Files that grow this period:

- `fen.py`
- `game_state.py`
- `make_move.py`
- `test_game.py`

Functions the student pairs write this period:

- `insufficient_material()` in `game_end.py`
- `game_result()` in `game_end.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `insufficient_material()` in `game_end.py`

Returns True when neither side can ever checkmate: kings alone, a king with one bishop or knight, or bishops that all stand on light squares, or all on dark squares. A square is light or dark by (row + col) % 2.

### `game_result()` in `game_end.py`

Checks every way a game ends, in order: no legal moves (checkmate or stalemate), insufficient material, threefold repetition, and the fifty-move rule. It returns the result and the reason, so the console and the GUI can say why a game is over.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 8:30 to 8:50 | Chess refresher: stalemate, repetition, the fifty and 75-move rules, and insufficient material, with a six-position quiz. |
| 8:50 to 9:00 | Slides: the halfmove clock and `position_key()`, which the teacher writes. |
| 9:00 to 9:45 | Student pairs write `insufficient_material()` and `game_result()` in `game_end.py`. |
| 9:45 to 10:00 | Student pairs check their answers on the quiz positions, then show and choose. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `game_end.py` | `insufficient_material()` | 17 | 18 | `test_game.py::test_insufficient_material` |
| `game_end.py` | `game_result()` | 42 | 12 | `test_game.py::test_checkmate_and_stalemate`, `test_game.py::test_threefold_repetition_and_undo`, `test_game.py::test_fifty_move_rule` |

Lines to type in all: 30. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
