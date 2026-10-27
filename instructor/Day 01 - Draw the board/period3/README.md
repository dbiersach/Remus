# Day 1, Period 3: Python lab 2: lists and nested lists

## Learning objectives

By the end of this period, each pair can:

- Make a list, read one item by index, and count the items with `len()`. **Measured by:** Part #1 of `python_lists.py` prints 8 pieces and `q` on the d-file.
- Visit every item with `for` and `range()`. **Measured by:** Part #2 prints the back rank `r n b q k b n r` on one line.
- Build an 8x8 board as a list of rows and read `board[row][col]`. **Measured by:** Part #3 prints the starting position, and the pair names the square `board[4][4]` (e4) without running code.
- Say where each rank lives: row 0 is rank 8. **Measured by:** Unplugged warm-up "Call the square": each student converts four squares on the printed board, such as e2 to (6, 4), with no mistakes.

## The files

This period comes before any Remus code. The lab is `python_lists.py` in `student/`, with the answers in `python_lists_instructor.py` in `instructor/`. Both come from `labs/day01/`. Run it with `uv run python_lists.py`.

## The changes and why

The pairs fill in the blanks of `python_lists.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_lists_instructor.py`.

Part #1: you count the pieces in a list with `len()` and read one by index. Index 3 is the d-file, where the queen starts.

Part #2: a `for` loop with `range(8)` visits the eight files in order. Remus walks the board with loops like this everywhere.

Part #3: you build the board as a list of eight rows, each a new list of eight dots, then put the pieces in. Row 0 is rank 8, so Black's pieces go in rows 0 and 1. This is the board `board.py` holds.

Part #4: you play 1. e4 by changing two squares, then count the White pawns left on rank 2. `board[row][col]` is how every rule in Remus reads and changes the board.
