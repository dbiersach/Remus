# Day 1, Period 4: board.py: the board and its square names

Running `show_board.py` draws the board as a picture in the web browser.

## Learning objectives

By the end of this period, each pair can:

- Print the board with rank numbers and file letters. **Measured by:** Running `board.py` prints the start board with 8 at the top and a to h below it.
- Convert between square names and (row, col) in both directions. **Measured by:** `test_board.py` passes, including e2 to (6, 4) and back.
- Reject text that is not a square. **Measured by:** `parse_square("i9")` raises `ValueError`, and the pair explains which check catches it.

## The files

New files this period:

- `board.py`
- `show_board.py`
- `test_board.py`

Functions the pairs write this period:

- `print_board()` in `board.py`
- `square_name()` in `board.py`
- `parse_square()` in `board.py`
- `piece_at()` in `board.py`

In the `student` folder these functions raise `NotImplementedError` until a pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `print_board()` in `board.py`

Prints the board one row at a time, with the rank number at the left of each row and the file letters along the bottom. Row 0 is rank 8, so the first line printed is Black's back rank, the way a board looks from White's side. Every later day prints positions this way, so this is the window you look through to check your own code.

### `square_name()` in `board.py`

Turns (row, col) into a name such as e4 by looking up the file letter and the rank digit. The engine thinks in rows and columns, but people read square names, so every move Remus shows you goes through this one line.

### `parse_square()` in `board.py`

Does the reverse: turns e4 into (4, 4), and raises `ValueError` for text that is not a square, such as i9. Checking the input here means a typo stops at the door instead of causing a strange bug deep in the engine.

### `piece_at()` in `board.py`

Unpacks a square into its row and column and returns the piece there. Almost every rule in Remus asks "what is on this square?", so this tiny function is the one they all call.

Check the work with the tests: open a terminal in VS Code inside the `student` folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).

## The period step by step

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Slides: the Remus board is an 8x8 list of one-character strings. Uppercase is White, lowercase is Black, and `.` is empty. The teacher walks through `new_board()`. |
| 3:15 to 4:00 | Pairs write `print_board()`, `square_name()`, `parse_square()`, and `piece_at()` in `board.py` and run `uv run pytest` after each one. |
| 4:00 to 4:10 | Pairs run `show_board.py`, which draws their board as a picture in the web browser. |
| 4:10 to 4:25 | Show and choose: two or three pairs show their `parse_square()` on the projector, the class picks one for clarity, and the teacher adds it to the class repository with the pair's team name in `CONTRIBUTORS.md`. |
| 4:25 to 4:30 | Checkpoint: running `board.py` prints the start board and "b1 holds N, expected N". |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `board.py` | `print_board()` | 37 | 6 | `uv run pytest` |
| `board.py` | `square_name()` | 51 | 1 | `test_board.py::test_corners_round_trip`, `test_board.py::test_every_square_round_trips` |
| `board.py` | `parse_square()` | 72 | 5 | `test_board.py::test_e2_is_row_6_col_4`, `test_board.py::test_corners_round_trip`, `test_board.py::test_every_square_round_trips`, `test_board.py::test_bad_square_names_are_rejected`, `test_board.py::test_start_position_pieces` |
| `board.py` | `piece_at()` | 96 | 2 | `test_board.py::test_start_position_pieces` |

Lines to type in all: 14. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
