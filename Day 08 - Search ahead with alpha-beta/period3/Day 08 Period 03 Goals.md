# Day 8, Period 3: The horizon effect and quiescence

## Learning objectives

By the end of this period, each pair can:

- Explain the horizon effect. **Measured by:** The pair explains why depth 2 takes a defended pawn with the queen.
- List the moves quiescence searches. **Measured by:** The `quiescence` tests pass, and the pair explains what "stand pat" means with the defended-pawn position.

## The files

Files that grow this period:

- `search.py`
- `test_search.py`

Functions the pairs write this period:

- `quiescence()` in `search.py`

In the `student` folder these functions raise `NotImplementedError` until a pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `quiescence()` in `search.py`

Keeps searching captures after the depth runs out, so Remus never judges a position in the middle of a trade. The mover may "stand pat" and take the evaluation as it is, or try a capture that does better. Without it, a search that stops after queen takes pawn misses the pawn that takes the queen back.

Check the work with the tests: open a terminal in VS Code inside the `student` folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).

## The period step by step

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | Puzzle: at depth 2 Remus takes a defended pawn with its queen. Why? The class names the horizon effect. |
| 1:15 to 1:30 | Slides: quiescence keeps searching captures until the position is quiet. The teacher writes `capture_moves()`. |
| 1:30 to 2:10 | Pairs write `quiescence()`, which may stand pat with the evaluation or try a capture that does better. |
| 2:10 to 2:20 | Pairs run the puzzle again: Remus keeps its queen. |
| 2:20 to 2:30 | Show and choose for `quiescence()`. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `quiescence()` | 271 | 15 | `test_search.py::test_quiescence_stands_pat_or_takes_a_free_pawn` |

Lines to type in all: 15. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
