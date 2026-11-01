# Day 6, Period 2: Perft

## Learning objectives

By the end of this period, each student pair can:

- Count the positions of the move tree with `perft()`. **Measured by:** Running `perft.py` prints 20, 400, and 8,902 for depths 1 to 3.
- Explain why perft proves the rules right. **Measured by:** Exit ticket: one sentence on what a wrong count tells you.

## The files

New files this period:

- `perft.py`

Functions the student pairs write this period:

- `perft()` in `perft.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `perft()` in `perft.py`

Counts every position reached after exactly `depth` moves, by making each legal move, counting below it, and undoing it. The counts from the start (20, 400, 8,902) are published, so a match proves the rules right and a mismatch points to a bug.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Unplugged warm-up, "Count by hand": in a king and pawn against king position, student pairs list every move two plies deep on index cards and count the leaves. |
| 10:45 to 10:55 | Slides: perft counts the leaves of the legal move tree. |
| 10:55 to 11:25 | Student pairs write `perft()` and run it on the warm-up position to check their cards. |
| 11:25 to 11:50 | Student pairs run `perft.py` from the start: 20, 400, and 8,902. The teacher shows `divide()`, which prints the count under each root move. |
| 11:50 to 12:00 | Show and choose for `perft()`. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `perft.py` | `perft()` | 25 | 8 | `run_tests.py` |

Lines to type in all: 8. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `perft()` in `perft.py`

**Where:** lines 41 to 48 of `perft.py`, inside `perft()`, in place of the stub below the docstring. It is called by `divide()` in `perft.py`.

```python
25 | def perft(state: dict, depth: int) -> int:
26 |     """
     ...
39 |         The number of leaf positions. At depth 0 the position itself counts as 1.
40 |     """
41 +     if depth == 0:
42 +         return 1
43 +     count = 0
44 +     for move in legal_moves(state):
45 +         undo = make_move(state, move)
46 +         count += perft(state, depth - 1)  # Recursive call to itself
47 +         undo_move(state, undo)
48 +     return count
49 |
50 |
51 | def divide(state: dict, depth: int) -> dict[str, int]:
```

**How it works:** At depth 0 the position itself is one leaf. Otherwise the function makes each legal move, counts the leaves below it with `perft(state, depth - 1)`, and undoes the move before trying the next one. The total is the number of positions at the given depth. From the start position perft(3) is 8,902.
