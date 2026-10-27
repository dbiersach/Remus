# Day 7, Period 3: First brains and the GUI

Register `remus.bat` from this folder in Lucas Chess again: Remus now plays greedy moves. `uv run play_match.py` plays random Remus against greedy Remus.

## Learning objectives

By the end of this period, each pair can:

- Choose a random move and a greedy move. **Measured by:** The brain tests pass: greedy Remus takes a hanging queen.
- Explain what the UCI commands do. **Measured by:** The pair explains `position`, `go`, and `bestmove` from a printed conversation.
- Measure one brain against another. **Measured by:** `uv run play_match.py` shows greedy Remus scoring more than random Remus.

## The files

New files this period:

- `play_match.py`
- `search.py`

Files that grow this period:

- `console_game.py`
- `test_game.py`
- `uci_engine.py`

Functions the pairs write this period:

- `random_move()` in `search.py`
- `greedy_move()` in `search.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `random_move()` in `search.py`

Picks any legal move at random. It is Remus's first brain: weak, but it proves the engine can play a whole game legally.

### `greedy_move()` in `search.py`

Picks the move that captures the most valuable piece, after shuffling so ties are broken at random. Greedy Remus beats random Remus, yet falls for any trap one move deep, which is why searching ahead comes next.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
