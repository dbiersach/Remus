# Day 5: Special moves

Day 5 adds the rare rules: castling, en passant, the double step, and promotion and underpromotion, each with an exact undo. It closes the first week with a payoff: by 4:30 every student pair plays its own Remus in Lucas Chess, where Remus answers with random legal moves.

## Objectives for the day

By 4:30, each student pair can:

- Use a set, `in`, a dict lookup, and `replace()` on the castling rights string `"KQkq"`.
- State the five conditions for castling, and say which moves take away each castling right.
- Explain why the pawn an en passant capture removes is not on the square the capturing pawn lands on.
- Show that a knight promotion can win where a queen promotion stalemates.
- Register Remus in Lucas Chess and play a game against it.

## The day at a glance

| Period | Time | Title | Student pairs write |
| --- | --- | --- | --- |
| P1 | 8:30 to 10:00 | Python lab 7: sets, in, string replacement | The lab `python_sets.py` (14 lines) |
| | 10:00 to 10:30 | Break | |
| P2 | 10:30 to 12:00 | Castling | `update_castling_rights()` in `make_move.py` (4 lines) |
| | 12:00 to 1:00 | Lunch | |
| P3 | 1:00 to 2:30 | En passant and the double step | `en_passant_victim_square()` in `make_move.py` (1 line) |
| | 2:30 to 3:00 | Break | |
| P4 | 3:00 to 4:30 | Promotion, and Remus plays in Lucas Chess | The demo `demo_promotion.py` (12 lines) |

## Period 1, 8:30 to 10:00: Python lab 7: sets, in, string replacement

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Slides: a set holds each item once, `in` asks a yes-or-no question, and a dict looks up a value by its key. |
| 8:45 to 9:35 | Student pairs work through the four parts of `python_sets.py`, ending with `replace()` removing "K" from "KQkq" when the h1 rook moves. |
| 9:35 to 9:50 | The class lists, on the board, every move that removes a castling right. |
| 9:50 to 10:00 | Wrap-up and a preview of castling. |

[`Day 05 Period 01 Goals.md`](<period1/Day 05 Period 01 Goals.md>) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 2, 10:30 to 12:00: Castling

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Chess refresher on the demonstration board: the five castling conditions. The rook may cross an attacked square (b1), and a rook captured on its home square removes that right. |
| 10:45 to 11:00 | Slides: the teacher's castling generation and the attacked-square checks. |
| 11:00 to 11:20 | Student pairs write `update_castling_rights()`, the table of which moves remove K, Q, k, or q. |
| 11:20 to 11:50 | Student pairs run the castling tests and build one castling position of their own to test. |
| 11:50 to 12:00 | Show and choose for `update_castling_rights()`. |

[`Day 05 Period 02 Goals.md`](<period2/Day 05 Period 02 Goals.md>) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 3, 1:00 to 2:30: En passant and the double step

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | Chess refresher: en passant is allowed only on the very next move after a two-square push, and the captured pawn is not on the destination square. |
| 1:15 to 1:30 | Slides: the double step sets the en passant target. The teacher walks through the en passant make and undo. |
| 1:30 to 1:55 | Student pairs write `en_passant_victim_square()`, then trace a capture and its undo on the printed board. |
| 1:55 to 2:20 | Student pairs run the en passant tests, including the rare capture that exposes the king along the rank. |
| 2:20 to 2:30 | Wrap-up: which square does the undo put the captured pawn back on? |

[`Day 05 Period 03 Goals.md`](<period3/Day 05 Period 03 Goals.md>) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 4, 3:00 to 4:30: Promotion, and Remus plays in Lucas Chess

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Puzzle on the demonstration board: promoting to a knight wins, and promoting to a queen stalemates. The teacher shows promotion in `make_move()` and `undo_move()`. |
| 3:15 to 3:45 | In `demo_promotion.py` student pairs write the loop that tries all four promotions and prints stalemate or checkmate for each. |
| 3:45 to 4:00 | The teacher hands out `uci_engine.py` and `remus.bat`. Student pairs register `remus.bat` from the period's `student` folder in Lucas Chess, following the [Lucas Chess guide](../misc/docs/course/lucas_chess_guide.md). |
| 4:00 to 4:25 | Student pairs play their own Remus, which answers with random legal moves. Every special move works on a real board. |
| 4:25 to 4:30 | Checkpoint: every special-move test passes. |

[`Day 05 Period 04 Goals.md`](<period4/Day 05 Period 04 Goals.md>) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## By the end of the day

**Checkpoint:** Every special-move test passes, every special move undoes exactly, and Remus plays random legal moves in Lucas Chess.

Each period folder starts from working code, so a student pair that falls behind opens the next period's folder with the rest of the class.
