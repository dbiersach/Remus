# Teacher tools: play_match.py, compare_search.py, tournament.py, run_all_tests.py

Teacher tools that referee games and compare searches.

## What they do

These scripts are teacher tools. They use `python-chess` as an outside referee, so an
illegal move from Remus is caught; the engine itself never imports `python-chess`.

| Script | Day | What it does |
| --- | --- | --- |
| `play_match.py` | 7 | Plays two brains against each other: `uv run play_match.py random greedy 20`. On Day 10, `think` beats `greedy` 4 to 0 |
| `compare_search.py` | 9 | Searches ten positions with `negamax` and `alpha_beta` at depth 3: the same scores, with alpha-beta visiting less than a fifth of the positions |
| `tournament.py` | 10 | Runs the round robin: every pair's engine plays every other once at 2 minutes plus 1 second a move, four games at a time, saving `tournament.pgn` and printing standings after each round |
| `run_all_tests.py` | all | At the repository root: runs pytest on each Day folder in turn, then `tests/` |

## Program flow of `tournament.py`

1. Each argument is a pair's Remus folder; the folder name is the team name.
2. `round_robin` pairs the entrants with the circle method: entrant 0 stays put and
   the others rotate one seat per round. Ten entrants play 9 rounds, 45 games, and
   each plays White four or five times.
3. `play_game` runs a chess clock for each side. An illegal move, an engine error, or
   a flag fall loses the game, and the reason is saved in the PGN.

With no arguments, the four brains of the Day 10 folder play a short demo.

## Try it

From inside `Day 10 - Upgrade Remus and add Science AI`:

```bash
uv run tournament.py
```

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 10.10, 9.2.
