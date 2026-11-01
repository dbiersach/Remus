# Day 2: Functions and records

Day 2 teaches functions, tests, dicts, and dataclasses, then uses them for the heart of every chess engine: making a move and taking it back exactly. By 4:30 Remus holds a whole game state, and ten moves made and undone return the exact start state.

## Objectives for the day

By 4:30, each student pair can:

- Write a function with type hints and a docstring, and check it with `assert` and pytest.
- Store named facts in a dict and a dataclass, and show why `b2 = board` gives one board two names instead of making a copy.
- Name the parts of a game state: the board, the side to move, castling rights, the en passant square, the two clocks, and the history.
- Turn a move into UCI text such as `e2e4` and back.
- Make a move, record everything it destroys, and undo it exactly.

## The day at a glance

| Period | Time | Title | Student pairs write |
| --- | --- | --- | --- |
| P1 | 8:30 to 10:00 | Python lab 3: functions, type hints, tuples, assert, pytest | The lab `python_functions.py` (16 lines) |
| | 10:00 to 10:30 | Break | |
| P2 | 10:30 to 12:00 | Python lab 4: dicts, dataclasses, aliasing, copying | The lab `python_dicts.py` (18 lines) |
| | 12:00 to 1:00 | Lunch | |
| P3 | 1:00 to 2:30 | game_state.py and moves.py: a game state and a move record | `is_white()` in `game_state.py` (1 line); `color_of()` in `game_state.py` (5 lines); `move_to_uci()` in `moves.py` (4 lines); `move_from_uci()` in `moves.py` (6 lines) |
| | 2:30 to 3:00 | Break | |
| P4 | 3:00 to 4:30 | make_move.py: make and undo ordinary moves | `make_move()` in `make_move.py` (23 lines); `undo_move()` in `make_move.py` (9 lines) |

## Period 1, 8:30 to 10:00: Python lab 3: functions, type hints, tuples, assert, pytest

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Slides: functions, parameters, `return`, type hints, and docstrings. |
| 8:45 to 9:25 | Student pairs work through Parts #1 to #3 of `python_functions.py`: call a function, write their own, and unpack a square tuple such as `row, col = (6, 4)`. |
| 9:25 to 9:35 | Slides: `assert` and pytest. A slide shows a function with a mistake in it, and the class reads the failing test together. |
| 9:35 to 9:50 | Student pairs finish Part #4, which checks their functions with `assert`. |
| 9:50 to 10:00 | Wrap-up: each student pair says what a failing test tells them and where to look first. |

[`Day_02_Period_01_Goals.md`](period1/Day_02_Period_01_Goals.md) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 2, 10:30 to 12:00: Python lab 4: dicts, dataclasses, aliasing, copying

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Slides: a dict holds named facts, and a dataclass describes a record with fixed fields. |
| 10:45 to 11:15 | Student pairs work through Parts #1 and #2 of `python_dicts.py` and watch `b2 = board` change both boards. |
| 11:15 to 11:50 | The teacher explains aliasing on the whiteboard: two names, one list. Then student pairs write Parts #3 and #4: a real copy, and a dataclass that describes a move. |
| 11:50 to 12:00 | Wrap-up: why would a chess engine break if it changed a board it meant to copy? |

[`Day_02_Period_02_Goals.md`](period2/Day_02_Period_02_Goals.md) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 3, 1:00 to 2:30: game_state.py and moves.py: a game state and a move record

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | Slides: the game state dict in `new_game()` and the `Move` dataclass with `from_square`, `to_square`, and `promotion`. |
| 1:15 to 2:05 | Student pairs write `is_white()` and `color_of()` in `game_state.py`, then `move_to_uci()` and `move_from_uci()` in `moves.py`, running `run_tests.py` after each. |
| 2:05 to 2:15 | Student pairs run `game_state.py` and `moves.py` and compare the printouts with the expected answers. |
| 2:15 to 2:30 | Show and choose: the class picks one `move_from_uci()`, and the teacher adds its student pair's team name to `CONTRIBUTORS.md`. |

[`Day_02_Period_03_Goals.md`](period3/Day_02_Period_03_Goals.md) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 4, 3:00 to 4:30: make_move.py: make and undo ordinary moves

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Unplugged warm-up, "Undo from the card": one partner makes three moves with sticky-note pieces and writes an undo card for each. The other partner restores the start position from the cards alone. |
| 3:15 to 3:25 | Slides: what a move destroys (the captured piece, the clocks, the side to move) and the undo record that saves it. The teacher shows `state_snapshot()` and the "make ten, undo ten, compare" test. |
| 3:25 to 4:15 | Student pairs write `make_move()` and `undo_move()` in `make_move.py` until the tests pass. |
| 4:15 to 4:30 | Show and choose for `make_move()`, then the checkpoint: ten moves made and undone give back the exact start state. |

[`Day_02_Period_04_Goals.md`](period4/Day_02_Period_04_Goals.md) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## By the end of the day

**Checkpoint:** Ten moves made and undone return the exact start state, and `test_make_move.py` passes.

Each period folder starts from working code, so a student pair that falls behind opens the next period's folder with the rest of the class.
