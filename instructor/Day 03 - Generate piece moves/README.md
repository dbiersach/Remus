# Day 3: Loops that walk the board

Day 3 teaches loops that walk across the board, then uses them to generate the moves of every piece. By 4:30 Remus finds the 20 moves of the start position, and `show_board.py` draws an arrow for every move the pairs' code finds.

## Objectives for the day

By 4:30, each pair can:

- Repeat steps with `while`, and stop early with `break`.
- Store a direction as a (row step, column step) tuple and walk it to the edge of the board or to the first piece.
- Generate knight and king moves from a list of jumps.
- Generate rook, bishop, and queen moves by sliding in each direction.
- Generate pawn pushes, including the double step from the start rank.

## The day at a glance

| Period | Time | Title | Pairs write |
| --- | --- | --- | --- |
| P1 | 8:30 to 10:00 | Python lab 5: while, break, direction tuples | The lab `python_loops.py` (14 lines) |
| | 10:00 to 10:30 | Break | |
| P2 | 10:30 to 12:00 | Jumping pieces: knights and kings | `king_moves()` in `move_generation.py` (1 line) |
| | 12:00 to 1:00 | Lunch | |
| P3 | 1:00 to 2:30 | Sliding pieces: rooks, bishops, and queens | `slide()` in `move_generation.py` (14 lines) |
| | 2:30 to 3:00 | Break | |
| P4 | 3:00 to 4:30 | Pawns | `pawn_pushes()` in `move_generation.py` (11 lines) |

## Period 1, 8:30 to 10:00: Python lab 5: while, break, direction tuples

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Slides: `while`, `break`, `continue`, and a list of direction tuples. |
| 8:45 to 9:35 | Pairs work through the four parts of `python_loops.py`: repeat with `while`, store a direction, walk from d4 until the edge or a piece, and try another direction. |
| 9:35 to 9:50 | The teacher runs the walk on the projector with a piece in the way and the class predicts where it stops. |
| 9:50 to 10:00 | Wrap-up: which loop stops at the edge, and which line stops it at a piece? |

[`period1/README.md`](period1/README.md) lists the period's learning objectives, how each one is measured, and every change the pairs make.

## Period 2, 10:30 to 12:00: Jumping pieces: knights and kings

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Unplugged warm-up, "Shade the reach": pairs shade every square a knight on d4, a knight on a1, and a bishop on c1 can reach, and compare counts with the next pair (8, 2, and 7). |
| 10:45 to 11:00 | Slides: an offset list for the knight. The teacher writes `knight_moves()` on the projector. |
| 11:00 to 11:20 | Pairs write `king_moves()` the same way and pass the jumping-piece tests: a knight on a1 has 2 moves and a king on a1 has 3. |
| 11:20 to 11:40 | Pairs run `show_board.py`, which draws an arrow for every move their generator returns, and count the arrows. |
| 11:40 to 12:00 | Pairs try their own squares, such as a king in a corner, and predict the arrows before they run the file. |

[`period2/README.md`](period2/README.md) lists the period's learning objectives, how each one is measured, and every change the pairs make.

## Period 3, 1:00 to 2:30: Sliding pieces: rooks, bishops, and queens

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | Slides: a sliding piece walks one direction until the edge or the first piece, and captures that piece only if it is an enemy. |
| 1:15 to 2:00 | Pairs write `slide()` in `move_generation.py`. The teacher's `slider_moves()` calls it with the rook, bishop, and queen directions. |
| 2:00 to 2:15 | Exercise: a rook on an empty board has 14 moves. Pairs check it with the tests and the arrow picture. |
| 2:15 to 2:30 | Show and choose for `slide()`. |

[`period3/README.md`](period3/README.md) lists the period's learning objectives, how each one is measured, and every change the pairs make.

## Period 4, 3:00 to 4:30: Pawns

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Slides: pawns move forward toward row 0 for White, push one or two squares, and capture diagonally. The teacher writes the captures and the four promotion choices. |
| 3:15 to 3:55 | Pairs write `pawn_pushes()`: the single step and the double step from the start rank. |
| 3:55 to 4:15 | Pairs run the tests and the arrow picture on the start position. |
| 4:15 to 4:30 | Checkpoint: `pseudo_legal_moves()` finds 20 moves from the start. |

[`period4/README.md`](period4/README.md) lists the period's learning objectives, how each one is measured, and every change the pairs make.

## By the end of the day

**Checkpoint:** `pseudo_legal_moves()` returns 20 moves from the start position.

Each period folder starts from working code, so a pair that falls behind opens the next period's folder with the rest of the class.
