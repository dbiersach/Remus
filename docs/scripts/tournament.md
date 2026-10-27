# tournament.py: The class round robin

*First appears in `instructor/Day 10 - Aim Remus at a science problem/period4`.*

## The big picture

On Day 10, every pair's Remus plays every other pair's Remus once. That is a round
robin.

This file runs it with clocks, saves every game, and prints the standings after each
round.

## Where this piece fits

tournament.py starts each pair's uci_engine.py. It uses python-chess as the referee.

- **Uses:** no other Remus file
- **Used by:** no other Remus file

## Words to know

- **round robin:** everyone plays everyone once.
- **PGN:** a text file format for saving chess games.
- **circle method:** a way to pair players: one stays put, the others rotate.

## What it stores

Ten engines play 9 rounds and 45 games. Each engine plays White 4 or 5 times.
The clock gives 2 minutes plus 1 second per move.

## How it works

1. `round_robin()` makes the pairings for every round.
2. Four games run at the same time.
3. `play_game()` runs the clocks. An illegal move, a crash, or running out of time loses.
4. After each round, print the standings and add the games to games/remus_games.pgn.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
main()
    round_robin()
    play_game()
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `round_robin` | Makes the pairings for every round. | Day 10, period 4 |
| `play_game` | Plays one game on a clock and returns it as PGN. | Day 10, period 4 |

## Try it

From inside a period folder that has the file, run:

```bash
uv run tournament.py
```

You should see: With no arguments, a short demo of four brains, then the standings.

## Puzzle questions

1. How many games does a round robin of 6 engines need?

## Slides

Slides 10.10 in the [slide plan](../slide_plan.md).
