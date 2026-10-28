# Day 10, Period 2: The phase hunt: score a guess, and the greedy agent

`uv run phase_hunt.py` names the crystal phases in an X-ray powder pattern and counts the right and wrong calls over 200 powders.

## Learning objectives

By the end of this period, each pair can:

- Score a guess about what a powder holds. **Measured by:** The `score` test passes, and the pair explains why an extra phase costs a point even when every peak is explained.
- Build an answer greedily, one best step at a time. **Measured by:** The `greedy_phases` tests pass, and the pair explains why greedy names gold for a powder that holds silver.

## The files

New files this period:

- `phase_hunt.py`
- `test_phase_hunt.py`

Functions the pairs write this period:

- `score()` in `phase_hunt.py`
- `greedy_phases()` in `phase_hunt.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `score()` in `phase_hunt.py`

Scores a guess about which phases are in the powder: a point for each measured peak the phases explain, and a point lost for each peak left over, each predicted peak that is missing, and each phase used. It is the evaluation of the science problem, like `material()` for a chess position, and the cost per phase makes the simpler explanation win a tie.

### `greedy_phases()` in `phase_hunt.py`

Adds the phase that raises the score most, then the next, and stops when no phase helps, the way `greedy_move()` takes the biggest capture. Each phase is tried with append and taken back with pop, like make and undo. Greedy gives one answer and never doubts it, so it names gold for a powder of silver.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `phase_hunt.py` | `score()` | 110 | 11 | `test_phase_hunt.py::test_score_rewards_explained_peaks_and_punishes_the_rest`, `test_search.py::test_negamax_finds_mate_in_one`, `test_search.py::test_quiescence_stands_pat_or_takes_a_free_pawn`, `test_search.py::test_gameworks_mate_in_two_puzzles`, `test_upgrades.py::test_upgraded_search_finds_a_mate_in_two` |
| `phase_hunt.py` | `greedy_phases()` | 134 | 17 | `test_phase_hunt.py::test_greedy_names_a_clean_mixture`, `test_phase_hunt.py::test_greedy_mistakes_silver_for_gold` |

Lines to type in all: 28. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
