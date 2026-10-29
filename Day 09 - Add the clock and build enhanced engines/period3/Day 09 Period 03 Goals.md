# Day 9, Period 3: Engine enhancements: test and measure

## Learning objectives

By the end of this period, each student pair can:

- Test an enhancement before trusting it. **Measured by:** The enhanced engine passes `run_tests.py` and a one-game smoke test against Remus-WHITE with no illegal moves.
- Predict what the enhancement changes. **Measured by:** Each student pair writes one sentence on the board: what should change, and how the class will see it in the match results.

## The files

This folder holds no engine code. Your student pair works in one folder only: your own engine folder in `engines/student`, such as `10 RED - Transposition table`. That folder already holds the whole Remus engine you finished in period 1, so you add only your one enhancement there. Do not change `00 WHITE - No enhancements`: it is plain Remus with no enhancement, and it stays as it is so the class can measure every enhancement against it. The `README.md` in each engine folder explains its enhancement, and its section "The code you type" shows every line the student pair types, with line numbers, the lines around it, and how the code works.

Before the smoke test, check your engine: open `run_tests.py` in your student pair's engine folder in `engines/student` and press Run. Every test must pass. Click your engine folder below to find it.

| Engine folder | The code you type | Tests |
| --- | --- | --- |
| [01 GRAY - King safety](../../engines/student/01%20GRAY%20-%20King%20safety) | [`README.md`](../../engines/student/01%20GRAY%20-%20King%20safety/README.md) | [`run_tests.py`](../../engines/student/01%20GRAY%20-%20King%20safety/run_tests.py) |
| [02 YELLOW - Draw sense](../../engines/student/02%20YELLOW%20-%20Draw%20sense) | [`README.md`](../../engines/student/02%20YELLOW%20-%20Draw%20sense/README.md) | [`run_tests.py`](../../engines/student/02%20YELLOW%20-%20Draw%20sense/run_tests.py) |
| [03 CYAN - Mating bonus](../../engines/student/03%20CYAN%20-%20Mating%20bonus) | [`README.md`](../../engines/student/03%20CYAN%20-%20Mating%20bonus/README.md) | [`run_tests.py`](../../engines/student/03%20CYAN%20-%20Mating%20bonus/run_tests.py) |
| [04 PINK - Principal variation search](../../engines/student/04%20PINK%20-%20Principal%20variation%20search) | [`README.md`](../../engines/student/04%20PINK%20-%20Principal%20variation%20search/README.md) | [`run_tests.py`](../../engines/student/04%20PINK%20-%20Principal%20variation%20search/run_tests.py) |
| [05 ORANGE - Null-move pruning](../../engines/student/05%20ORANGE%20-%20Null-move%20pruning) | [`README.md`](../../engines/student/05%20ORANGE%20-%20Null-move%20pruning/README.md) | [`run_tests.py`](../../engines/student/05%20ORANGE%20-%20Null-move%20pruning/run_tests.py) |
| [06 BROWN - Late move reductions](../../engines/student/06%20BROWN%20-%20Late%20move%20reductions) | [`README.md`](../../engines/student/06%20BROWN%20-%20Late%20move%20reductions/README.md) | [`run_tests.py`](../../engines/student/06%20BROWN%20-%20Late%20move%20reductions/run_tests.py) |
| [07 PURPLE - Pawn structure](../../engines/student/07%20PURPLE%20-%20Pawn%20structure) | [`README.md`](../../engines/student/07%20PURPLE%20-%20Pawn%20structure/README.md) | [`run_tests.py`](../../engines/student/07%20PURPLE%20-%20Pawn%20structure/run_tests.py) |
| [08 GREEN - Opening book](../../engines/student/08%20GREEN%20-%20Opening%20book) | [`README.md`](../../engines/student/08%20GREEN%20-%20Opening%20book/README.md) | [`run_tests.py`](../../engines/student/08%20GREEN%20-%20Opening%20book/run_tests.py) |
| [09 BLUE - Killer moves](../../engines/student/09%20BLUE%20-%20Killer%20moves) | [`README.md`](../../engines/student/09%20BLUE%20-%20Killer%20moves/README.md) | [`run_tests.py`](../../engines/student/09%20BLUE%20-%20Killer%20moves/run_tests.py) |
| [10 RED - Transposition table](../../engines/student/10%20RED%20-%20Transposition%20table) | [`README.md`](../../engines/student/10%20RED%20-%20Transposition%20table/README.md) | [`run_tests.py`](../../engines/student/10%20RED%20-%20Transposition%20table/run_tests.py) |

## The period step by step

| Time | Activity |
| --- | --- |
| 1:00 to 1:40 | Student pairs finish their engine enhancement, then open `run_tests.py` in their engine folder in `engines/student` and press Run until every test passes. The table above links each engine folder. |
| 1:40 to 2:10 | Each student pair opens `smoke_test.py` in its engine folder and presses Run in VS Code: one 2-minute game against Remus-WHITE, which checks only that the engine plays legal moves to the end. |
| 2:10 to 2:30 | Each student pair writes one sentence on the board: what its enhancement should change, and how the class will see it. |
