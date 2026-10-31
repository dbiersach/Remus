# Day 7: A whole game, and judging a position

Day 7 turns the rules into a whole game. Remus learns when a game ends, reads moves in standard notation, plays its first moves with a plan, and scores a position. By 4:30 a full game in Lucas Chess ends with the right result and reason. This is the "legal moves" milestone: from here on, the work is about good moves.

## Objectives for the day

By 4:30, each student pair can:

- Name every way a game ends: checkmate, stalemate, threefold repetition, the fifty-move rule, and insufficient material.
- Read a move a player types in SAN by matching it against the legal moves.
- Pick a random move, and pick the biggest capture with a loop that keeps the best so far.
- Explain how Remus and Lucas Chess talk over UCI.
- Score a position by its material in centipawns, and read the piece-square tables.

## The day at a glance

| Period | Time | Title | Student pairs write |
| --- | --- | --- | --- |
| P1 | 8:30 to 10:00 | Ending the game | `insufficient_material()` in `game_end.py` (18 lines); `game_result()` in `game_end.py` (12 lines) |
| | 10:00 to 10:30 | Break | |
| P2 | 10:30 to 12:00 | SAN: moves people read and type | `parse_san()` in `notation.py` (5 lines); the lab `python_input_output.py` (16 lines) |
| | 12:00 to 1:00 | Lunch | |
| P3 | 1:00 to 2:30 | First brains and the GUI | `random_move()` in `search.py` (1 line); `greedy_move()` in `search.py` (10 lines) |
| | 2:30 to 3:00 | Break | |
| P4 | 3:00 to 4:30 | What makes a position good? Material and piece-square tables | `material()` in `evaluation.py` (10 lines) |

## Period 1, 8:30 to 10:00: Ending the game

| Time | Activity |
| --- | --- |
| 8:30 to 8:50 | Chess refresher: stalemate, repetition, the fifty and 75-move rules, and insufficient material, with a six-position quiz. |
| 8:50 to 9:00 | Slides: the halfmove clock and `position_key()`, both in the given code. |
| 9:00 to 9:45 | Student pairs write `insufficient_material()` and `game_result()` in `game_end.py`. |
| 9:45 to 10:00 | Student pairs check their answers on the quiz positions, then show and choose. |

[`Day 07 Period 01 Goals.md`](<period1/Day 07 Period 01 Goals.md>) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 2, 10:30 to 12:00: SAN: moves people read and type

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Slides: SAN. The teacher walks through `move_to_san()`, including `Nbd2` and the `+` and `#` endings. |
| 10:45 to 11:05 | Student pairs write `parse_san()`: build the SAN of every legal move and return the one that matches. |
| 11:05 to 11:20 | Student pairs run `notation.py`, then change its position and check that `parse_san()` reads each SAN move it prints. |
| 11:20 to 12:00 | Student pairs work through `python_input_output.py`: `random.choice()`, a loop that keeps the best so far, stderr, and a tiny program that answers `isready` with `readyok`. |

[`Day 07 Period 02 Goals.md`](<period2/Day 07 Period 02 Goals.md>) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 3, 1:00 to 2:30: First brains and the GUI

| Time | Activity |
| --- | --- |
| 1:00 to 1:10 | Slides: a brain is a function that picks a move. Random picks any legal move, and greedy takes the most valuable capture. |
| 1:10 to 1:40 | Student pairs write `random_move()` and `greedy_move()`. |
| 1:40 to 2:00 | The class reads the Day 5 `uci_engine.py` line by line, then the given version in this folder, which adds FEN positions and a choice of brains. |
| 2:00 to 2:15 | Student pairs register `remus.bat` from the `student` folder in Lucas Chess again and play greedy Remus. |
| 2:15 to 2:30 | Student pairs run `play_match.py`: random Remus against greedy Remus for 20 games, with the score at the end. |

[`Day 07 Period 03 Goals.md`](<period3/Day 07 Period 03 Goals.md>) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 4, 3:00 to 4:30: What makes a position good? Material and piece-square tables

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Student pairs rank three printed positions and write one reason for each. The reasons become the evaluation terms. |
| 3:15 to 3:25 | Chess refresher: piece values (pawn 1, knight 3, bishop 3, rook 5, queen 9) and the fork, pin, and skewer. |
| 3:25 to 3:50 | Student pairs write `material()` in centipawns, scored for White. |
| 3:50 to 4:05 | The teacher shows the piece-square tables and `explain_evaluation()`, which prints every term. A knight on d4 attacks eight squares; on a1 it attacks two. |
| 4:05 to 4:25 | Each student pair proposes one change to one table, and the class votes. |
| 4:25 to 4:30 | Checkpoint: `explain_evaluation()` gives 0 for the start. |

[`Day 07 Period 04 Goals.md`](<period4/Day 07 Period 04 Goals.md>) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## By the end of the day

**Checkpoint:** A full game in Lucas Chess ends with the correct result and reason, and `explain_evaluation()` gives 0 for the start position.

Each period folder starts from working code, so a student pair that falls behind opens the next period's folder with the rest of the class.
