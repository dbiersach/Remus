# Day 6, Period 4: Python lab 9 and FEN

## Learning objectives

By the end of this period, each pair can:

- Read and write the piece placement of FEN. **Measured by:** `test_game.py` FEN tests pass: the start FEN goes in and comes back out the same.
- Name the six fields of a FEN string. **Measured by:** `python_fen_fields.py` prints the six fields of the start FEN with their names, and the pair labels them on the worksheet.

## The files

The lab is `python_fen_fields.py` in `student/`, with the answers in `python_fen_fields_instructor.py` in `instructor/`. Both come from `labs/day06/`. Run it with `uv run python_fen_fields.py`.

New files this period:

- `fen.py`
- `test_game.py`

Files that grow this period:

- `test_perft.py`

Functions the pairs write this period:

- `fen_placement()` in `fen.py`
- `board_from_placement()` in `fen.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

The pairs fill in the blanks of `python_fen_fields.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_fen_fields_instructor.py`.

The lab cuts the start FEN into its six fields with `split()` and prints each with its name, the map the pair needs before writing `fen.py`. Then `try` and `except ValueError` catch the error that `int()` raises on text that is not a number, which is how a FEN reader can reject a broken string instead of crashing.

### `fen_placement()` in `fen.py`

Writes the board as the first field of FEN: one rank at a time, with a digit for each run of empty squares and a slash between ranks. FEN lets you save any position in one line and share it with other chess programs.

### `board_from_placement()` in `fen.py`

Reads that field back into an 8x8 board, turning each digit into that many empty squares, and refuses a rank that does not describe exactly 8 squares. From now on every test position starts as FEN.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `fen.py` | `fen_placement()` | 21 | 18 | `uv run pytest` |
| `fen.py` | `board_from_placement()` | 41 | 14 | `uv run pytest` |

Lines to type in all: 32. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## What you edit in the lab

Open `python_fen_fields.py`. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 8. Check the work with `uv run python_fen_fields.py` and compare each printed result with the expected value beside it.
