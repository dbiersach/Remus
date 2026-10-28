# Day 2, Period 1: Python lab 3: functions, type hints, tuples, assert, pytest

## Learning objectives

By the end of this period, each pair can:

- Write a function with parameters, a return value, type hints, and a docstring. **Measured by:** The lab's `is_white()` and `on_board()` return the right answers for every example on the worksheet.
- Check a function with `assert` and with pytest. **Measured by:** `uv run pytest` shows the lab's tests passing, and one deliberately wrong `assert` fails with a clear report.
- Pack two numbers into a tuple and unpack them. **Measured by:** The pair writes `row, col = square` and explains what each name holds.

## The files

The lab is `python_functions.py` in the `student` folder, with the answers in `python_functions_instructor.py` in the `instructor` folder beside it. Open `python_functions.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

The code here is the same as at the end of the period before.

## The changes and why

The pairs fill in the blanks of `python_functions.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_functions_instructor.py`.

Part #1 calls the finished `is_white()` and `on_board()`. You type the one line under each docstring: `is_white()` asks `isupper()`, and `on_board()` checks that the row and the column both lie between 0 and 7. Remus asks these two questions in nearly every function from Day 2 on.

Part #2: you write `is_black()` from nothing: the `def` line with its type hints, the docstring, and the `return`. The type hints say what goes in and what comes out, so a reader knows how to call the function without reading its body.

Part #3 packs e4 into the tuple `(4, 4)` and unpacks it with `row, col = square`. Every Remus square is a tuple like this one.

Part #4 runs the two test functions, whose `assert` lines stop the program when a check fails. `uv run pytest python_functions.py` runs the same tests and prints a report, and breaking one test on purpose shows what a failure looks like before a real one happens.

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).
