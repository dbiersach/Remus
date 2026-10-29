# Day 6: Counting the tree, and FEN

Day 6 teaches recursion and uses it to count every position the rules allow, a check called perft. Matching the counts of trusted chess programs proves the rules are right. By 4:30 perft matches the reference counts and Remus reads and writes positions as FEN text.

## Objectives for the day

By 4:30, each student pair can:

- Write a recursive function with a base case and a recursive case.
- Count the positions of the move tree to a fixed depth with `perft()`: 20, 400, and 8,902 from the start.
- Find a broken rule by comparing counts under each root move with python-chess.
- Read a FEN string with `split()` and `int()`, and catch a bad field with `try` and `ValueError`.
- Turn a board into the placement part of FEN and back.

## The day at a glance

| Period | Time | Title | Student pairs write |
| --- | --- | --- | --- |
| P1 | 8:30 to 10:00 | Python lab 8: recursion | The lab `python_recursion.py` (11 lines) |
| | 10:00 to 10:30 | Break | |
| P2 | 10:30 to 12:00 | Perft | `perft()` in `perft.py` (8 lines) |
| | 12:00 to 1:00 | Lunch | |
| P3 | 1:00 to 2:30 | Perft against python-chess, and bug hunt | The fixes for the planted bugs in `bug_hunt/` (3 lines) |
| | 2:30 to 3:00 | Break | |
| P4 | 3:00 to 4:30 | Python lab 9 and FEN | `fen_placement()` in `fen.py` (18 lines); `board_from_placement()` in `fen.py` (14 lines); the lab `python_fen_fields.py` (8 lines) |

## Period 1, 8:30 to 10:00: Python lab 8: recursion

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Slides: a function that calls itself, its base case, and the call stack. |
| 8:45 to 9:35 | Student pairs work through the three parts of `python_recursion.py`: count down, count the leaves of a small tree, and count the paths of a knight. |
| 9:35 to 9:50 | The teacher draws the call stack of a short count on the whiteboard while the class traces it. |
| 9:50 to 10:00 | Wrap-up: what stops a recursion? |

[`Day 06 Period 01 Goals.md`](<period1/Day 06 Period 01 Goals.md>) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 2, 10:30 to 12:00: Perft

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Unplugged warm-up, "Count by hand": in a king and pawn against king position, student pairs list every move two plies deep on index cards and count the leaves. |
| 10:45 to 10:55 | Slides: perft counts the leaves of the legal move tree. |
| 10:55 to 11:25 | Student pairs write `perft()` and run it on the warm-up position to check their cards. |
| 11:25 to 11:50 | Student pairs run `perft.py` from the start: 20, 400, and 8,902. The teacher shows `divide()`, which prints the count under each root move. |
| 11:50 to 12:00 | Show and choose for `perft()`. |

[`Day 06 Period 02 Goals.md`](<period2/Day 06 Period 02 Goals.md>) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 3, 1:00 to 2:30: Perft against python-chess, and bug hunt

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | Slides: `test_perft.py` compares Remus with python-chess on the standard positions. |
| 1:15 to 2:10 | Bug hunt: the `bug_hunt` folder holds a copy of Remus with three planted bugs. Student pairs run `hunt.py` there and race to find each bug from the root moves whose counts disagree. |
| 2:10 to 2:25 | Student pairs explain each bug they found and the rule it broke. |
| 2:25 to 2:30 | Wrap-up: the hunt is over when `hunt.py` prints 0 root moves that disagree. |

[`Day 06 Period 03 Goals.md`](<period3/Day 06 Period 03 Goals.md>) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 4, 3:00 to 4:30: Python lab 9 and FEN

| Time | Activity |
| --- | --- |
| 3:00 to 3:10 | Slides: the six fields of FEN, `split()`, `int()`, and `ValueError`. |
| 3:10 to 3:30 | Student pairs work through `python_fen_fields.py`. |
| 3:30 to 4:20 | Student pairs write `fen_placement()` and `board_from_placement()` in `fen.py`. The teacher writes the other five fields. |
| 4:20 to 4:30 | Checkpoint: every test position loads from FEN and perft matches the reference. |

[`Day 06 Period 04 Goals.md`](<period4/Day 06 Period 04 Goals.md>) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## By the end of the day

**Checkpoint:** Perft matches the reference at depth 3 for the start and the standard positions, and every test position loads from FEN. The rules are verified, so the search can begin.

Each period folder starts from working code, so a student pair that falls behind opens the next period's folder with the rest of the class.
