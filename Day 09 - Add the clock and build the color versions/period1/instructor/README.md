# Day 9, Period 1: Iterative deepening, the clock, and UCI info

## Learning objectives

By the end of this period, each pair can:

- Search deeper one step at a time until the clock runs out. **Measured by:** `test_think_respects_its_time` passes, and Remus never loses on time in Lucas Chess.
- Report the search to the GUI with `info` lines. **Measured by:** Lucas Chess shows Remus's depth, score, and best line for each depth that `think()` finishes.

## The files

Files that grow this period:

- `console_game.py`
- `search.py`
- `test_game.py`
- `test_search.py`
- `uci_engine.py`

Functions the pairs write this period:

- `think()` in `search.py`

In the `student` folder these functions raise `NotImplementedError` until a pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `think()` in `search.py`

Searches depth 1, then depth 2, then depth 3, and keeps the best move of the deepest search that finished. When the clock runs out in the middle of a search, the unfinished search is thrown away. Each finished depth also puts its best move first for the next depth, so alpha-beta cuts off more. This is iterative deepening, and it lets Remus play on any clock.

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).
