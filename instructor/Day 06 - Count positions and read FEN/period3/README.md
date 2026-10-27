# Day 6, Period 3: Perft against python-chess, and bug hunt

The `bug_hunt` folder holds a copy of this period's Remus with three planted bugs. `uv run hunt.py` inside it shows where the counts go wrong.

## Learning objectives

By the end of this period, each pair can:

- Compare Remus with python-chess on standard positions. **Measured by:** `test_perft.py` passes on all five positions.
- Find a planted bug with `divide()`. **Measured by:** `uv run hunt.py` in `bug_hunt/` points at three bugs; the pair fixes at least two of them and names the root move that showed each one.

## The files

New files this period:

- `test_perft.py`

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
