# Day 2, Period 1: Python lab 3: functions, type hints, tuples, assert, pytest

## Learning objectives

By the end of this period, each student pair can:

- Write a function with parameters, a return value, type hints, and a docstring. **Measured by:** The lab's `is_white()` and `on_board()` return the right answers for every example on the worksheet.
- Check a function with `assert` and with pytest. **Measured by:** `run_tests.py` shows the lab's tests passing, and one deliberately wrong `assert` fails with a clear report.
- Pack two numbers into a tuple and unpack them. **Measured by:** The student pair writes `row, col = square` and explains what each name holds.

## The files

The lab is `python_functions.py` in the `student` folder, with the answers in `python_functions_instructor.py` in the `instructor` folder beside it. Open `python_functions.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

The code here is the same as at the end of the period before.

## The changes and why

The student pairs fill in the blanks of `python_functions.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_functions_instructor.py`.

Part #1 calls the finished `is_white()` and `on_board()`. You type the one line under each docstring: `is_white()` asks `isupper()`, and `on_board()` checks that the row and the column both lie between 0 and 7. Remus asks these two questions in nearly every function from Day 2 on.

Part #2: you write `is_black()` from nothing: the `def` line with its type hints, the docstring, and the `return`. The type hints say what goes in and what comes out, so a reader knows how to call the function without reading its body.

Part #3 packs e4 into the tuple `(4, 4)` and unpacks it with `row, col = square`. Every Remus square is a tuple like this one.

Part #4 runs the two test functions, whose `assert` lines stop the program when a check fails. Running `run_tests.py` runs the same tests with pytest and prints a report, and breaking one test on purpose shows what a failure looks like before a real one happens.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Slides: functions, parameters, `return`, type hints, and docstrings. |
| 8:45 to 9:25 | Student pairs work through Parts #1 to #3 of `python_functions.py`: call a function, write their own, and unpack a square tuple such as `row, col = (6, 4)`. |
| 9:25 to 9:35 | Slides: `assert` and pytest. The teacher breaks a function on purpose and the class reads the failing test together. |
| 9:35 to 9:50 | Student pairs finish Part #4, which checks their functions with `assert`. |
| 9:50 to 10:00 | Wrap-up: each student pair says what a failing test tells them and where to look first. |

## What you edit in the lab

Open `python_functions.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 16. Check the work by running `python_functions.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

### `is_white()`

```text
11 | def is_white(piece: str) -> bool:
12 |     """Return True if the piece is White. White pieces are uppercase letters."""
13 +     return piece.isupper()
14 |
15 |
```

### `on_board()`

```text
30 |         True when both the row and the column are between 0 and 7.
31 |     """
32 +     return 0 <= row <= 7 and 0 <= col <= 7
33 |
34 |
35 | # Write a whole function yourself: its def line, its docstring, and its body
36 + def is_black(piece: str) -> bool:
37 +     """Return True if the piece is Black. Black pieces are lowercase letters."""
38 +     return piece.islower()
39 |
40 |
```

### `test_is_white()`

```text
41 | def test_is_white():
42 |     """A White knight is White, and a Black knight is not."""
43 +     assert is_white("N")
44 +     assert not is_white("n")
45 |
46 |
```

### `test_on_board()`

```text
48 |     """The corner a1 is on the board, and row 8 is one row past rank 1."""
49 |     # a1 is row 7, col 0
50 +     assert on_board(7, 0)
51 +     assert not on_board(8, 3)
52 |
53 |
```

### Part #2 - Your Own Function

```text
60 |
61 |     print("Part #2 - Your Own Function")
62 +     print(f'is_black("q") is {is_black("q")}  (expected True)')
63 +     print(f'is_black("Q") is {is_black("Q")}  (expected False)')
64 |
65 |     print("Part #3 - A Square Is a Tuple")
```

### Part #3 - A Square Is a Tuple

```text
67 |     square = (4, 4)
68 |     # Unpacking gives each number its own name, in order
69 +     row, col = square
70 +     print(f"row {row}, col {col}  (expected row 4, col 4)")
71 +     print(f"On the board: {on_board(row, col)}  (expected True)")
72 |
73 |     print("Part #4 - Check the Functions with assert")
```

### Part #4 - Check the Functions with assert

```text
73 |     print("Part #4 - Check the Functions with assert")
74 |     # assert does nothing when its test is True and stops the program when it is False
75 +     test_is_white()
76 +     test_on_board()
77 |     print("Every assert passed  (expected this line)")
78 |     print("Now run the same tests with pytest: press Run on run_tests.py")
```
