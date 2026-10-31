# Day 8, Period 3: The horizon effect and quiescence

## Learning objectives

By the end of this period, each student pair can:

- Explain the horizon effect. **Measured by:** The student pair explains why depth 2 takes a defended pawn with the queen.
- List the moves quiescence searches. **Measured by:** The `quiescence` tests pass, and the student pair explains what "stand pat" means with the defended-pawn position.

## The files

Files that grow this period:

- `search.py`: the teacher adds `capture_moves()`
- `test_search.py`: 1 new test

Functions the student pairs write this period:

- `quiescence()` in `search.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `quiescence()` in `search.py`

Keeps searching captures after the depth runs out, so Remus never judges a position in the middle of a trade. The mover may "stand pat" and take the evaluation as it is, or try a capture that does better. Without it, a search that stops after queen takes pawn misses the pawn that takes the queen back.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | Puzzle: at depth 2 Remus takes a defended pawn with its queen. Why? The class names the horizon effect. |
| 1:15 to 1:30 | Slides: quiescence keeps searching captures until the position is quiet. The teacher writes `capture_moves()`. |
| 1:30 to 2:10 | Student pairs write `quiescence()`, which may stand pat with the evaluation or try a capture that does better. |
| 2:10 to 2:20 | Student pairs run the puzzle again: Remus keeps its queen. |
| 2:20 to 2:30 | Show and choose for `quiescence()`. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `quiescence()` | 273 | 15 | `test_search.py::test_quiescence_stands_pat_or_takes_a_free_pawn` |

Lines to type in all: 15. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `quiescence()` in `search.py`

**Where:** lines 298 to 312 of `search.py`, inside `quiescence()`, in place of the stub below the docstring. The tests call it directly.

```python
273 | def quiescence(state: dict, alpha: int, beta: int, info: SearchInfo) -> int:
274 |     """
      ...
296 |         The score for the side to move.
297 |     """
298 +     info.nodes += 1
299 +     stand_pat = evaluate(state)
300 +     if stand_pat >= beta:
301 +         return stand_pat
302 +     alpha = max(alpha, stand_pat)
303 +     for move in capture_moves(state):
304 +         undo = make_move(state, move)
305 +         try:
306 +             score = -quiescence(state, -beta, -alpha, info)  # Recursive call to itself
307 +         finally:
308 +             undo_move(state, undo)
309 +         if score >= beta:
310 +             return score
311 +         alpha = max(alpha, score)
312 +     return alpha
313 |
314 |
315 | def main():
```

**How it works:** Quiescence keeps searching captures after the main search ends, so Remus never stops in the middle of a trade. The side to move may stand pat, keeping the score it has without capturing. If that score already reaches `beta`, the opponent avoids this position, so the function returns at once. Otherwise each capture is made, searched with the window flipped, and undone, with the same cutoff as alpha-beta.
