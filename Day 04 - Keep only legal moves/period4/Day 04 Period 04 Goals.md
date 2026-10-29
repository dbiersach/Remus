# Day 4, Period 4: Practice positions

## Learning objectives

By the end of this period, each student pair can:

- Check the move generator on practice positions. **Measured by:** Every practice-position test in `test_legal_moves.py` passes.
- Predict a legal-move count before running the code. **Measured by:** In `demo_practice_positions.py` the student pair types its prediction for each position first, then runs the file and compares.

## The files

The demo is `demo_practice_positions.py` in the `student` folder, with the answers in `demo_practice_positions_instructor.py` in the `instructor` folder beside it. Open `demo_practice_positions.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

Files that grow this period:

- `test_legal_moves.py`

## The changes and why

The student pairs fill in the blanks of `demo_practice_positions.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `demo_practice_positions_instructor.py`.

`demo_practice_positions.py` builds three positions from a dict of {square: piece} and prints each board with Remus's legal-move count. The student pair types each position and its prediction before running the file, so every count is a test of the student pair's own reasoning as well as of the code.

Part #2 puts a rook check on the White king, and Part #3 adds a knight on e2 that blocks the check but cannot move: it is pinned. The loop at the end counts only the moves that start on e2, the same check as `test_pinned_knight_has_no_moves()`.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 3:00 to 3:10 | Slides: the workshop's first three verification positions: the start, a king in check, and a pinned knight. |
| 3:10 to 3:50 | In `demo_practice_positions.py` student pairs type each position and write their prediction of its legal move count before Remus counts. |
| 3:50 to 4:15 | Part #4: each student pair builds a position of its own and trades it with the next student pair, who predict before they run it. |
| 4:15 to 4:30 | Checkpoint: a pinned knight has zero legal moves, and a king in check has only escapes. |

## What you edit in the demo

Open `demo_practice_positions.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 14. Check the work by running `demo_practice_positions.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

### Part #1 - The Start Position

```text
36 |     print("Part #1 - The Start Position")
37 |     # Write your prediction first, then run the file
38 +     prediction = 20
39 +     compare(new_game(), prediction)
40 |
41 |     print("Part #2 - A King in Check")
```

**How it works:** Before you run the file, change `prediction` to the number of legal moves you expect, then compare it with the count Remus prints. From the starting position it is 20: 16 pawn moves and 4 knight moves.

### Part #2 - A King in Check

```text
41 |     print("Part #2 - A King in Check")
42 |     # White: king on e1. Black: rook on e8 and king on a8. The rook checks down the e-file.
43 +     state = position({"e1": "K", "e8": "r", "a8": "k"})
44 +     print(f"White in check: {in_check(state, WHITE)}  (expected True)")
45 +     prediction = 4
46 +     compare(state, prediction)
47 |
48 |     print("Part #3 - A Pinned Knight")
```

**How it works:** `position` builds a board holding only the pieces in the dict. The Black rook on e8 checks the White king on e1 along the e-file, so `in_check` prints True. Count the king's legal moves yourself, put the number in `prediction`, and run the file.

### Part #3 - A Pinned Knight

```text
48 |     print("Part #3 - A Pinned Knight")
49 |     # Put a White knight on e2, between the king and the rook
50 +     state = position({"e1": "K", "e2": "N", "e8": "r", "a8": "k"})
51 +     prediction = 4
52 +     compare(state, prediction)
53 |     # Count only the moves that start on e2
54 +     knight_count = 0
55 +     for move in legal_moves(state):
56 +         if move_to_uci(move).startswith("e2"):
57 +             knight_count += 1
58 +     print(f"Legal knight moves: {knight_count}  (expected 0: the knight is pinned)")
59 |
60 |     print("Part #4 - Your Own Position")
```

**How it works:** The White knight on e2 stands between its king and the Black rook, so it is pinned: any knight move would expose the king. The loop counts the legal moves that start on e2, using the first two characters of each move's UCI text, and finds none.
