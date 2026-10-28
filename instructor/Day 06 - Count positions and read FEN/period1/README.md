# Day 6, Period 1: Python lab 8: recursion

## Learning objectives

By the end of this period, each pair can:

- Write a recursive function with a base case. **Measured by:** The lab's countdown and leaf count give the worksheet's numbers.
- Trace a call stack by hand. **Measured by:** The pair draws the calls of a depth-2 count and the value each one returns.

## The files

The lab is `python_recursion.py` in `student/`, with the answers in `python_recursion_instructor.py` in `instructor/`. Open `python_recursion.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

The Remus code here is the same as at the end of the period before.

## The changes and why

The pairs fill in the blanks of `python_recursion.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_recursion_instructor.py`.

Part #1: `countdown()` calls itself with a smaller number until it reaches the base case, 0. Without the base case the calls would never stop.

Part #2: `count_leaves()` counts the moves at the bottom of a small tree made of lists. A move name is a leaf and counts 1, and a list adds up the counts of its branches.

Part #3 is finished code to read and trace: `knight_paths()` counts the ways a knight can jump from a1. It has the same shape as `perft()` in period 2: at depth 0 return 1, otherwise add up the count under every move.

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).
