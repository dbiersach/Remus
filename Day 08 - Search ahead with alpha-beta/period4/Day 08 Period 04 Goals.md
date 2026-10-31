# Day 8, Period 4: Move ordering

## Learning objectives

By the end of this period, each student pair can:

- Order moves so the best ones come first. **Measured by:** The `mvv_lva_score` test passes: pawn takes queen scores above queen takes rook.
- Measure what ordering saves. **Measured by:** The student pair records node counts before and after ordering for one position.

## The files

New files this period:

- `move_ordering.py`

Files that grow this period:

- `search.py`: the teacher adds `check_time()`, `alpha_beta_with_quiescence()`; the teacher changes `quiescence()`
- `test_search.py`: 3 new tests

Functions the student pairs write this period:

- `mvv_lva_score()` in `move_ordering.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `mvv_lva_score()` in `move_ordering.py`

Scores a capture: most valuable victim, least valuable attacker, so pawn takes queen comes first. Alpha-beta cuts off more of the tree when strong moves come first, so the same search finishes faster.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Slides: alpha-beta cuts more when the best move comes first. Most valuable victim, least valuable attacker (MVV-LVA). |
| 3:15 to 3:40 | Student pairs write `mvv_lva_score()`. The teacher writes `order_moves()` and the check extension. |
| 3:40 to 4:05 | Student pairs measure node counts before and after ordering with `compare_search.py`. |
| 4:05 to 4:20 | Student pairs run the mate puzzles. |
| 4:20 to 4:30 | Checkpoint: every mate in 1 and every puzzle mate in 2. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `move_ordering.py` | `mvv_lva_score()` | 18 | 8 | `test_search.py::test_capture_moves_and_mvv_lva` |

Lines to type in all: 8. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `mvv_lva_score()` in `move_ordering.py`

**Where:** lines 36 to 43 of `move_ordering.py`, inside `mvv_lva_score()`, in place of the stub below the docstring. It is called by `order_moves()` in `move_ordering.py`.

```python
18 | def mvv_lva_score(move: Move, board: Board) -> int:
19 |     """
     ...
34 |         A promotion counts like capturing the new piece.
35 |     """
36 +     victim = piece_at(board, move.to_square)
37 +     attacker = piece_at(board, move.from_square)
38 +     score = 0
39 +     if victim != EMPTY:
40 +         score = 10 * PIECE_VALUES[victim.upper()] - PIECE_VALUES[attacker.upper()]
41 +     if move.promotion is not None:
42 +         score += 10 * PIECE_VALUES[move.promotion.upper()]
43 +     return score
44 |
45 |
46 | def order_moves(
```

**How it works:** MVV-LVA means most valuable victim, least valuable attacker. A capture scores 10 times the victim's value minus the attacker's value, so pawn takes queen (9,000 - 100) comes before queen takes queen (9,000 - 900). A quiet move scores 0. A promotion adds 10 times the new piece's value, as if it captured that piece.
