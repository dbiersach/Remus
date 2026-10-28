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

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).
