# Day 2: Remus2 searches and plays Stockfish

**Goal for the day:** the student pair turns Remus1 into Remus2, and Remus2 plays Stockfish 1500 in Lucas Chess.

## The day at a glance

| Period | Time | Title |
| --- | --- | --- |
| P1 | 8:30 to 10:00 | [The evaluation](period1/Day_2_Period_1_Syllabus.md) |
| | 10:00 to 10:30 | Break |
| P2 | 10:30 to 12:00 | [Move ordering and quiescence](period2/Day_2_Period_2_Syllabus.md) |
| | 12:00 to 1:00 | Lunch |
| P3 | 1:00 to 2:30 | [Alpha-beta and iterative deepening](period3/Day_2_Period_3_Syllabus.md) |
| | 2:30 to 3:00 | Break |
| P4 | 3:00 to 4:30 | [Remus2 against Stockfish 1500](period4/Day_2_Period_4_Syllabus.md) |

## Period 1, 8:30 to 10:00: The evaluation

| Time | Activity |
| --- | --- |
| 8:30 to 8:35 | In File Explorer, copy every file of `engines/Remus1` into `engines/Remus2`. The rest of Day 2 edits those copies. |
| 8:35 to 8:45 | A score in centipawns: material, plus a bonus or penalty for where each piece stands. A Black piece reads each table upside down. |
| 8:45 to 9:55 | Type `evaluation.py` (68 code lines): `mirrored_table()`, the four piece-square tables (files a to d only), the piece values, and `evaluate()`. Run it. |
| 9:55 to 10:00 | Swap driver and navigator. |

[`Day_2_Period_1_Syllabus.md`](period1/Day_2_Period_1_Syllabus.md) has the period's goal, the big picture of what the student pair types or edits and why, every file that changes with its line numbers, and how the student pair knows it is done.

## Period 2, 10:30 to 12:00: Move ordering and quiescence

| Time | Activity |
| --- | --- |
| 10:30 to 10:50 | Alpha-beta on paper: look ahead, assume both sides play their best, and skip the moves that cannot change the result. MVV-LVA: try pawn takes queen before queen takes pawn. |
| 10:50 to 11:55 | In `engines/Remus2`, keep the three import lines of Remus1's `search.py`, change `import random` to `import time`, delete Remus1's random-move `think()`, and type the rest of the top of Remus2's `search.py` (about 50 code lines): the imports and constants, `ordered_moves()`, `count_node()`, and `quiescence()`. |
| 11:55 to 12:00 | Swap driver and navigator. |

[`Day_2_Period_2_Syllabus.md`](period2/Day_2_Period_2_Syllabus.md) has the period's goal, the big picture of what the student pair types or edits and why, every file that changes with its line numbers, and how the student pair knows it is done.

## Period 3, 1:00 to 2:30: Alpha-beta and iterative deepening

| Time | Activity |
| --- | --- |
| 1:00 to 1:10 | Reminder of checkmate and stalemate: a side with no legal move has lost if in check, and draws if not. |
| 1:10 to 2:10 | Type `alpha_beta()` and `think()` (about 43 code lines), which finish `search.py`. Change the name line in `uci.py` to `id name Remus2`. |
| 2:10 to 2:30 | Run `uci.py` and send `position startpos` and `go movetime 2000`: the `info` lines show Remus2 searching one move deeper at a time. Then run `check_my_remus.py` in `engines/Remus2` and fix any file it names until Remus2 passes every check. |

[`Day_2_Period_3_Syllabus.md`](period3/Day_2_Period_3_Syllabus.md) has the period's goal, the big picture of what the student pair types or edits and why, every file that changes with its line numbers, and how the student pair knows it is done.

## Period 4, 3:00 to 4:30: Remus2 against Stockfish 1500

| Time | Activity |
| --- | --- |
| 3:00 to 3:25 | Add `engines\Remus2\remus.bat` to Lucas Chess as "My Remus2" and start it against Stockfish 1500, one round of two 5-minute games (Part 3 of the guide), and watch the first game. |
| 3:25 to 4:05 | While the second game runs, each student plays one game against the instructor's Remus2 on the main board (Part 4). |
| 4:05 to 4:30 | Each student pair reads its results tab, then plays My Remus2 against My Remus1 for a few minutes to see what the search buys. |

[`Day_2_Period_4_Syllabus.md`](period4/Day_2_Period_4_Syllabus.md) has the period's goal, the big picture of what the student pair types or edits and why, every file that changes with its line numbers, and how the student pair knows it is done.

## By the end of the day

**Checkpoint:** Remus2 is complete, 342 code lines, and it plays two full games against Stockfish 1500.
