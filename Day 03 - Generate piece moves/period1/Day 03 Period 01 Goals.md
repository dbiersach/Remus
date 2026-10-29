# Day 3, Period 1: Python lab 5: while, break, direction tuples

## Learning objectives

By the end of this period, each student pair can:

- Repeat steps with `while` and stop early with `break`. **Measured by:** The lab's walk from d4 toward the edge stops at the first piece in its way.
- Describe a direction as a (row change, col change) tuple. **Measured by:** The student pair writes the tuple for "up and to the right" (-1, 1) and explains the minus sign.

## The files

The lab is `python_loops.py` in the `student` folder, with the answers in `python_loops_instructor.py` in the `instructor` folder beside it. Open `python_loops.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

The code here is the same as at the end of the period before.

## The changes and why

The student pairs fill in the blanks of `python_loops.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_loops_instructor.py`.

Part #1 counts to 3 with `while`, the loop that repeats as long as its test is true.

Part #2 writes the direction up and to the right as the tuple `(-1, 1)`. The row step is -1 because row 0 is rank 8: moving toward Black's side makes the row smaller.

Part #3 walks from d4 one square at a time with `while True` and leaves the loop with `break` at the edge of the board or at the first piece. The walk reaches e5, f6, and g7, where a Black pawn stops it. `slide()` on Day 3, period 3 is this same loop, and it returns moves instead of square names.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Slides: `while`, `break`, `continue`, and a list of direction tuples. |
| 8:45 to 9:35 | Student pairs work through the four parts of `python_loops.py`: repeat with `while`, store a direction, walk from d4 until the edge or a piece, and try another direction. |
| 9:35 to 9:50 | The teacher runs the walk on the projector with a piece in the way and the class predicts where it stops. |
| 9:50 to 10:00 | Wrap-up: which loop stops at the edge, and which line stops it at a piece? |

## What you edit in the lab

Open `python_loops.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 14. Check the work by running `python_loops.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

### Part #1 - Repeat with while

```python
21 |     print("Part #1 - Repeat with while")
22 |     # A while loop repeats as long as its test is True
23 +     count = 0
24 +     while count < 3:
25 +         print(f"  step {count}")
26 +         count += 1
27 |     print("  (expected step 0, step 1, step 2)")
28 |
```

**How it works:** A `while` loop repeats its indented lines as long as its test is True. `count` starts at 0 and grows by 1 each time, so the loop prints steps 0, 1, and 2 and stops when `count` reaches 3.

### Part #2 - A Direction Is a Tuple

```python
30 |     # Row 0 is rank 8, so a step toward rank 8 makes the row smaller: -1
31 |     up_right = (-1, 1)
32 +     row_step, col_step = up_right
33 +     print(f"row step {row_step}, col step {col_step}  (expected -1 and 1)")
34 |
35 |     print("Part #3 - Walk Until the Edge or a Piece")
```

**How it works:** A direction is a tuple of two steps. Unpacking gives each step a name: `row_step` is -1, one row toward rank 8, and `col_step` is 1, one column to the right.

### Part #3 - Walk Until the Edge or a Piece

```python
41 |     row, col = 4, 3
42 |     squares = ""
43 +     while True:
44 +         row += row_step
45 +         col += col_step
46 |         # Leaving the board ends the walk
47 +         if row < 0 or row > 7 or col < 0 or col > 7:
48 +             break
49 +         squares += square_name(row, col) + " "
50 |         # A piece on the square ends the walk too, after the square is counted
51 +         if board[row][col] != ".":
52 +             break
53 |     print(f"Squares reached: {squares}  (expected e5 f6 g7)")
54 |
```

**How it works:** `while True` repeats until a `break` stops it. Each pass takes one step in the direction. If the step leaves the board, the walk ends. Otherwise the square's name is added to the text, and if a piece stands there the walk ends too, after counting that square. This is the walk a bishop, rook, or queen makes.
