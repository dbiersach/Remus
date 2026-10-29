# Day 4, Period 4: Practice positions

## Learning objectives

By the end of this period, each pair can:

- Check the move generator on practice positions. **Measured by:** Every practice-position test in `test_legal_moves.py` passes.
- Predict a legal-move count before running the code. **Measured by:** In `demo_practice_positions.py` the pair types its prediction for each position first, then runs the file and compares.

## The files

The demo is `demo_practice_positions.py` in the `student` folder, with the answers in `demo_practice_positions_instructor.py` in the `instructor` folder beside it. Open `demo_practice_positions.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

Files that grow this period:

- `test_legal_moves.py`

## The changes and why

The pairs fill in the blanks of `demo_practice_positions.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `demo_practice_positions_instructor.py`.

`demo_practice_positions.py` builds three positions from a dict of {square: piece} and prints each board with Remus's legal-move count. The pair types each position and its prediction before running the file, so every count is a test of the pair's own reasoning as well as of the code.

Part #2 puts a rook check on the White king, and Part #3 adds a knight on e2 that blocks the check but cannot move: it is pinned. The loop at the end counts only the moves that start on e2, the same check as `test_pinned_knight_has_no_moves()`.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 3:00 to 3:10 | Slides: the workshop's first three verification positions: the start, a king in check, and a pinned knight. |
| 3:10 to 3:50 | In `demo_practice_positions.py` pairs type each position and write their prediction of its legal move count before Remus counts. |
| 3:50 to 4:15 | Part #4: each pair builds a position of its own and trades it with the next pair, who predict before they run it. |
| 4:15 to 4:30 | Checkpoint: a pinned knight has zero legal moves, and a king in check has only escapes. |

## What you edit in the demo

Open `demo_practice_positions.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 14. Check the work by running `demo_practice_positions.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.
