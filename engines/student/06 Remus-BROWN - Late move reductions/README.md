# Remus-BROWN: Late move reductions

Search late, quiet moves one ply shallower, and in full only if they surprise.

## Learning objectives

By the end of Day 9, each student pair can:

- Explain the idea of this enhancement in two sentences. **Measured by:** The student pair explains the idea to another student pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `run_tests.py` passes in the version folder.
- Run a fair experiment: same opening, both piece colors. **Measured by:** In the Day 9 battles, `play_battle.py` in the version folder plays both 10-minute games with no illegal moves or crashes when the student pair presses Run in VS Code, and the student pair says why two games cannot show which enhancement is stronger.

## The idea, with an example

Remus orders its moves: the best move from the last depth first, then captures, then quiet moves. In a position with 35 moves, the best one is almost always among the first three. Remus-BROWN searches the first three moves at full depth and every later quiet move one ply shallower. A late move that still beats alpha at the shallower depth is a surprise, and Remus searches it again at full depth before trusting it.

## Why it makes Remus stronger

Most of a search's work goes into proving that bad moves are bad. Late move reductions prove it more cheaply, and the re-search keeps the rare good late move from being missed. Captures, promotions, and checks are never reduced, because they change the position too much to judge from a shallow search.

## What it costs

Each surprise costs a second search. The reduction only starts with 3 or more plies to go, so it does nothing in a depth 2 search.

## Measured against Remus-WHITE

Each version searched the ten positions of the designer's benchmark, `misc/designer/remus_benchmark.py`, one depth at a time up to depth 4, on one computer. Fewer positions for the same depth means a smaller search tree. Positions per second shows what each position costs. The last column gave each position 5 seconds, the way a game does, and averages the deepest search that finished.

| Version | Positions to finish depth 4 | Share of Remus-WHITE's | Positions per second | Average depth in 5 seconds |
| --- | ---: | ---: | ---: | ---: |
| Remus-WHITE | 431,212 | 100% | 5,183 | 3.1 |
| Remus-BROWN | 162,998 | 38% | 5,175 | 3.7 |

## What to expect

Fewer positions for the same depth, growing with depth, and now and then a different move, because a reduced search can miss a quiet move that only works deep down.

## Where your code fits

`reduced_search()` in `search.py` makes each move, asks `reduction()` how many plies to cut (1 or 0), and searches at `depth - 1 - cut`. If a cut search scores above alpha, it searches the move again at full depth. `LATE_MOVE_INDEX` (3) says where the late moves begin.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus in `00 Remus-WHITE - No enhancements` beside it, plus this one enhancement. The student pair writes `reduction()` in `search.py`, `test_only_late_quiet_moves_are_reduced()` in `test_upgrades.py`, `test_reduced_search_saves_work_and_keeps_the_state()` in `test_upgrades.py`.

## The changes and why

### `reduction()` in `search.py`

Returns 1 for a late, quiet move that gives no check at depth 3 or more, and 0 otherwise. Late moves in a well-ordered list are rarely best, so a shallower look saves time, and a surprise earns a full search.

### `test_only_late_quiet_moves_are_reduced()` in `test_upgrades.py`

Checks `reduction()` one condition at a time: a late quiet move is cut, and an early move, a move near the leaves, a capture, and a check are not.

### `test_reduced_search_saves_work_and_keeps_the_state()` in `test_upgrades.py`

Counts positions: the reduced search must visit fewer than the Day 9 search at the same depth and leave the position unchanged.

## Check it

Check the work by opening `run_tests.py` in this folder and pressing Run. Then open `basic_test.py` in VS Code and press Run: Remus-BROWN plays one 2-minute game against Remus-WHITE, which shows that the engine plays legal moves to the end of a game. In the Day 9 battles, follow the numbered steps at the top of `play_battle.py`: copy the visiting student pair's engine folder into `engines/student`, set `VISITING_ENGINE` to the visitor's engine color, and press Run. Remus-BROWN plays it twice at 10 minutes a side, once with each piece color, and both games go into misc/games/remus_games.pgn. Each script runs `misc/designer/version_match.py`, which plays the games.

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `reduction()` | 399 | 3 | `test_upgrades.py::test_only_late_quiet_moves_are_reduced` |
| `test_upgrades.py` | `test_only_late_quiet_moves_are_reduced()` | 22 | 6 | `run_tests.py` |
| `test_upgrades.py` | `test_reduced_search_saves_work_and_keeps_the_state()` | 32 | 9 | `run_tests.py` |

Lines to type in all: 18. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `reduction()` in `search.py`

**Where:** lines 425 to 427 of `search.py`, inside `reduction()`, in place of the stub below the docstring. It is called by `reduced_search()` in `search.py`.

```python
399 | def reduction(
400 |     depth: int, index: int, move: Move, captured: str, gives_check: bool
      ...
423 |         quiet move rarely turns out best. Otherwise 0.
424 |     """
425 +     late = index >= LATE_MOVE_INDEX and depth >= 3
426 +     quiet = captured == EMPTY and move.promotion is None
427 +     return 1 if late and quiet and not gives_check else 0
428 |
429 |
430 | def reduced_search(
```

**How it works:** `index` is the move's place in the ordered list, counting from 0, so `index >= LATE_MOVE_INDEX` (3) means the fourth move or later. `depth >= 3` keeps the reduction away from the last plies, where one ply matters most. `quiet` is True for a move that captures nothing (`captured == EMPTY`) and does not promote. The last line returns 1, meaning search this move one ply shallower, only for a late, quiet move that does not give check. Every other move returns 0 and gets the full depth.

### `test_only_late_quiet_moves_are_reduced()` in `test_upgrades.py`

**Where:** lines 24 to 29 of `test_upgrades.py`, inside `test_only_late_quiet_moves_are_reduced()`, in place of the stub below the docstring. `run_tests.py` runs it with every other test in the folder.

```python
22 | def test_only_late_quiet_moves_are_reduced() -> None:
23 |     """Expected: only a late, quiet move with no check and 3 plies to go loses 1 ply."""
24 +     quiet = Move((6, 0), (5, 0))
25 +     assert reduction(4, 5, quiet, EMPTY, False) == 1
26 +     assert reduction(4, 1, quiet, EMPTY, False) == 0  # Early in the list
27 +     assert reduction(2, 5, quiet, EMPTY, False) == 0  # Too close to the leaves
28 +     assert reduction(4, 5, quiet, "p", False) == 0  # A capture
29 +     assert reduction(4, 5, quiet, EMPTY, True) == 0  # A check
30 |
31 |
32 | def test_reduced_search_saves_work_and_keeps_the_state() -> None:
```

**How it works:** The test builds one quiet pawn move, a2a3, and asks `reduction` about it five times, changing one thing each time. At depth 4 and index 5 with no capture and no check the answer is 1. Each other line breaks one condition, an early index, a depth of 2, a captured pawn, or a check, and expects 0.

### `test_reduced_search_saves_work_and_keeps_the_state()` in `test_upgrades.py`

**Where:** lines 34 to 42 of `test_upgrades.py`, inside `test_reduced_search_saves_work_and_keeps_the_state()`, in place of the stub below the docstring. `run_tests.py` runs it with every other test in the folder.

```python
32 | def test_reduced_search_saves_work_and_keeps_the_state() -> None:
33 |     """The upgraded search visits fewer positions than plain alpha-beta at depth 4."""
34 +     state = state_from_fen(ITALIAN)
35 +     before = state_snapshot(state)
36 +     plain = SearchInfo()
37 +     upgraded = SearchInfo()
38 +     alpha_beta_with_quiescence(state, 4, 0, *WIDE, plain)
39 +     _, pv = reduced_search(state, 4, 0, *WIDE, upgraded)
40 +     assert upgraded.nodes < plain.nodes
41 +     assert pv
42 +     assert state_snapshot(state) == before
```

**How it works:** Two `SearchInfo` records count positions: `plain` for ordinary alpha-beta and `upgraded` for `reduced_search`, both at depth 4 on the Italian opening. The asserts check that the reduced search visits fewer positions, that it returns a line of moves, and that the state snapshot is unchanged afterward.
