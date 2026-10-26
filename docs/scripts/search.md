# search.py

Chooses a move, from a random brain up to the final Day 10 search.

First appears in `instructor/Day 07 - Play full games in En Croissant`. Grows on Day 8, Day 9, Day 10.

## What it does

`search.py` grows more than any other file. Every day adds a smarter search next to
the earlier ones, so students can compare node counts and scores on the same position.

| Day | Function | Idea |
| --- | --- | --- |
| 7 | `random_move`, `greedy_move` | Any legal move; the biggest capture |
| 8 | `minimax` | White maximizes, Black minimizes, two mirror-image halves |
| 8 | `negamax`, `best_move` | One function: my score is minus my opponent's best |
| 9 | `alpha_beta` | Skips moves that cannot change the result; same score, far fewer positions |
| 9 | `quiescence` | Keeps searching captures at the leaves until the position is quiet |
| 9 | `alpha_beta_with_quiescence` | Alpha-beta, quiescence, MVV-LVA ordering, a check extension, and the principal variation |
| 9 | `think` | Iterative deepening on a clock, stopping with `SearchTimeout` |
| 10 | `upgraded_search` | Adds the transposition table, killer moves, principal variation search, and draw sense |

## Data structures

`SearchInfo` collects what one search counts and needs: `nodes`, the `deadline`, the
GUI's `stop` event, and on Day 10 the transposition `table` and the `killers`.
`MATE_SCORE` is 100,000; a mate found `ply` moves from the root scores
`MATE_SCORE - ply`, so a quicker mate scores higher.

## Program flow of `think`

1. Order the root moves so there is always a move to return.
2. For depth 1, 2, 3, and on: run the search with the widest window.
3. If `check_time` raises `SearchTimeout`, keep the last finished depth's move. The
   `try/finally` around every `make_move` undoes each move on the way out.
4. After each depth, report an `info` line and stop early on a forced mate or a single
   legal move.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `SearchInfo` | 8 | What a search counts while it runs. |
| `SearchTimeout` | 9 | Raised inside the search when time is up, to unwind back to the root. |
| `check_time` | 9 | Raise SearchTimeout if the deadline has passed or the GUI said stop. |
| `random_move` | 7 | Return a random legal move. |
| `capture_value` | 7 | Return the value of the piece a move captures, or 0 for a quiet move. |
| `greedy_move` | 7 | Return the move that captures the most valuable piece. |
| `white_score` | 8 | Return the evaluation from White's side, as minimax uses it. |
| `minimax` | 8 | Score a position by looking `depth` moves ahead. White picks the highest score, Black the lowest. |
| `negamax` | 8 | Score a position by looking `depth` moves ahead, from the side to move. |
| `best_move` | 8 | Search every root move with negamax and return the best one. |
| `negamax_move` | 8 | Return the negamax move at depth 2, the brain the UCI engine uses. |
| `alpha_beta` | 9 | Negamax with alpha-beta pruning: the same score, far fewer positions. |
| `capture_moves` | 9 | Return the legal moves that capture a piece or promote a pawn. |
| `quiescence` | 9 | Keep searching captures until the position is quiet, then evaluate it. |
| `alpha_beta_with_quiescence` | 9 | The full Day 9 search: alpha-beta with quiescence at the leaves, ordered moves, a check extension, a clock, and the line of best play. |
| `remember_killer` | 10 | Keep a quiet move that caused a cutoff as one of two killers for this ply. |
| `upgraded_search` | 10 | The final Day 10 search: alpha_beta_with_quiescence plus the upgrade stations. |
| `format_info` | 9 | Return a UCI "info" line so the GUI can show what Remus is thinking. |
| `think` | 9 | Search one move deeper at a time until time runs out, and return the best move. |
| `think_move` | 9 | Return the iterative-deepening move with two seconds to think. |

## Try it

From inside a Day folder in `instructor/` that has the file:

```bash
uv run search.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 7.7, 8.3, 8.4, 8.5, 9.1, 9.3, 9.5, 9.6, 9.8, 10.4, 10.5.
