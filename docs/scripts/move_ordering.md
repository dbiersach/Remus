# move_ordering.py

Puts the moves most likely to be best first.

First appears in `instructor/Day 09 - Search faster with alpha-beta`. Grows on Day 10.

## What it does

Alpha-beta cuts off more of the tree when a strong move comes early. With a pawn able
to take a queen and a queen able to take a pawn, the pawn capture goes first.

## Program flow

`mvv_lva_score` scores a capture by Most Valuable Victim, Least Valuable Attacker:
ten times the victim's value minus the attacker's value. `order_moves` sorts by that
score, puts a `first` move (the previous depth's best, or the transposition table's
move) ahead of everything, and on Day 10 places up to two killer moves right after
the captures with `KILLER_SCORE`.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `mvv_lva_score` | 9 | Score a move for ordering: high for a big capture by a small piece. |
| `order_moves` | 9 | Return the moves sorted best first. |

## Try it

From inside a Day folder in `instructor/` that has the file:

```bash
uv run move_ordering.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 9.4, 10.4.
