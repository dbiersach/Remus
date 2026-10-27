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

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `mvv_lva_score()` in `move_ordering.py`

Scores a capture: most valuable victim, least valuable attacker, so pawn takes queen comes first. Alpha-beta cuts off more of the tree when strong moves come first, so the same search finishes faster.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
