# Day 1, Period 4: board.py: the board and its square names

Running `show_board.py` draws the board as a picture in the web browser.

## Learning objectives

By the end of this period, each student pair can:

- Print the board with rank numbers and file letters. **Measured by:** Running `board.py` prints the start board with 8 at the top and a to h below it.
- Convert between square names and (row, col) in both directions. **Measured by:** `test_board.py` passes, including e2 to (6, 4) and back.
- Reject text that is not a square. **Measured by:** `parse_square("i9")` raises `ValueError`, and the student pair explains which check catches it.

## The files

New files this period:

- `board.py`
- `show_board.py`
- `test_board.py`

Functions the student pairs write this period:

- `print_board()` in `board.py`
- `square_name()` in `board.py`
- `parse_square()` in `board.py`
- `piece_at()` in `board.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `print_board()` in `board.py`

Prints the board one row at a time, with the rank number at the left of each row and the file letters along the bottom. Row 0 is rank 8, so the first line printed is Black's back rank, the way a board looks from White's side. Every later day prints positions this way, so this is the window you look through to check your own code.

### `square_name()` in `board.py`

Turns (row, col) into a name such as e4 by looking up the file letter and the rank digit. The engine thinks in rows and columns, but people read square names, so every move Remus shows you goes through this one line.

### `parse_square()` in `board.py`

Does the reverse: turns e4 into (4, 4), and raises `ValueError` for text that is not a square, such as i9. Checking the input here means a typo stops at the door instead of causing a strange bug deep in the engine.

### `piece_at()` in `board.py`

Unpacks a square into its row and column and returns the piece there. Almost every rule in Remus asks "what is on this square?", so this tiny function is the one they all call.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Slides: the Remus board is an 8x8 list of one-character strings. Uppercase is White, lowercase is Black, and `.` is empty. The teacher walks through `new_board()`. |
| 3:15 to 4:00 | Student pairs write `print_board()`, `square_name()`, `parse_square()`, and `piece_at()` in `board.py` and run `run_tests.py` after each one. |
| 4:00 to 4:10 | Student pairs run `show_board.py`, which draws their board as a picture in the web browser. |
| 4:10 to 4:25 | Show and choose: two or three student pairs show their `parse_square()` on the projector, the class picks one for clarity, and the teacher adds it to the class repository with the student pair's team name in `CONTRIBUTORS.md`. |
| 4:25 to 4:30 | Checkpoint: running `board.py` prints the start board and "b1 holds N, expected N". |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `board.py` | `print_board()` | 37 | 6 | `run_tests.py` |
| `board.py` | `square_name()` | 56 | 1 | `test_board.py::test_corners_round_trip`, `test_board.py::test_every_square_round_trips` |
| `board.py` | `parse_square()` | 75 | 5 | `test_board.py::test_e2_is_row_6_col_4`, `test_board.py::test_corners_round_trip`, `test_board.py::test_every_square_round_trips`, `test_board.py::test_bad_square_names_are_rejected`, `test_board.py::test_start_position_pieces` |
| `board.py` | `piece_at()` | 101 | 2 | `test_board.py::test_start_position_pieces` |

Lines to type in all: 14. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `print_board()` in `board.py`

**Where:** lines 46 to 53 of `board.py`, inside `print_board()`, in place of the stub below the docstring. The tests call it directly.

```text
37 | def print_board(board: Board) -> None:
     ...
44 |         The board, row 0 first (rank 8).
45 |     """
46 +     for row in range(8):
47 +         # Start the line with the rank number, then add a space and each square
48 +         line = BOARD_RANKS[row]
49 +         for col in range(8):
50 +             line = line + " " + board[row][col]
51 +         print(line)
52 +     # Two spaces line up the file letters under the squares
53 +     print("  a b c d e f g h")
54 |
55 |
56 | def square_name(row: int, col: int) -> str:
```

**How it works:** The loop prints one line per row, row 0 (rank 8) first. Each line starts with the rank number from `BOARD_RANKS`, and the inner loop adds a space and each square's letter with `+`. After the eight rows, the last line prints the file letters, with two spaces in front so each letter sits under its column.

### `square_name()` in `board.py`

**Where:** line 72 of `board.py`, inside `square_name()`, in place of the stub below the docstring. The tests call it directly.

```text
56 | def square_name(row: int, col: int) -> str:
     ...
70 |         The square name, such as "e2" for (6, 4).
71 |     """
72 +     return BOARD_FILES[col] + BOARD_RANKS[row]
73 |
74 |
75 | def parse_square(name: str) -> Square:
```

**How it works:** `BOARD_FILES` is "abcdefgh", so `BOARD_FILES[col]` is the file letter, and `BOARD_RANKS` lists the rank digits from row 0, so `BOARD_RANKS[row]` is the rank. Glued together, (6, 4) gives "e" + "2" = "e2".

### `parse_square()` in `board.py`

**Where:** lines 94 to 98 of `board.py`, inside `parse_square()`, in place of the stub below the docstring. The tests call it directly.

```text
 75 | def parse_square(name: str) -> Square:
      ...
 92 |         If the name is not a square on the board, such as "i9".
 93 |     """
 94 +     if len(name) != 2 or name[0] not in BOARD_FILES or name[1] not in BOARD_RANKS:
 95 +         raise ValueError(f"Not a square: {name!r}")
 96 +     col = BOARD_FILES.index(name[0])
 97 +     row = BOARD_RANKS.index(name[1])
 98 +     return row, col
 99 |
100 |
101 | def piece_at(board: Board, square: Square) -> str:
```

**How it works:** A square name has exactly two characters, a file letter and a rank digit. Anything else, such as "i9" or "e10", raises `ValueError` with a message that shows the bad text. `index` finds where a character sits in a string, which turns the letter into a column and the digit into a row: "e4" becomes (4, 4).

### `piece_at()` in `board.py`

**Where:** lines 103 to 104 of `board.py`, inside `piece_at()`, in place of the stub below the docstring. The tests call it directly.

```text
101 | def piece_at(board: Board, square: Square) -> str:
102 |     """Return the piece on a (row, col) square, or EMPTY."""
103 +     row, col = square
104 +     return board[row][col]
105 |
106 |
107 | def main():
```

**How it works:** A square is a (row, col) tuple, so unpacking gives the two numbers their names. `board[row][col]` picks the row from the list of rows and then the square from that row.
