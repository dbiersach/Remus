# Day 9: The clock and the enhanced engines

Day 9 gives Remus a clock, then splits the class into ten enhancement enhanced engines. Each student pair adds one idea to the same engine, Remus-WHITE, and tests it. In period 4 the student pairs carry their enhanced engines to each other's laptops on USB sticks and battle. By 4:30 every enhanced engine passes its tests and has played two battles.

## Objectives for the day

By 4:30, each student pair can:

- Search deeper one step at a time and keep the best move of the deepest search that finished before time ran out.
- Read the `info` lines Remus sends to Lucas Chess: depth, score, nodes, and the principal variation.
- Use a dict as a cache with a tuple as its key.
- Add one enhancement to Remus-WHITE, test it, and say what it should change in a game.
- Play two enhanced engines against each other, and read the result with its uncertainty.

## The day at a glance

| Period | Time | Title | Student pairs write |
| --- | --- | --- | --- |
| P1 | 8:30 to 10:00 | Iterative deepening, the clock, and UCI info | `think()` in `search.py` (17 lines) |
| | 10:00 to 10:30 | Break | |
| P2 | 10:30 to 12:00 | Python lab 12 and the engine enhancements | The lab `python_caches.py` (7 lines); their enhanced engine's functions, from the version README |
| | 12:00 to 1:00 | Lunch | |
| P3 | 1:00 to 2:30 | Engine enhancements: test and measure | Their enhanced engine's functions, from the version README |
| | 2:30 to 3:00 | Break | |
| P4 | 3:00 to 4:30 | Engine battles | The demo `demo_results.py` (13 lines) |

## Period 1, 8:30 to 10:00: Iterative deepening, the clock, and UCI info

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Slides: the clock. The teacher reads `go movetime`, `wtime`, and `btime`, turns them into a thinking time, and writes `format_info()`. |
| 8:45 to 9:25 | Student pairs write `think()` (the iterative deepening loop): depth 1, then 2, then 3, keeping the best move of the deepest search that finished. |
| 9:25 to 9:35 | Show and choose for `think()`. The chosen code makes Remus-WHITE, the Remus with none of the enhancements and the starting point of every enhanced engine. |
| 9:35 to 10:00 | The class watches Remus-WHITE play a 5-minute game against Stockfish at 1500 Elo in Lucas Chess and reads the `info` lines as it thinks. |

[`Day 09 Period 01 Goals.md`](<period1/Day 09 Period 01 Goals.md>) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 2, 10:30 to 12:00: Python lab 12 and the engine enhancements

| Time | Activity |
| --- | --- |
| 10:30 to 10:50 | Student pairs work through `python_caches.py`: a dict remembers answers, `math.dist()`, and `random.seed()`. |
| 10:50 to 11:00 | Slides: the ten enhanced engines. Each one is the period 1 Remus with one enhancement added, such as RED (transposition table) or BLUE (killer moves). The folder names use colors so that no engine sounds better than another. |
| 11:00 to 12:00 | Each student pair opens its enhanced engine in `engines/student`, reads the version README, and writes the enhanced engine's stubbed code. |

[`Day 09 Period 02 Goals.md`](<period2/Day 09 Period 02 Goals.md>) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 3, 1:00 to 2:30: Engine enhancements: test and measure

| Time | Activity |
| --- | --- |
| 1:00 to 1:40 | Student pairs finish their engine enhancement, then open `run_tests.py` in their engine folder in `engines/student` and press Run until every test passes. The table above links each engine folder. |
| 1:40 to 2:10 | Each student pair opens `basic_test.py` in its engine folder and presses Run in VS Code: one 2-minute game against Remus-WHITE, which checks only that the engine plays legal moves to the end. |
| 2:10 to 2:30 | Each student pair writes one sentence on the board: what its enhancement should change, and how the class will see it. |

[`Day 09 Period 03 Goals.md`](<period3/Day 09 Period 03 Goals.md>) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## Period 4, 3:00 to 4:30: Engine battles

| Time | Activity |
| --- | --- |
| 3:00 to 3:10 | Slides: how a battle works. Each student pair copies its finished engine folder, such as `engines/student/10 Remus-RED - Transposition table`, onto its USB stick. The teacher posts the pairings for two rounds; in each round five student pairs host and five visit. |
| 3:10 to 3:40 | Round 1. The visiting student pair pastes its engine folder into the same path on the host laptop, `engines/student`, and replaces the folder of the same name. The host opens `play_battle.py` in its own engine folder, sets `VISITING_ENGINE` to the visitor's engine color, and presses Run in VS Code. Two 10-minute games run side by side, one with each piece color. Each student pair writes the score on the board. |
| 3:40 to 3:45 | Round 2: the student pairs that visited now host, against new opponents. |
| 3:45 to 4:10 | While the round 2 games run, each student pair turns its round 1 result into an Elo gap with a margin of error in `demo_results.py`, then tries its engine's league games. |
| 4:10 to 4:25 | The class reads the board: which engines won, and why two games prove little. The teacher shows the league table, 110 games for each engine, and compares. |
| 4:25 to 4:30 | Each visiting student pair takes its USB stick back. The visitor's folder stays on the host laptop in place of an engine the host student pair never writes, so the host's own engine folder is untouched. |

[`Day 09 Period 04 Goals.md`](<period4/Day 09 Period 04 Goals.md>) lists the period's learning objectives, how each one is measured, every change the student pairs make, and their exact tasks.

## By the end of the day

**Checkpoint:** Every enhanced engine passes its tests and its one-game test match, and has played two battles against other enhanced engines.

Each period folder starts from working code, so a student pair that falls behind opens the next period's folder with the rest of the class.
