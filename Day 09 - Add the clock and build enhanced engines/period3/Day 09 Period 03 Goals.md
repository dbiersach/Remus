# Day 9, Period 3: Color versions: test and measure

## Learning objectives

By the end of this period, each student pair can:

- Test an enhancement before trusting it. **Measured by:** The color version passes `run_tests.py` and a one-game smoke test against Remus-WHITE with no illegal moves.
- Predict what the enhancement changes. **Measured by:** Each student pair writes one sentence on the board: what should change, and how the class will see it in the match results.

## The files

This folder holds no engine code. Each student pair works in its own engine folder in `period2/student/engines`, a complete copy of Remus-WHITE plus one enhancement. Remus-WHITE itself is in the `period1` folder.

Before the smoke test, check your engine: open `run_tests.py` in your student pair's engine folder from period 2 and press Run. Every test must pass. Click your engine folder below to find it.

| Engine folder | Tests |
| --- | --- |
| [01 GRAY - King safety](../period2/student/engines/01%20GRAY%20-%20King%20safety) | [`run_tests.py`](../period2/student/engines/01%20GRAY%20-%20King%20safety/run_tests.py) |
| [02 YELLOW - Draw sense](../period2/student/engines/02%20YELLOW%20-%20Draw%20sense) | [`run_tests.py`](../period2/student/engines/02%20YELLOW%20-%20Draw%20sense/run_tests.py) |
| [03 CYAN - Mating bonus](../period2/student/engines/03%20CYAN%20-%20Mating%20bonus) | [`run_tests.py`](../period2/student/engines/03%20CYAN%20-%20Mating%20bonus/run_tests.py) |
| [04 PINK - Principal variation search](../period2/student/engines/04%20PINK%20-%20Principal%20variation%20search) | [`run_tests.py`](../period2/student/engines/04%20PINK%20-%20Principal%20variation%20search/run_tests.py) |
| [05 ORANGE - Null-move pruning](../period2/student/engines/05%20ORANGE%20-%20Null-move%20pruning) | [`run_tests.py`](../period2/student/engines/05%20ORANGE%20-%20Null-move%20pruning/run_tests.py) |
| [06 BROWN - Late move reductions](../period2/student/engines/06%20BROWN%20-%20Late%20move%20reductions) | [`run_tests.py`](../period2/student/engines/06%20BROWN%20-%20Late%20move%20reductions/run_tests.py) |
| [07 PURPLE - Pawn structure](../period2/student/engines/07%20PURPLE%20-%20Pawn%20structure) | [`run_tests.py`](../period2/student/engines/07%20PURPLE%20-%20Pawn%20structure/run_tests.py) |
| [08 GREEN - Opening book](../period2/student/engines/08%20GREEN%20-%20Opening%20book) | [`run_tests.py`](../period2/student/engines/08%20GREEN%20-%20Opening%20book/run_tests.py) |
| [09 BLUE - Killer moves](../period2/student/engines/09%20BLUE%20-%20Killer%20moves) | [`run_tests.py`](../period2/student/engines/09%20BLUE%20-%20Killer%20moves/run_tests.py) |
| [10 RED - Transposition table](../period2/student/engines/10%20RED%20-%20Transposition%20table) | [`run_tests.py`](../period2/student/engines/10%20RED%20-%20Transposition%20table/run_tests.py) |

## The period step by step

| Time | Activity |
| --- | --- |
| 1:00 to 1:40 | Student pairs finish their color version code, then open `run_tests.py` in their engine folder in `period2/student/engines` and press Run until every test passes. The table above links each engine folder. |
| 1:40 to 2:10 | Each student pair opens `smoke_test.py` in its engine folder and presses Run in VS Code: one 2-minute game against Remus-WHITE, which checks only that the engine plays legal moves to the end. |
| 2:10 to 2:30 | Each student pair writes one sentence on the board: what its enhancement should change, and how the class will see it. |
