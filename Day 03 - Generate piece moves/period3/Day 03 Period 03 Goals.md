# Day 3, Period 3: Sliding pieces: rooks, bishops, and queens

## Learning objectives

By the end of this period, each student pair can:

- Slide a rook, bishop, or queen until a piece or the edge stops it. **Measured by:** The slider tests pass: a rook on d4 of an empty board has 14 moves.
- Explain why a slider may land on an enemy piece but not on a friend. **Measured by:** The student pair traces `slide()` by hand on a board with one friend and one enemy.

## The files

Files that grow this period:

- `move_generation.py`
- `test_move_generation.py`

Functions the student pairs write this period:

- `slide()` in `move_generation.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `slide()` in `move_generation.py`

Walks one direction from a square, adding a move for each empty square, and stops at the edge or at the first piece. An enemy piece can be captured, so its square is added before the walk stops; a friendly piece is not. Rooks, bishops, and queens all use this walk with different directions.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | Slides: a sliding piece walks one direction until the edge or the first piece, and captures that piece only if it is an enemy. |
| 1:15 to 2:00 | Student pairs write `slide()` in `move_generation.py`. The teacher's `slider_moves()` calls it with the rook, bishop, and queen directions. |
| 2:00 to 2:15 | Exercise: a rook on an empty board has 14 moves. Student pairs check it with the tests and the arrow picture. |
| 2:15 to 2:30 | Show and choose for `slide()`. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `move_generation.py` | `slide()` | 70 | 14 | `test_move_generation.py::test_slide_stops_at_a_friend_and_captures_an_enemy` |

Lines to type in all: 14. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `slide()` in `move_generation.py`

**Where:** lines 91 to 104 of `move_generation.py`, inside `slide()`, in place of the stub below the docstring. It is called by `slider_moves()` in `move_generation.py`.

```text
 70 | def slide(board: Board, square: Square, direction: Direction, color: str) -> list[Move]:
      ...
 89 |         that piece is an enemy, the capture is the last move in the list.
 90 |     """
 91 +     row, col = square
 92 +     row_change, col_change = direction
 93 +     moves = []
 94 +     row, col = row + row_change, col + col_change
 95 +     while on_board(row, col):
 96 +         target_piece = piece_at(board, (row, col))
 97 +         if target_piece == EMPTY:
 98 +             moves.append(Move(square, (row, col)))
 99 +         else:
100 +             if color_of(target_piece) != color:
101 +                 moves.append(Move(square, (row, col)))
102 +             break
103 +         row, col = row + row_change, col + col_change
104 +     return moves
105 |
106 |
107 | def slider_moves(
```

**How it works:** The function unpacks the start square and the direction, then takes its first step. The `while` loop runs while the square is on the board. An empty square is a move, and the walk goes on. A square with a piece ends the walk: an enemy piece is one last move, a capture, and a friendly piece is not a move at all. The last line of the loop takes the next step.
