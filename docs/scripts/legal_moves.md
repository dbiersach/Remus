# legal_moves.py

Keeps only the legal moves, and adds castling.

First appears in `Day 04 - Keep only legal moves`. Grows on Day 5.

## What it does

A knight pinned to its king has pseudo-legal moves but no legal ones. This module
finds that out with one rule: make the move, and keep it only if the mover's king is
not attacked afterward.

## Program flow

1. `legal_moves(state)` takes every move from `pseudo_legal_moves` and, from Day 5,
   `castling_moves`.
2. For each move: `make_move`, then `in_check` for the side that just moved, then
   `undo_move`.
3. The move joins the list only if the king was safe.

Testing after the move catches pins, discovered checks, and en passant captures that
expose the king, with no special cases.

## Data structure: the castling table

Each row of `CASTLES` holds the right's letter (`"K"`, `"Q"`, `"k"`, `"q"`), the
king's start and target squares, the squares that must be empty, and the square the
king passes through. `castling_moves` checks the right, the empty squares, that the
king is not in check, and that neither the passing nor the landing square is attacked.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `castling_moves` | 5 | Return the castling moves the side to move may make. |
| `legal_moves` | 4 | Return every legal move for the side to move. |

## Try it

From inside a Day folder that has the file:

```bash
uv run legal_moves.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 4.3, 4.4, 5.1, 5.5.
