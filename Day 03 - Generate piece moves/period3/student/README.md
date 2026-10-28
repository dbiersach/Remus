# Day 3, Period 3: Sliding pieces: rooks, bishops, and queens

## Learning objectives

By the end of this period, each pair can:

- Slide a rook, bishop, or queen until a piece or the edge stops it. **Measured by:** The slider tests pass: a rook on d4 of an empty board has 14 moves.
- Explain why a slider may land on an enemy piece but not on a friend. **Measured by:** The pair traces `slide()` by hand on a board with one friend and one enemy.

## The files

Files that grow this period:

- `move_generation.py`
- `test_move_generation.py`

Functions the pairs write this period:

- `slide()` in `move_generation.py`

In the `student` folder these functions raise `NotImplementedError` until a pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `slide()` in `move_generation.py`

Walks one direction from a square, adding a move for each empty square, and stops at the edge or at the first piece. An enemy piece can be captured, so its square is added before the walk stops; a friendly piece is not. Rooks, bishops, and queens all use this walk with different directions.

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `move_generation.py` | `slide()` | 70 | 14 | `test_move_generation.py::test_slide_stops_at_a_friend_and_captures_an_enemy` |

Lines to type in all: 14. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
