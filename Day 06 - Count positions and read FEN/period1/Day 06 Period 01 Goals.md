# Day 6, Period 1: Python lab 8: recursion

## Learning objectives

By the end of this period, each student pair can:

- Write a recursive function with a base case. **Measured by:** The lab's countdown and leaf count give the worksheet's numbers.
- Trace a call stack by hand. **Measured by:** The student pair draws the calls of a depth-2 count and the value each one returns.

## The files

The lab is `python_recursion.py` in the `student` folder, with the answers in `python_recursion_instructor.py` in the `instructor` folder beside it. Open `python_recursion.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

The code here is the same as at the end of the period before.

## The changes and why

The student pairs fill in the blanks of `python_recursion.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_recursion_instructor.py`.

Part #1: `countdown()` calls itself with a smaller number until it reaches the base case, 0. Without the base case the calls would never stop.

Part #2: `count_leaves()` counts the moves at the bottom of a small tree made of lists. A move name is a leaf and counts 1, and a list adds up the counts of its branches.

Part #3 is finished code to read and trace: `knight_paths()` counts the ways a knight can jump from a1. It has the same shape as `perft()` in period 2: at depth 0 return 1, otherwise add up the count under every move.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Slides: a function that calls itself, its base case, and the call stack. |
| 8:45 to 9:35 | Student pairs work through the three parts of `python_recursion.py`: count down, count the leaves of a small tree, and count the paths of a knight. |
| 9:35 to 9:50 | The teacher draws the call stack of a short count on the whiteboard while the class traces it. |
| 9:50 to 10:00 | Wrap-up: what stops a recursion? |

## What you edit in the lab

Open `python_recursion.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 11. Check the work by running `python_recursion.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

### `countdown()`

```text
15 |     """Print number, number - 1, ..., 1, and then Go!"""
16 |     # Base case: at 0 the function stops calling itself
17 +     if number == 0:
18 +         print("  Go!")
19 +         return
20 |     # Recursive case: print one number, then let a smaller call do the rest
21 +     print(f"  {number}")
22 +     countdown(number - 1)
23 |
24 |
```

**How it works:** A recursive function calls itself on a smaller problem. The base case comes first: at 0 the function prints Go! and returns, so the calls stop. Otherwise it prints its number and calls `countdown(number - 1)`, which does the rest.

### `count_leaves()`

```text
37 |         The number of leaves in the whole tree.
38 |     """
39 +     if isinstance(tree, str):
40 +         return 1
41 +     total = 0
42 +     for branch in tree:
43 +         total += count_leaves(branch)
44 +     return total
45 |
46 |
```

**How it works:** A leaf is a string, and it counts as 1. Any other tree is a list of branches, so the function adds up `count_leaves` of each branch. Each branch is a smaller tree, so every call gets closer to the leaves.
