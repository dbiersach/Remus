# mate_solver.py

Solves the ten GameWorks mate puzzles with a yes-or-no search.

First appears in `Day 10 - Upgrade Remus and add Science AI`.

## What it does

MATE.001 asks for White to mate in 2; the answer is Be4. A mate solver does not
compute scores. It asks whether the attacker has a move such that every defender
reply still allows mate in one move fewer.

## Program flow

`mating_move(state, moves_left)` tries each attacker move:

1. On the last allowed move, skip any move that does not give check: only a check can
   be mate.
2. If the defender has no replies, it is mate when in check and stalemate otherwise.
3. Otherwise, `defense_fails` must be true for every reply: after that reply,
   `mating_move(state, moves_left - 1)` still finds a mate.

Skipping quiet last moves makes the solver fast: all nine mates in 2 take well under
a second each, and MATE.008, a mate in 3 that takes the general search about two
minutes, falls in about 6 seconds. `read_puzzles` reads `tests/mate_puzzles.epd`.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `mating_move` | 10 | Find a move that forces checkmate within moves_left of the attacker's moves. |
| `defense_fails` | 10 | Return True if the attacker still mates in moves_left after this reply. |
| `read_puzzles` | 10 | Read mate puzzles from an EPD file. |

## Try it

From inside a Day folder that has the file:

```bash
uv run mate_solver.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 10.9.
