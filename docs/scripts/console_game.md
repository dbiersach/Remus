# console_game.py

Plays chess in the terminal with moves typed in SAN.

First appears in `instructor/Day 07 - Play full games in En Croissant`. Grows on Day 8, Day 9, Day 10.

## What it does

Two people take turns typing moves such as `e4` and `Nf3`; with `remus` as the
argument, Remus plays Black. Typing `quit` stops the game. The board prints after
every move.

## Program flow

The loop prints the board, reads a move with `parse_san` (an illegal move prints the
error and asks again), makes it, and repeats until `game_result` reports the end. On
Day 10, Remus plays from the opening book first, then thinks.

## Functions

| Function | Day | What it does |
| --- | --- | --- |

## Try it

From inside a Day folder in `instructor/` that has the file:

```bash
uv run console_game.py remus
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 1.1.
