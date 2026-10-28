# Day 9: The clock and the stations

Day 9 gives Remus a clock, then splits the class into ten enhancement stations. Each pair adds one idea to the same engine, Remus-WHITE, and tests it. By 4:30 every station passes its tests and plays a legal game, and the mate solver solves all ten puzzles.

## Objectives for the day

By 4:30, each pair can:

- Search deeper one step at a time and keep the best move of the deepest search that finished before time ran out.
- Read the `info` lines Remus sends to Lucas Chess: depth, score, nodes, and the principal variation.
- Use a dict as a cache with a tuple as its key.
- Add one enhancement to Remus-WHITE, test it, and say what it should change in a game.
- Solve a mate puzzle with a yes-or-no search.

## The day at a glance

| Period | Time | Title | Pairs write |
| --- | --- | --- | --- |
| P1 | 8:30 to 10:00 | Iterative deepening, the clock, and UCI info | `think()` in `search.py` (17 lines) |
| | 10:00 to 10:30 | Break | |
| P2 | 10:30 to 12:00 | Python lab 12 and the enhancement stations | The lab `python_caches.py` (7 lines); their color station's functions, from the station README |
| | 12:00 to 1:00 | Lunch | |
| P3 | 1:00 to 2:30 | Enhancement stations: test and measure | Their color station's functions, from the station README |
| | 2:30 to 3:00 | Break | |
| P4 | 3:00 to 4:30 | The mate solver | `mating_move()` in `mate_solver.py` (22 lines) |

## Period 1, 8:30 to 10:00: Iterative deepening, the clock, and UCI info

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Slides: the clock. The teacher reads `go movetime`, `wtime`, and `btime`, turns them into a thinking time, and writes `format_info()`. |
| 8:45 to 9:25 | Pairs write `think()` (the iterative deepening loop): depth 1, then 2, then 3, keeping the best move of the deepest search that finished. |
| 9:25 to 9:35 | Show and choose for `think()`. The chosen code makes Remus-WHITE, the Remus with none of the enhancements and the starting point of every station. |
| 9:35 to 10:00 | The class watches Remus-WHITE play a 5-minute game against Stockfish at 1500 Elo in Lucas Chess and reads the `info` lines as it thinks. |

[`period1/README.md`](period1/README.md) lists the period's learning objectives, how each one is measured, and every change the pairs make.

## Period 2, 10:30 to 12:00: Python lab 12 and the enhancement stations

| Time | Activity |
| --- | --- |
| 10:30 to 10:50 | Pairs work through `python_caches.py`: a dict remembers answers, `math.dist()`, and `random.seed()`. |
| 10:50 to 11:00 | Slides: the ten color stations. Each is Remus-WHITE plus one enhancement, such as RED (transposition table) or BLUE (killer moves). Colors name the stations so that no station sounds better than another. |
| 11:00 to 12:00 | Each pair opens its color station in the `Remus` folder next to the Day folders, reads the station README, and writes the station's stubbed code. |

[`period2/README.md`](period2/README.md) lists the period's learning objectives, how each one is measured, and every change the pairs make.

## Period 3, 1:00 to 2:30: Enhancement stations: test and measure

| Time | Activity |
| --- | --- |
| 1:00 to 1:40 | Pairs finish their station code and pass its tests. |
| 1:40 to 2:10 | Each pair opens `smoke_test.py` in its station folder and presses Run in VS Code: one 2-minute game against Remus-WHITE, which checks only that the engine plays legal moves to the end. |
| 2:10 to 2:30 | Each pair writes one sentence on the board: what its enhancement should change, and how the class will see it. |

[`period3/README.md`](period3/README.md) lists the period's learning objectives, how each one is measured, and every change the pairs make.

## Period 4, 3:00 to 4:30: The mate solver

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Slides: the ten mate puzzles: nine mates in 2 and one mate in 3. A mate search asks a yes-or-no question instead of a score. |
| 3:15 to 3:55 | Pairs write `mating_move()` in `mate_solver.py`. |
| 3:55 to 4:20 | Pairs run `mate_solver.py` on all ten puzzles, including the mate in 3. |
| 4:20 to 4:30 | Checkpoint: every station passes its tests, and the mate solver solves all ten. |

[`period4/README.md`](period4/README.md) lists the period's learning objectives, how each one is measured, and every change the pairs make.

## By the end of the day

**Checkpoint:** Every station passes its tests and its one-game test match, and the mate solver solves all ten puzzles.

Each period folder starts from working code, so a pair that falls behind opens the next period's folder with the rest of the class.
