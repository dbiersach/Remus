# Day 4: Legal moves

Day 4 teaches modules and git, then the rule that makes a move legal: the mover's own king must be safe after it. By 4:30 Remus finds attacks and check, and keeps only the legal moves, so a pinned knight has no moves and a king in check has only escapes.

## Objectives for the day

By 4:30, each pair can:

- Import functions from another file, and explain why every Remus file keeps its prints inside `main()`.
- Save work with git: fetch, switch to a new branch, commit, and read the log.
- Decide whether a square is attacked by looking outward from the square.
- Keep only legal moves: make each move, test the king, and undo it.
- Predict the legal moves of a position, then check the prediction with Remus.

## The day at a glance

| Period | Time | Title | Pairs write |
| --- | --- | --- | --- |
| P1 | 8:30 to 10:00 | Python lab 6: modules, imports, __main__, git | The lab `python_modules.py` (11 lines) |
| | 10:00 to 10:30 | Break | |
| P2 | 10:30 to 12:00 | Attacks | `piece_at_offsets()` in `attacks.py` (6 lines); `attacked_by_pawn()` in `attacks.py` (3 lines); `attacked_by_king()` in `attacks.py` (2 lines) |
| | 12:00 to 1:00 | Lunch | |
| P3 | 1:00 to 2:30 | Check and the legal filter | `in_check()` in `attacks.py` (2 lines); `legal_moves()` in `legal_moves.py` (8 lines) |
| | 2:30 to 3:00 | Break | |
| P4 | 3:00 to 4:30 | Practice positions | The demo `demo_practice_positions.py` (14 lines) |

## Period 1, 8:30 to 10:00: Python lab 6: modules, imports, __main__, git

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Slides: a module is a file, `import` reads it, and `if __name__ == "__main__"` keeps a file quiet when another file imports it. |
| 8:45 to 9:20 | Pairs work through Parts #1 to #3 of `python_modules.py`: every file has a `__name__`, use yesterday's `board.py` and `move_generation.py`, and list the knight moves from g1. |
| 9:20 to 9:30 | Slides: git. The teacher shows `fetch`, `switch -c`, `commit`, and `log` on the projector. |
| 9:30 to 9:50 | Pairs finish Part #4 and save the lab with their first commit. |
| 9:50 to 10:00 | Every pair shows its `git log` to the teacher or the assistant. |

[`period1/README.md`](period1/README.md) lists the period's learning objectives, how each one is measured, and every change the pairs make.

## Period 2, 10:30 to 12:00: Attacks

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Chess refresher on the demonstration board: check, pins, and discovered check. |
| 10:45 to 11:00 | Slides: a square is attacked if a piece could capture there. Stand on the square and look outward like a "super piece". The teacher writes `attacked_by_knight()` and the sliding-line part. |
| 11:00 to 11:40 | Pairs write `piece_at_offsets()`, then `attacked_by_pawn()` and `attacked_by_king()` on top of it. |
| 11:40 to 11:50 | Pairs run the attack tests and the file's self-check. |
| 11:50 to 12:00 | Show and choose for `piece_at_offsets()`. |

[`period2/README.md`](period2/README.md) lists the period's learning objectives, how each one is measured, and every change the pairs make.

## Period 3, 1:00 to 2:30: Check and the legal filter

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | Unplugged warm-up, "Pin hunt": on four printed positions, pairs cross out every move that leaves the mover's king attacked. |
| 1:15 to 1:25 | Slides: a move is legal only if the mover's king is safe after the move. Make it, test the king, undo it. |
| 1:25 to 2:05 | Pairs write `in_check()` and `legal_moves()` until the tests pass. |
| 2:05 to 2:15 | Pairs compare Remus's answers with their pin hunt worksheets. |
| 2:15 to 2:30 | Show and choose for `legal_moves()`. |

[`period3/README.md`](period3/README.md) lists the period's learning objectives, how each one is measured, and every change the pairs make.

## Period 4, 3:00 to 4:30: Practice positions

| Time | Activity |
| --- | --- |
| 3:00 to 3:10 | Slides: the workshop's first three verification positions: the start, a king in check, and a pinned knight. |
| 3:10 to 3:50 | In `demo_practice_positions.py` pairs type each position and write their prediction of its legal move count before Remus counts. |
| 3:50 to 4:15 | Part #4: each pair builds a position of its own and trades it with the next pair, who predict before they run it. |
| 4:15 to 4:30 | Checkpoint: a pinned knight has zero legal moves, and a king in check has only escapes. |

[`period4/README.md`](period4/README.md) lists the period's learning objectives, how each one is measured, and every change the pairs make.

## By the end of the day

**Checkpoint:** A pinned knight has zero legal moves, a king in check has only escapes, and `test_legal_moves.py` passes.

Each period folder starts from working code, so a pair that falls behind opens the next period's folder with the rest of the class.
