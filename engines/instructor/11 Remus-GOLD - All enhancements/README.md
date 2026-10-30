# Remus-GOLD: All enhancements

Remus-GOLD is the finished Remus of Day 10, with all ten enhancements at once. It lives only in the teacher's folders; estimate_elo.py measures its rating against Stockfish, and Niram, in engines/Niram, is the same engine in Rust.

## The idea, with an example

Remus-GOLD is the finished Day 10 Remus: Remus-WHITE plus all ten enhancements working together in one search, `upgraded_search()`. It probes the transposition table (RED), tries a null move (ORANGE), orders the moves with the stored best move and killers first (RED, BLUE), searches later moves with a null window (PINK) and late quiet moves one ply shallower (BROWN), scores repeated positions as draws (YELLOW), plays from the opening book (GREEN), and adds pawn structure, the mating bonus, and king safety to its evaluation (PURPLE, CYAN, GRAY).

## Why it is stronger

The search tricks multiply. The table and the killers put the best move first, a good first move makes PVS's null windows cheap, and null moves and late move reductions remove whole subtrees. Together they reach a ply or two deeper in the same time than Remus-WHITE, and the better evaluation chooses better among the moves it sees.

## What it costs

Its evaluation does three more scans of the board for every position, so Remus-GOLD evaluates fewer positions a second than Remus-WHITE. It wins that time back by visiting far fewer positions for each depth.

## Measured against Remus-WHITE

Each version searched the ten positions of the designer's benchmark, `misc/scripts/remus_benchmark.py`, one depth at a time up to depth 4, on one computer. Fewer positions for the same depth means a smaller search tree. Positions per second shows what each position costs. The last column gave each position 5 seconds, the way a game does, and averages the deepest search that finished.

| Version | Positions to finish depth 4 | Share of Remus-WHITE's | Positions per second | Average depth in 5 seconds |
| --- | ---: | ---: | ---: | ---: |
| Remus-WHITE | 431,212 | 100% | 5,183 | 3.1 |
| Remus-GOLD | 84,812 | 20% | 4,511 | 4.9 |

## What to expect

In the designer's league, where every version searched about as deep as Remus does in a game of several hours, Remus-GOLD scored 85 percent and rated +339 plus or minus 91 over Remus-WHITE, far ahead of every engine with one enhancement. It gains more the longer the clock, because null moves and late move reductions save work only at depth 3 and deeper.

## Check it

Check it by opening `run_tests.py` in this folder and clicking Run Python File, and rate it against Stockfish the same way with `estimate_elo.py`. [`engines_elo.md`](../../../misc/docs/engine_comparison/engines_elo.md) shows its score against every other version in the designer's league.
