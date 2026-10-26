# notation.py

Writes and reads moves in SAN, the notation people use.

First appears in `instructor/Day 07 - Play full games in En Croissant`.

## What it does

People write `Nf3`, `exd5`, `O-O`, and `e8=Q+`. `move_to_san` writes a legal move
that way, adding `+` for check and `#` for mate. When two knights can reach d2,
`disambiguation` adds the file, rank, or square that tells them apart, as in `Nbd2`.

## Program flow

`parse_san(state, text)` uses one simple idea: write the SAN of every legal move and
return the one that matches what the player typed. It ignores a trailing `+`, `#`,
`!`, or `?` and accepts `0-0` for `O-O`. A text that matches no legal move raises
`ValueError`, so an illegal move can never enter the game through SAN.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `move_to_san` | 7 | Return the SAN text of a legal move in the current position. |
| `disambiguation` | 7 | Return the file, rank, or square that tells this move apart from another legal move by the same kind of piece to the same square, such as "b" in "Nbd2". |
| `parse_san` | 7 | Find the legal move that a SAN text describes. |

## Try it

From inside a Day folder in `instructor/` that has the file:

```bash
uv run notation.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 7.2, 7.3.
