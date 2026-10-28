# Day 10, Period 3: The phase hunt: search every set, and verify

## Learning objectives

By the end of this period, each pair can:

- Search every set of phases with make and undo, as Remus searches moves. **Measured by:** The `search` tests pass: the phases list comes back unchanged, and the search scores 176 sets, one for each set of up to three phases.
- Verify a method against known answers, and say when the data cannot decide. **Measured by:** Running `phase_hunt.py` shows the search making fewer wrong calls than greedy, and the pair names the extra measurement that would tell gold from silver.

## The tree you search

In period 2, `greedy_phases()` built one guess, one phase at a time. In this period,
`search()` scores **every** guess of up to three phases. The guesses form a tree,
like Remus's game tree: the empty guess at the top, one more phase on each level
down. Going down a branch adds a phase (`append`, like making a move), and coming
back up takes it out (`pop`, like undoing it). The period 2 README explains the
experiment and the score.

![The tree of guesses for powder 23, using 4 of the 10 phases and 2 levels, with
the score of each guess; silicon + halite scores best](../../../docs/images/phase_hunt/search_tree.png)

Silicon + halite is the same guess as halite + silicon, just as two move orders can
reach the same chess position. So `search()` adds phases only in library order,
from `PHASE_NAMES[start]` on. With 10 phases and 3 levels, that scores 176 guesses
instead of 821.

`search()` keeps every guess that ties for the best score in `hunt.sets`, not just
the first. When the answer is one guess, the search is sure. When gold and silver tie,
the answer holds both, and the verdict is "can't tell".

![Over 200 powders, greedy is right 166 times and wrong 34 times; the search is
right 139 times, says can't tell 52 times, and is wrong 9
times](../../../docs/images/phase_hunt/verdicts.png)

Greedy names more powders right, because it guesses gold every time and gold is
right half the time. The search is wrong far less often, and it says so when the
pattern cannot decide. A scientist then takes a second measurement, such as X-ray
fluorescence, which tells gold from silver at once.

## The files

The engine for Day 10 is Remus-GOLD, the finished Remus with all ten enhancements, in the `Remus/11 GOLD - All enhancements` folder beside the Day folders. Lucas Chess runs its `remus.bat`, and its `estimate_elo.py` rates it against Stockfish. This folder holds only the science files, which never import the engine.

Files that grow this period:

- `phase_hunt.py`
- `test_phase_hunt.py`

Functions the pairs write this period:

- `search()` in `phase_hunt.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `search()` in `phase_hunt.py`

Scores the set of phases it is given, keeps every set that ties for the best score, and calls itself on each set one phase larger, adding a phase with append and taking it back with pop. Phases go in library order only, so each set is scored once instead of once for every order, 176 sets instead of 821. Keeping every tied set lets the search say gold or silver when the pattern cannot tell them apart, as CrystalShift and Dara report every likely answer.

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `hidden_peak.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `phase_hunt.py` | `search()` | 187 | 13 | `test_phase_hunt.py::test_search_leaves_the_phases_as_it_found_them` |

Lines to type in all: 13. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
