# game_end.py

Decides whether the game is over, and why.

First appears in `Day 07 - Play full games in En Croissant`.

## What it does

After 1. f3 e5 2. g4 Qh4, White has no legal moves and is in check: checkmate,
`("0-1", "checkmate")`. With no legal moves and no check, the game is stalemate.

## Program flow

`game_result(state)` checks, in order:

1. No legal moves: checkmate if the side to move is in check, otherwise stalemate.
2. `insufficient_material`: king against king, or king and one minor piece, or
   bishops all on one color of square.
3. `repetition_count(state)` of 3 or more: draw by repetition.
4. `halfmove_clock` of 100 or more: the fifty-move rule.

It returns `None` while the game goes on. Remus treats repetition and the fifty-move
rule as the end of the game, the way chess GUIs and engine tournaments do.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `insufficient_material` | 7 | Return True if neither side can ever checkmate. |
| `repetition_count` | 7 | Return how many times the current position has appeared in the game. |
| `game_result` | 7 | Return the result and the reason if the game is over, or None if it goes on. |

## Try it

From inside a Day folder that has the file:

```bash
uv run game_end.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 7.4, 7.5.
