# Day 3, Period 2: Jumping pieces: knights and kings

Running `show_board.py` draws an arrow for every move a generator returns.

## Learning objectives

By the end of this period, each student pair can:

- Generate knight and king moves from a list of jumps. **Measured by:** The jumping-piece tests pass: a knight on a1 has 2 moves and a king on a1 has 3.
- See the moves a generator returns. **Measured by:** Running `show_board.py` draws one arrow per king move, and the student pair counts the arrows.

## The files

New files this period:

- `move_generation.py`
- `test_move_generation.py`

Files that grow this period:

- `show_board.py`

Functions the student pairs write this period:

- `king_moves()` in `move_generation.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `king_moves()` in `move_generation.py`

Hands the king's eight one-step jumps to `jump_moves()`, which the knight uses too. Two pieces share one helper because both jump to fixed squares; only their list of jumps differs.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Unplugged warm-up, "Shade the reach": student pairs shade every square a knight on d4, a knight on a1, and a bishop on c1 can reach, and compare counts with the next student pair (8, 2, and 7). |
| 10:45 to 11:00 | Slides: an offset list for the knight. The teacher writes `knight_moves()` on the projector. |
| 11:00 to 11:20 | Student pairs write `king_moves()` the same way and pass the jumping-piece tests: a knight on a1 has 2 moves and a king on a1 has 3. |
| 11:20 to 11:40 | Student pairs run `show_board.py`, which draws an arrow for every move their generator returns, and count the arrows. |
| 11:40 to 12:00 | Student pairs try their own squares, such as a king in a corner, and predict the arrows before they run the file. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `move_generation.py` | `king_moves()` | 62 | 1 | `test_move_generation.py::test_king_in_the_corner_has_three_moves` |

Lines to type in all: 1. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `king_moves()` in `move_generation.py`

**Where:** lines 64 to 64 of `move_generation.py`, inside `king_moves()`, in place of the stub below the docstring. The tests call it directly.

```text
62 | def king_moves(board: Board, square: Square, color: str) -> list[Move]:
63 |     """Return the one-step moves of a king on the square (castling comes later)."""
64 +     return jump_moves(board, square, color, KING_STEPS)
65 |
66 |
67 | def main():
```
