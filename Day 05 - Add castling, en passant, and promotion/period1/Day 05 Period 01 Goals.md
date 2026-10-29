# Day 5, Period 1: Python lab 7: sets, in, string replacement

## Learning objectives

By the end of this period, each student pair can:

- Use sets and `in` to test membership, and change strings with `replace()`. **Measured by:** The lab removes `"K"` from `"KQkq"` when the h1 rook moves.

## The files

The lab is `python_sets.py` in the `student` folder, with the answers in `python_sets_instructor.py` in the `instructor` folder beside it. Open `python_sets.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

The code here is the same as at the end of the period before.

## The changes and why

The student pairs fill in the blanks of `python_sets.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_sets_instructor.py`.

Part #1 adds squares to a set. A set holds each item once, so adding h1 a second time changes nothing.

Parts #2 and #3 ask questions with `in`, of a set and of a dict. The dict `rights_lost` names the castling rights each home square guards: a piece leaving e1 removes K and Q, and a piece leaving h1 removes K.

Part #4 removes rights with `replace()`, one letter at a time, starting from `"KQkq"`. `update_castling_rights()` in `make_move.py` does exactly this in period 2.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Slides: a set holds each item once, `in` asks a yes-or-no question, and a dict looks up a value by its key. |
| 8:45 to 9:35 | Student pairs work through the four parts of `python_sets.py`, ending with `replace()` removing "K" from "KQkq" when the h1 rook moves. |
| 9:35 to 9:50 | The class lists, on the board, every move that removes a castling right. |
| 9:50 to 10:00 | Wrap-up and a preview of castling. |

## What you edit in the lab

Open `python_sets.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 14. Check the work by running `python_sets.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.
