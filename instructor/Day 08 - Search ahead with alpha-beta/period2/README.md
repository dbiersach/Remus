# Day 8, Period 2: Python lab 11 and alpha-beta

## Learning objectives

By the end of this period, each pair can:

- Explain an alpha-beta cutoff. **Measured by:** "Fewest flips": the pair reaches the right move while turning fewer cards than the whole tree.
- Show that alpha-beta keeps the answer and saves work. **Measured by:** The `alpha_beta` tests pass, and `uv run compare_search.py` prints the same scores as negamax with fewer nodes.

## The files

New files this period:

- `compare_search.py`

Files that grow this period:

- `search.py`
- `test_search.py`

Functions the pairs write this period:

- `alpha_beta()` in `search.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `alpha_beta()` in `search.py`

Does the same work as negamax, but carries two numbers: alpha, the score the mover is already sure of, and beta, the score the opponent will not allow. As soon as one move scores beta or more, the opponent would never let this position happen, so the other moves are skipped. The answer is the same as negamax, and far fewer positions are visited, so Remus can look deeper in the same time.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
