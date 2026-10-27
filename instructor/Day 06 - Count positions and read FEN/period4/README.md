# Day 6, Period 4: Python lab 9 and FEN

## Learning objectives

By the end of this period, each pair can:

- Read and write the piece placement of FEN. **Measured by:** `test_game.py` FEN tests pass: the start FEN goes in and comes back out the same.
- Name the six fields of a FEN string. **Measured by:** The pair labels the six fields of the start FEN on the worksheet.

## The files

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

### `fen_placement()` in `fen.py`

Writes the board as the first field of FEN: one rank at a time, with a digit for each run of empty squares and a slash between ranks. FEN lets you save any position in one line and share it with other chess programs.

### `board_from_placement()` in `fen.py`

Reads that field back into an 8x8 board, turning each digit into that many empty squares, and refuses a rank that does not describe exactly 8 squares. From now on every test position starts as FEN.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
