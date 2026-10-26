# uci_engine.py

Connects Remus to En Croissant through UCI.

First appears in `instructor/Day 07 - Play full games in En Croissant`. Grows on Day 8, Day 9, Day 10.

## What it does

En Croissant sends one command per line, and Remus answers on standard output:

```text
GUI:   uci                         Remus: id name Remus ... uciok
GUI:   isready                     Remus: readyok
GUI:   position startpos moves e2e4
GUI:   go wtime 60000 btime 60000  Remus: info depth 3 ... then bestmove e7e5
```

Debug text goes to standard error, which the GUI ignores. `remus.bat` starts the
engine on Windows so En Croissant can launch it.

## Program flow

1. `set_position` builds the state from `startpos` or a FEN, then plays the listed
   moves.
2. On `go`, a brain named on the command line (`random`, `greedy`, `negamax`) answers
   at once. The default `think` brain plays a book move (Day 10) if there is one.
3. Otherwise `thinking_time` turns the clocks into seconds, and `search_and_send`
   runs `think` in a thread, so Remus can still answer `isready` and obey `stop`.
4. `bestmove 0000` goes out only when there is no legal move.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `send` | 7 | Send one line to the GUI. flush=True makes it leave at once. |
| `set_position` | 7 | Build the state that a "position" command describes. |
| `thinking_time` | 9 | Decide how many seconds to think from a "go" command. |
| `search_and_send` | 9 | Think in the background, then send the best move to the GUI. |

## Try it

From inside a Day folder in `instructor/` that has the file:

```bash
uv run uci_engine.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 1.1, 7.6, 9.7.
