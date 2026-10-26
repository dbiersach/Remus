# perft.py

Counts positions in the move tree to prove the rules are right.

First appears in `instructor/Day 06 - Count positions with perft`.

## What it does

From the start position, White has 20 moves, the two sides together reach 400
positions after two moves, 8,902 after three, and 197,281 after four. Chess
programmers have published these counts for many positions. When Remus's count
matches, every rule it exercised is right; when it differs, a rule is wrong.

## Program flow

`perft(state, depth)` returns 1 at depth 0. Otherwise it loops over `legal_moves`,
makes each move, adds `perft(state, depth - 1)`, and undoes the move.

`divide(state, depth)` returns the count under each root move separately, as a dict
from UCI text to count. Comparing that dict with a reference program points to the one
root move whose count is wrong; repeat `divide` one move deeper until the bug shows.

The tests check the start position and four well-known test positions (including
"Kiwipete", 97,862 at depth 3) against counts written down before the run, then
against `python-chess`.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `perft` | 6 | Count the positions reached after exactly `depth` moves. |
| `divide` | 6 | Split a perft count by root move, to find which move a bug hides under. |

## Try it

From inside a Day folder in `instructor/` that has the file:

```bash
uv run perft.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 6.1, 6.2, 6.3.
