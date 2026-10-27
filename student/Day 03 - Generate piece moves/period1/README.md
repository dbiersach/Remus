# Day 3, Period 1: Python lab 5: while, break, direction tuples

## Learning objectives

By the end of this period, each pair can:

- Repeat steps with `while` and stop early with `break`. **Measured by:** The lab's walk from d4 toward the edge stops at the first piece in its way.
- Describe a direction as a (row change, col change) tuple. **Measured by:** The pair writes the tuple for "up and to the right" (-1, 1) and explains the minus sign.

## The files

The lab is `python_loops.py` in `student/`, with the answers in `python_loops_instructor.py` in `instructor/`. Both come from `labs/day03/`. Run it with `uv run python_loops.py`.

The Remus code here is the same as at the end of the period before.

## The changes and why

The pairs fill in the blanks of `python_loops.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_loops_instructor.py`.

Part #1 counts to 3 with `while`, the loop that repeats as long as its test is true.

Part #2 writes the direction up and to the right as the tuple `(-1, 1)`. The row step is -1 because row 0 is rank 8: moving toward Black's side makes the row smaller.

Part #3 walks from d4 one square at a time with `while True` and leaves the loop with `break` at the edge of the board or at the first piece. The walk reaches e5, f6, and g7, where a Black pawn stops it. `slide()` on Day 3, period 3 is this same loop, and it returns moves instead of square names.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.

## What you edit in the lab

Open `python_loops.py`. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 14. Check the work with `uv run python_loops.py` and compare each printed result with the expected value beside it.
