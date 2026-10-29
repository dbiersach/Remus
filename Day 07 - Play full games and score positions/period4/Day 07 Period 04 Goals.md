# Day 7, Period 4: What makes a position good? Material and piece-square tables

## Learning objectives

By the end of this period, each pair can:

- Count material in centipawns. **Measured by:** The evaluation tests pass, and running `evaluation.py` prints -200 for a knight against a rook.
- Explain a piece-square table. **Measured by:** The pair says why a knight scores more on d4 than on a1, using the number of squares it attacks (8 and 2).

## The files

New files this period:

- `evaluation.py`
- `test_search.py`

Functions the pairs write this period:

- `material()` in `evaluation.py`

In the `student` folder these functions raise `NotImplementedError` until a pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `material()` in `evaluation.py`

Adds up the pieces in centipawns (pawn 100, knight 300, bishop 300, rook 500, queen 900), plus for White and minus for Black. It is the first evaluation term, and the search uses it to tell good positions from bad ones.

Check the work with the tests: open a terminal in VS Code inside the `student` folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).

## The period step by step

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Pairs rank three printed positions and write one reason for each. The reasons become the evaluation terms. |
| 3:15 to 3:25 | Chess refresher: piece values (pawn 1, knight 3, bishop 3, rook 5, queen 9) and the fork, pin, and skewer. |
| 3:25 to 3:50 | Pairs write `material()` in centipawns, scored for White. |
| 3:50 to 4:05 | The teacher shows the piece-square tables and `explain_evaluation()`, which prints every term. A knight on d4 attacks eight squares; on a1 it attacks two. |
| 4:05 to 4:25 | Each pair proposes one change to one table, and the class votes. |
| 4:25 to 4:30 | Checkpoint: `explain_evaluation()` gives 0 for the start. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `evaluation.py` | `material()` | 79 | 10 | `test_search.py::test_start_position_is_level` |

Lines to type in all: 10. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
