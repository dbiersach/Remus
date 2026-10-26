# transposition_table.py

Remembers positions the search has already scored.

First appears in `Day 10 - Upgrade Remus and add Science AI`.

## What it does

1. Nf3 Nf6 2. Nc3 and 1. Nc3 Nf6 2. Nf3 reach the same position. A plain dict keyed by
`position_key` lets the search score that position once.

## Data structure

Each entry is a dict: `depth`, `score`, `bound`, and `best` move. An alpha-beta score
is not always exact, so `bound` says what the score proves:

| Bound | Meaning |
| --- | --- |
| `EXACT` | The true score at that depth |
| `LOWER` | A cutoff happened: the true score is at least this much |
| `UPPER` | No move beat alpha: the true score is at most this much |

## Program flow

`store` keeps the deeper of two results. `probe` returns a stored score only when it
was searched deep enough and its bound settles the current window. Even when `probe`
returns `None`, `best_stored_move` gives the search a strong move to try first.
`upgraded_search` does not store mate scores, because they depend on the distance
from the root.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `store` | 10 | Save a search result for a position, keeping the deeper of two results. |
| `probe` | 10 | Return a stored score that answers this search, or None. |
| `best_stored_move` | 10 | Return the best move stored for a position, to try first. |

## Try it

From inside a Day folder that has the file:

```bash
uv run transposition_table.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 10.2, 10.3.
