# Day 5, Period 1: Python lab 7: sets, in, string replacement

## Learning objectives

By the end of this period, each pair can:

- Use sets and `in` to test membership, and change strings with `replace()`. **Measured by:** The lab removes `"K"` from `"KQkq"` when the h1 rook moves.

## The files

The lab is `python_sets.py` in the `student` folder, with the answers in `python_sets_instructor.py` in the `instructor` folder beside it. Open `python_sets.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

The code here is the same as at the end of the period before.

## The changes and why

The pairs fill in the blanks of `python_sets.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_sets_instructor.py`.

Part #1 adds squares to a set. A set holds each item once, so adding h1 a second time changes nothing.

Parts #2 and #3 ask questions with `in`, of a set and of a dict. The dict `rights_lost` names the castling rights each home square guards: a piece leaving e1 removes K and Q, and a piece leaving h1 removes K.

Part #4 removes rights with `replace()`, one letter at a time, starting from `"KQkq"`. `update_castling_rights()` in `make_move.py` does exactly this in period 2.

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).

## What you edit in the lab

Open `python_sets.py`. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 14. Check the work by running `python_sets.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.
