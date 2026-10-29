# Day 8, Period 4: Move ordering

## Learning objectives

By the end of this period, each pair can:

- Order moves so the best ones come first. **Measured by:** The `mvv_lva_score` test passes: pawn takes queen scores above queen takes rook.
- Measure what ordering saves. **Measured by:** The pair records node counts before and after ordering for one position.

## The files

New files this period:

- `move_ordering.py`

Files that grow this period:

- `search.py`
- `test_search.py`

Functions the pairs write this period:

- `mvv_lva_score()` in `move_ordering.py`

In the `student` folder these functions raise `NotImplementedError` until a pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `mvv_lva_score()` in `move_ordering.py`

Scores a capture: most valuable victim, least valuable attacker, so pawn takes queen comes first. Alpha-beta cuts off more of the tree when strong moves come first, so the same search finishes faster.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Slides: alpha-beta cuts more when the best move comes first. Most valuable victim, least valuable attacker (MVV-LVA). |
| 3:15 to 3:40 | Pairs write `mvv_lva_score()`. The teacher writes `order_moves()` and the check extension. |
| 3:40 to 4:05 | Pairs measure node counts before and after ordering with `compare_search.py`. |
| 4:05 to 4:20 | Pairs run the mate puzzles. |
| 4:20 to 4:30 | Checkpoint: every mate in 1 and every puzzle mate in 2. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `move_ordering.py` | `mvv_lva_score()` | 18 | 8 | `test_search.py::test_capture_moves_and_mvv_lva` |

Lines to type in all: 8. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
