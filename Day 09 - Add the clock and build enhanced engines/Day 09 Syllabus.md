# Day 9: The clock and the enhanced engines

Day 9 gives Remus a clock, then splits the class into ten enhancement color versions. Each pair adds one idea to the same engine, Remus-WHITE, and tests it. In period 4 the pairs carry their color versions to each other's laptops on USB sticks and battle. By 4:30 every color version passes its tests and has played two battles.

## Objectives for the day

By 4:30, each pair can:

- Search deeper one step at a time and keep the best move of the deepest search that finished before time ran out.
- Read the `info` lines Remus sends to Lucas Chess: depth, score, nodes, and the principal variation.
- Use a dict as a cache with a tuple as its key.
- Add one enhancement to Remus-WHITE, test it, and say what it should change in a game.
- Play two color versions against each other, and read the result with its uncertainty.

## The day at a glance

| Period | Time | Title | Pairs write |
| --- | --- | --- | --- |
| P1 | 8:30 to 10:00 | Iterative deepening, the clock, and UCI info | `think()` in `search.py` (17 lines) |
| | 10:00 to 10:30 | Break | |
| P2 | 10:30 to 12:00 | Python lab 12 and the color versions | The lab `python_caches.py` (7 lines); their color version's functions, from the version README |
| | 12:00 to 1:00 | Lunch | |
| P3 | 1:00 to 2:30 | Color versions: test and measure | Their color version's functions, from the version README |
| | 2:30 to 3:00 | Break | |
| P4 | 3:00 to 4:30 | Color battles | The demo `demo_results.py` (13 lines) |

## Period 1, 8:30 to 10:00: Iterative deepening, the clock, and UCI info

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Slides: the clock. The teacher reads `go movetime`, `wtime`, and `btime`, turns them into a thinking time, and writes `format_info()`. |
| 8:45 to 9:25 | Pairs write `think()` (the iterative deepening loop): depth 1, then 2, then 3, keeping the best move of the deepest search that finished. |
| 9:25 to 9:35 | Show and choose for `think()`. The chosen code makes Remus-WHITE, the Remus with none of the enhancements and the starting point of every color version. |
| 9:35 to 10:00 | The class watches Remus-WHITE play a 5-minute game against Stockfish at 1500 Elo in Lucas Chess and reads the `info` lines as it thinks. |

[`Day 09 Period 01 Goals.md`](<period1/Day 09 Period 01 Goals.md>) lists the period's learning objectives, how each one is measured, every change the pairs make, and their exact tasks.

## Period 2, 10:30 to 12:00: Python lab 12 and the color versions

| Time | Activity |
| --- | --- |
| 10:30 to 10:50 | Pairs work through `python_caches.py`: a dict remembers answers, `math.dist()`, and `random.seed()`. |
| 10:50 to 11:00 | Slides: the ten color versions. Each is Remus-WHITE plus one enhancement, such as RED (transposition table) or BLUE (killer moves). Colors name the color versions so that no color version sounds better than another. |
| 11:00 to 12:00 | Each pair opens its color version in `period2/student/engines`, reads the version README, and writes the color version's stubbed code. |

[`Day 09 Period 02 Goals.md`](<period2/Day 09 Period 02 Goals.md>) lists the period's learning objectives, how each one is measured, every change the pairs make, and their exact tasks.

## Period 3, 1:00 to 2:30: Color versions: test and measure

| Time | Activity |
| --- | --- |
| 1:00 to 1:40 | Pairs finish their color version code and pass its tests. |
| 1:40 to 2:10 | Each pair opens `smoke_test.py` in its version folder and presses Run in VS Code: one 2-minute game against Remus-WHITE, which checks only that the engine plays legal moves to the end. |
| 2:10 to 2:30 | Each pair writes one sentence on the board: what its enhancement should change, and how the class will see it. |

[`Day 09 Period 03 Goals.md`](<period3/Day 09 Period 03 Goals.md>) lists the period's learning objectives, how each one is measured, every change the pairs make, and their exact tasks.

## Period 4, 3:00 to 4:30: Color battles

| Time | Activity |
| --- | --- |
| 3:00 to 3:10 | Slides: how a battle works. Each pair copies its own color folder from `period2/student/engines` onto its USB stick. The teacher posts the pairings for two rounds; in each round five pairs host and five visit. |
| 3:10 to 3:40 | Round 1. The visiting pair copies its color folder over the folder of the same engine color in the host laptop's `engines` folder. The host opens `play_battle.py` in its own color folder, presses Run in VS Code, and types the visitor's engine color. Two 10-minute games run side by side, one with each piece color. Each pair writes the score on the board. |
| 3:40 to 3:45 | Round 2: the pairs that visited now host, against new opponents. |
| 3:45 to 4:10 | While the round 2 games run, each pair turns its round 1 result into an Elo gap with a margin of error in `demo_results.py`, then tries its engine color's league games. |
| 4:10 to 4:25 | The class reads the board: which engine colors won, and why two games prove little. The teacher shows the league table, 110 games for each engine color, and compares. |
| 4:25 to 4:30 | Each visiting pair takes its USB stick back. The visitor's folder stays on the host laptop in place of an engine color the host pair never writes, so the host's own color folder is untouched. |

[`Day 09 Period 04 Goals.md`](<period4/Day 09 Period 04 Goals.md>) lists the period's learning objectives, how each one is measured, every change the pairs make, and their exact tasks.

## By the end of the day

**Checkpoint:** Every color version passes its tests and its one-game test match, and has played two battles against other engine colors.

Each period folder starts from working code, so a pair that falls behind opens the next period's folder with the rest of the class.
