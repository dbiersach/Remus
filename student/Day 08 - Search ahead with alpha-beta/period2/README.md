# Day 8, Period 2: Python lab 11 and alpha-beta

## Learning objectives

By the end of this period, each pair can:

- Explain an alpha-beta cutoff. **Measured by:** "Fewest flips": the pair reaches the right move while turning fewer cards than the whole tree.
- Show that alpha-beta keeps the answer and saves work. **Measured by:** The `alpha_beta` tests pass, and `uv run compare_search.py` prints the same scores as negamax with fewer nodes.
- Keep a list in order with `insert()`, start a best value at minus infinity, and time code. **Measured by:** `python_sorting.py` puts the queen first, finds the best victim, and prints the run time of `perft(3)`.

## The files

The lab is `python_sorting.py` in `student/`, with the answers in `python_sorting_instructor.py` in `instructor/`. Run it with `uv run python_sorting.py`.

New files this period:

- `compare_search.py`

Files that grow this period:

- `search.py`
- `test_search.py`

Functions the pairs write this period:

- `alpha_beta()` in `search.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

The pairs fill in the blanks of `python_sorting.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_sorting_instructor.py`.

Part #1 sorts captures by the value of the piece they take: each new piece steps past every piece worth at least as much and is inserted there. `order_moves()` in period 4 sorts moves the same way.

Part #2 starts the best value at minus infinity, so the first real value always replaces it. `alpha_beta()` starts its alpha the same way, below any score a move can get.

Part #3 times `perft(3)` with `time.perf_counter()`, the clock that `compare_search.py` uses to show how much time alpha-beta saves.

### `alpha_beta()` in `search.py`

Does the same work as negamax, but carries two numbers: alpha, the score the mover is already sure of, and beta, the score the opponent will not allow. As soon as one move scores beta or more, the opponent would never let this position happen, so the other moves are skipped. The answer is the same as negamax, and far fewer positions are visited, so Remus can look deeper in the same time.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `alpha_beta()` | 197 | 16 | `test_search.py::test_alpha_beta_matches_negamax_with_fewer_positions` |

Lines to type in all: 16. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## What you edit in the lab

Open `python_sorting.py`. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 19. Check the work with `uv run python_sorting.py` and compare each printed result with the expected value beside it.
