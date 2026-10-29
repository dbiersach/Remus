# Day 6, Period 2: Perft

## Learning objectives

By the end of this period, each pair can:

- Count the positions of the move tree with `perft()`. **Measured by:** Running `perft.py` prints 20, 400, and 8,902 for depths 1 to 3.
- Explain why perft proves the rules right. **Measured by:** Exit ticket: one sentence on what a wrong count tells you.

## The files

New files this period:

- `perft.py`

Functions the pairs write this period:

- `perft()` in `perft.py`

In the `student` folder these functions raise `NotImplementedError` until a pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `perft()` in `perft.py`

Counts every position reached after exactly `depth` moves, by making each legal move, counting below it, and undoing it. The counts from the start (20, 400, 8,902) are published, so a match proves the rules right and a mismatch points to a bug.

Check the work with the tests: open a terminal in VS Code inside the `student` folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).

## The period step by step

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Unplugged warm-up, "Count by hand": in a king and pawn against king position, pairs list every move two plies deep on index cards and count the leaves. |
| 10:45 to 10:55 | Slides: perft counts the leaves of the legal move tree. |
| 10:55 to 11:25 | Pairs write `perft()` and run it on the warm-up position to check their cards. |
| 11:25 to 11:50 | Pairs run `perft.py` from the start: 20, 400, and 8,902. The teacher shows `divide()`, which prints the count under each root move. |
| 11:50 to 12:00 | Show and choose for `perft()`. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `perft.py` | `perft()` | 25 | 8 | `uv run pytest` |

Lines to type in all: 8. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
