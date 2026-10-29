# Day 8: Searching ahead, then smarter

Day 8 teaches Remus to look ahead. It starts with minimax, folds it into negamax, prunes it with alpha-beta, keeps capturing past the horizon with quiescence, and tries the best captures first. By 4:30 Remus finds every mate in 1 and every puzzle mate in 2.

## Objectives for the day

By 4:30, each pair can:

- Back up scores through a game tree by hand, the way minimax does.
- Write negamax: one function that flips the sign of each reply's score and prefers the faster mate.
- Explain an alpha-beta cutoff, and show that alpha-beta gives the same score with fewer nodes.
- Explain the horizon effect, and stop it with a quiescence search that may stand pat.
- Order captures by most valuable victim, least valuable attacker, and measure the nodes it saves.

## The day at a glance

| Period | Time | Title | Pairs write |
| --- | --- | --- | --- |
| P1 | 8:30 to 10:00 | Minimax, negamax, and mates | `negamax()` in `search.py` (17 lines) |
| | 10:00 to 10:30 | Break | |
| P2 | 10:30 to 12:00 | Python lab 11 and alpha-beta | `alpha_beta()` in `search.py` (16 lines); the lab `python_sorting.py` (19 lines) |
| | 12:00 to 1:00 | Lunch | |
| P3 | 1:00 to 2:30 | The horizon effect and quiescence | `quiescence()` in `search.py` (15 lines) |
| | 2:30 to 3:00 | Break | |
| P4 | 3:00 to 4:30 | Move ordering | `mvv_lva_score()` in `move_ordering.py` (8 lines) |

## Period 1, 8:30 to 10:00: Minimax, negamax, and mates

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Unplugged warm-up, "Paper minimax": pairs back up max and min on a printed two-ply tree and circle the best move. A seven-student human tree can act it out at the front of the room. |
| 8:45 to 9:00 | The teacher writes `minimax()` to depth 2 with a node counter, and pairs compare its answer with their worksheets. |
| 9:00 to 9:10 | Slides: negamax, the same search in one function: flip the sign, wrap make and undo in `try/finally`, and score checkmate as `-(MATE_SCORE - ply)`. |
| 9:10 to 9:50 | Pairs write `negamax()` until the tests show it agrees with minimax and leaves the root state unchanged. |
| 9:50 to 10:00 | Show and choose for `negamax()`. |

[`Day 08 Period 01 Goals.md`](<period1/Day 08 Period 01 Goals.md>) lists the period's learning objectives, how each one is measured, every change the pairs make, and their exact tasks.

## Period 2, 10:30 to 12:00: Python lab 11 and alpha-beta

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Unplugged warm-up, "Fewest flips": the same tree as face-down cards. Pairs turn a card only when the answer could still change. |
| 10:45 to 10:55 | Slides: alpha and beta, and the cutoff. |
| 10:55 to 11:25 | Pairs write `alpha_beta()` beside `negamax()` and run `compare_search.py`: the same score, fewer nodes. |
| 11:25 to 12:00 | Pairs work through `python_sorting.py`: `insert()` puts the biggest victim first, `float("inf")`, and timing a perft run. |

[`Day 08 Period 02 Goals.md`](<period2/Day 08 Period 02 Goals.md>) lists the period's learning objectives, how each one is measured, every change the pairs make, and their exact tasks.

## Period 3, 1:00 to 2:30: The horizon effect and quiescence

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | Puzzle: at depth 2 Remus takes a defended pawn with its queen. Why? The class names the horizon effect. |
| 1:15 to 1:30 | Slides: quiescence keeps searching captures until the position is quiet. The teacher writes `capture_moves()`. |
| 1:30 to 2:10 | Pairs write `quiescence()`, which may stand pat with the evaluation or try a capture that does better. |
| 2:10 to 2:20 | Pairs run the puzzle again: Remus keeps its queen. |
| 2:20 to 2:30 | Show and choose for `quiescence()`. |

[`Day 08 Period 03 Goals.md`](<period3/Day 08 Period 03 Goals.md>) lists the period's learning objectives, how each one is measured, every change the pairs make, and their exact tasks.

## Period 4, 3:00 to 4:30: Move ordering

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Slides: alpha-beta cuts more when the best move comes first. Most valuable victim, least valuable attacker (MVV-LVA). |
| 3:15 to 3:40 | Pairs write `mvv_lva_score()`. The teacher writes `order_moves()` and the check extension. |
| 3:40 to 4:05 | Pairs measure node counts before and after ordering with `compare_search.py`. |
| 4:05 to 4:20 | Pairs run the mate puzzles. |
| 4:20 to 4:30 | Checkpoint: every mate in 1 and every puzzle mate in 2. |

[`Day 08 Period 04 Goals.md`](<period4/Day 08 Period 04 Goals.md>) lists the period's learning objectives, how each one is measured, every change the pairs make, and their exact tasks.

## By the end of the day

**Checkpoint:** Remus finds every mate in 1 and every puzzle mate in 2, and alpha-beta returns the same score as negamax with fewer nodes.

Each period folder starts from working code, so a pair that falls behind opens the next period's folder with the rest of the class.
