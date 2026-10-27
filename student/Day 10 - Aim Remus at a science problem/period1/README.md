# Day 10, Period 1: Science AI: hidden_peak.py

## Learning objectives

By the end of this period, each pair can:

- Map the chess engine's loop onto a measurement problem. **Measured by:** The pair fills in the chess-to-science table: legal moves, evaluation, and greedy move each have a science partner.
- Balance exploring and exploiting. **Measured by:** The pair's `choose_next_measurement()` beats random guessing on the 100-grid benchmark, and the pair names the explore weight it chose.

## The files

New files this period:

- `hidden_peak.py`
- `opening_book.py`
- `opening_book.txt`
- `test_upgrades.py`
- `transposition_table.py`

Files that grow this period:

- `console_game.py`
- `evaluation.py`
- `move_ordering.py`
- `search.py`
- `uci_engine.py`

Functions the pairs write this period:

- `candidate_squares()` in `hidden_peak.py`
- `score_candidate()` in `hidden_peak.py`
- `choose_next_measurement()` in `hidden_peak.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `candidate_squares()` in `hidden_peak.py`

Lists every square not measured yet. These are the "legal moves" of the science problem: the places the AI could measure next.

### `score_candidate()` in `hidden_peak.py`

Scores a square by its predicted value plus a bonus for being far from earlier readings. The first part exploits what the AI knows, and the second explores where it knows little.

### `choose_next_measurement()` in `hidden_peak.py`

Returns the candidate with the highest score, just as `greedy_move()` returns the best capture. The same generate, score, and choose loop now runs on a science problem.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `hidden_peak.py` | `candidate_squares()` | 85 | 6 | `test_upgrades.py::test_greedy_ai_measures_where_it_looks_hot` |
| `hidden_peak.py` | `score_candidate()` | 104 | 4 | `uv run pytest` |
| `hidden_peak.py` | `choose_next_measurement()` | 132 | 9 | `test_upgrades.py::test_greedy_ai_measures_where_it_looks_hot`, `test_upgrades.py::test_greedy_ai_beats_random_guessing` |

Lines to type in all: 19. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
