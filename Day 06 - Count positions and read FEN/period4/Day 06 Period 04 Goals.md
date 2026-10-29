# Day 6, Period 4: Python lab 9 and FEN

## Learning objectives

By the end of this period, each student pair can:

- Read and write the piece placement of FEN. **Measured by:** `test_game.py` FEN tests pass: the start FEN goes in and comes back out the same.
- Name the six fields of a FEN string. **Measured by:** `python_fen_fields.py` prints the six fields of the start FEN with their names, and the student pair labels them on the worksheet.

## The files

The lab is `python_fen_fields.py` in the `student` folder, with the answers in `python_fen_fields_instructor.py` in the `instructor` folder beside it. Open `python_fen_fields.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

New files this period:

- `fen.py`
- `test_game.py`

Files that grow this period:

- `test_perft.py`

Functions the student pairs write this period:

- `fen_placement()` in `fen.py`
- `board_from_placement()` in `fen.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

The student pairs fill in the blanks of `python_fen_fields.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_fen_fields_instructor.py`.

The lab cuts the start FEN into its six fields with `split()` and prints each with its name, the map the student pair needs before writing `fen.py`. Then `try` and `except ValueError` catch the error that `int()` raises on text that is not a number, which is how a FEN reader can reject a broken string instead of crashing.

### `fen_placement()` in `fen.py`

Writes the board as the first field of FEN: one rank at a time, with a digit for each run of empty squares and a slash between ranks. FEN lets you save any position in one line and share it with other chess programs.

### `board_from_placement()` in `fen.py`

Reads that field back into an 8x8 board, turning each digit into that many empty squares, and refuses a rank that does not describe exactly 8 squares. From now on every test position starts as FEN.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 3:00 to 3:10 | Slides: the six fields of FEN, `split()`, `int()`, and `ValueError`. |
| 3:10 to 3:30 | Student pairs work through `python_fen_fields.py`. |
| 3:30 to 4:20 | Student pairs write `fen_placement()` and `board_from_placement()` in `fen.py`. The teacher writes the other five fields. |
| 4:20 to 4:30 | Checkpoint: every test position loads from FEN and perft matches the reference. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `fen.py` | `fen_placement()` | 21 | 18 | `run_tests.py` |
| `fen.py` | `board_from_placement()` | 56 | 14 | `run_tests.py` |

Lines to type in all: 32. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `fen_placement()` in `fen.py`

**Where:** lines 36 to 53 of `fen.py`, inside `fen_placement()`, in place of the stub below the docstring. It is called by `state_to_fen()` in `fen.py`.

```python
21 | def fen_placement(board: Board) -> str:
22 |     """
     ...
34 |         empty squares in a row, so an empty rank is "8".
35 |     """
36 +     placement = ""
37 +     for row in board:
38 +         text = ""
39 +         empty_count = 0
40 +         for piece in row:
41 +             if piece == EMPTY:
42 +                 empty_count += 1
43 +             else:
44 +                 if empty_count > 0:
45 +                     text += str(empty_count)
46 +                     empty_count = 0
47 +                 text += piece
48 +         if empty_count > 0:
49 +             text += str(empty_count)
50 +         if placement != "":
51 +             placement += "/"  # A slash separates one rank from the next
52 +         placement += text
53 +     return placement
54 |
55 |
56 | def board_from_placement(text: str) -> Board:
```

**How it works:** FEN writes each rank from the a-file to the h-file, and a run of empty squares becomes one digit. For each row the code counts empty squares in `empty_count`. When a piece appears, the count, if any, is written first, then the piece letter. At the end of the row a final count is written. A slash goes between ranks, so the starting row 0 gives "rnbqkbnr" and an empty rank gives "8".

### `board_from_placement()` in `fen.py`

**Where:** lines 70 to 83 of `fen.py`, inside `board_from_placement()`, in place of the stub below the docstring. It is called by `state_from_fen()` in `fen.py`.

```python
56 | def board_from_placement(text: str) -> Board:
57 |     """
     ...
68 |         The board, row 0 (rank 8) first.
69 |     """
70 +     board = []
71 +     for rank_text in text.split("/"):
72 +         row = []
73 +         for character in rank_text:
74 +             if character.isdigit():
75 +                 row += [EMPTY] * int(character)
76 +             else:
77 +                 row.append(character)
78 +         if len(row) != 8:
79 +             raise ValueError(f"A FEN rank must describe 8 squares: {rank_text!r}")
80 +         board.append(row)
81 +     if len(board) != 8:
82 +         raise ValueError(f"FEN must describe 8 ranks: {text!r}")
83 +     return board
84 |
85 |
86 | def state_from_fen(fen: str) -> dict:
```

**How it works:** `split("/")` cuts the placement into eight ranks, rank 8 first. In each rank a digit adds that many empty squares and a letter adds one piece. A rank that does not add up to 8 squares, or a placement without 8 ranks, raises `ValueError`, so a typing mistake in a FEN stops at once.

### Part #1 - split() Cuts Text at Every Space

```python
22 |     print("Part #1 - split() Cuts Text at Every Space")
23 |     # split("/") cuts at every slash instead, the way fen.py cuts the placement into rows
24 +     fields = START_FEN.split()
25 +     print(f"Fields: {len(fields)}  (expected 6)")
26 |
27 |     print("Part #2 - Name the Six Fields")
```

**How it works:** `split()` with no argument cuts text at every run of spaces and returns a list of the pieces. A FEN has six fields, so the list holds 6 items.

### Part #2 - Name the Six Fields

```python
26 |
27 |     print("Part #2 - Name the Six Fields")
28 +     for i in range(6):
29 +         print(f"  {FIELD_NAMES[i]}: {fields[i]}")
30 |     print("  (expected the placement, w, KQkq, -, 0, and 1)")
31 |
```

**How it works:** The loop counts i from 0 to 5 and prints the name of field i next to its value, so each field is labeled.

### Part #3 - int() and ValueError

```python
33 |     # Try "12" here too: int() turns digits into a number and raises ValueError otherwise
34 |     text = "x"
35 +     try:
36 +         print(f"  {text} is the number {int(text)}")
37 +     except ValueError:
38 +         print(f"  {text} is not a number, so int() raised ValueError")
39 |     print("  (expected x is not a number)")
40 |
```

**How it works:** `try` runs a line that may fail. `int("x")` cannot make a number from x, so Python raises `ValueError`, and the `except ValueError` lines run instead of stopping the program. Change `text` to "12" to see the other path.

## What you edit in the lab

Open `python_fen_fields.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 8. Check the work by running `python_fen_fields.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.
