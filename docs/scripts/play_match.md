# play_match.py: Two Remus brains play each other

*First appears in `instructor/Day 07 - Play full games in En Croissant`.*

## The big picture

Which brain is stronger? Let them play.

This file starts two copies of Remus and lets them play a match. python-chess acts as
the referee, so an illegal move is caught.

## Where this piece fits

play_match.py starts uci_engine.py twice. It uses python-chess, which only teacher tools may use.

- **Uses:** no other Remus file
- **Used by:** no other Remus file

## Words to know

- **referee:** a program that checks every move is legal.
- **match:** several games between the same two players, swapping colors.

## What it stores

On Day 10, `think` beat `greedy` 4 to 0.

## How it works

1. `start_engine()` starts one copy of Remus with a chosen brain.
2. `play_game()` asks each side for a move until the game ends.
3. `main()` swaps colors each game and keeps the score.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
main()
    start_engine()
    play_game()
```

## The functions

| Function | What it does | Day |
| --- | --- | --- |
| `start_engine` | Starts one copy of Remus with a chosen brain. | 7 |
| `play_game` | Plays one game and returns the result. | 7 |

## Try it

From inside a Day folder that has the file, run:

```bash
uv run play_match.py
```

You should see: Each game's result, then the final score.

## Puzzle questions

1. Why swap colors every game?

## Slides

Slides 7.7 in the [slide plan](../slide_plan.md).
