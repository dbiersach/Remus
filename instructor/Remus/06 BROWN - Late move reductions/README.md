# Remus-BROWN: Late move reductions

Search late, quiet moves one ply shallower, and in full only if they surprise.

## Learning objectives

By the end of Day 9, each pair can:

- Explain the idea of the color version's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the version folder.
- Run a fair experiment against Remus-WHITE: same opening, both colors. **Measured by:** In the Day 10 tournament, `play_tournament.py` in the version folder plays both 10-minute games with no illegal moves or crashes when the pair presses Run in VS Code, and the pair says why two games cannot show whether the enhancement helps.

## The idea, with an example

Remus orders its moves: the best move from the last depth first, then captures, then quiet moves. In a position with 35 moves, the best one is almost always among the first three. Remus-BROWN searches the first three moves at full depth and every later quiet move one ply shallower. A late move that still beats alpha at the shallower depth is a surprise, and Remus searches it again at full depth before trusting it.

## Why it makes Remus stronger

Most of a search's work goes into proving that bad moves are bad. Late move reductions prove it more cheaply, and the re-search keeps the rare good late move from being missed. Captures, promotions, and checks are never reduced, because they change the position too much to judge from a shallow search.

## What it costs

Each surprise costs a second search. The reduction only starts with 3 or more plies to go, so it does nothing in a depth 2 search.

## Measured against Remus-WHITE

Each version searched the ten positions of `compare_search.py`, one depth at a time up to depth 4, on one computer. Fewer positions for the same depth means a smaller search tree. Positions per second shows what each position costs. The last column gave each position 5 seconds, the way a game does, and averages the deepest search that finished.

| Version | Positions to finish depth 4 | Share of Remus-WHITE's | Positions per second | Average depth in 5 seconds |
| --- | ---: | ---: | ---: | ---: |
| Remus-WHITE | 431,212 | 100% | 5,183 | 3.1 |
| Remus-BROWN | 162,998 | 38% | 5,175 | 3.7 |

## What to expect

Fewer positions for the same depth, growing with depth, and now and then a different move, because a reduced search can miss a quiet move that only works deep down.

## Where your code fits

`reduced_search()` in `search.py` makes each move, asks `reduction()` how many plies to cut (1 or 0), and searches at `depth - 1 - cut`. If a cut search scores above alpha, it searches the move again at full depth. `LATE_MOVE_INDEX` (3) says where the late moves begin.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `reduction()` in `search.py`, `test_only_late_quiet_moves_are_reduced()` in `test_upgrades.py`, `test_reduced_search_saves_work_and_keeps_the_state()` in `test_upgrades.py`.

## The changes and why

### `reduction()` in `search.py`

Returns 1 for a late, quiet move that gives no check at depth 3 or more, and 0 otherwise. Late moves in a well-ordered list are rarely best, so a shallower look saves time, and a surprise earns a full search.

### `test_only_late_quiet_moves_are_reduced()` in `test_upgrades.py`

Checks `reduction()` one condition at a time: a late quiet move is cut, and an early move, a move near the leaves, a capture, and a check are not.

### `test_reduced_search_saves_work_and_keeps_the_state()` in `test_upgrades.py`

Counts positions: the reduced search must visit fewer than the Day 9 search at the same depth and leave the position unchanged.

## Check it

Check the work from inside this folder with `uv run pytest`. Then open `smoke_test.py` in VS Code and press Run: Remus-BROWN plays one 2-minute game against Remus-WHITE, which shows that the engine plays legal moves to the end of a game. In the Day 10 tournament, open `play_tournament.py` and press Run: Remus-BROWN plays Remus-WHITE twice, once with each color, at 10 minutes a side, and both games go into games/remus_games.pgn. Each script runs `version_match.py` from the `Remus` folder above this one.
