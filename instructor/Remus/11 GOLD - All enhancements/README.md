# Remus-GOLD: All enhancements

Remus-GOLD is the finished Remus of Day 10, with all ten enhancements at once. It stays out of the color matches; estimate_elo.py measures its rating against Stockfish.

## The idea, with an example

Remus-GOLD is the finished Day 10 Remus: Remus-WHITE plus all ten enhancements working together in one search, `upgraded_search()`. It probes the transposition table (RED), tries a null move (ORANGE), orders the moves with the stored best move and killers first (RED, BLUE), searches later moves with a null window (PINK) and late quiet moves one ply shallower (BROWN), scores repeated positions as draws (YELLOW), plays from the opening book (GREEN), and adds pawn structure, the mating bonus, and king safety to its evaluation (PURPLE, CYAN, GRAY).

## Why it is stronger

The search tricks multiply. The table and the killers put the best move first, a good first move makes PVS's null windows cheap, and null moves and late move reductions remove whole subtrees. Together they reach a ply or two deeper in the same time than Remus-WHITE, and the better evaluation chooses better among the moves it sees.

## What it costs

Its evaluation does three more scans of the board for every position, so Remus-GOLD evaluates fewer positions a second than Remus-WHITE. It wins that time back by visiting far fewer positions for each depth.

## Measured against Remus-WHITE

Each version searched the ten positions of `compare_search.py`, one depth at a time up to depth 4, on one computer. Fewer positions for the same depth means a smaller search tree. Positions per second shows what each position costs. The last column gave each position 5 seconds, the way a game does, and averages the deepest search that finished.

| Version | Positions to finish depth 4 | Share of Remus-WHITE's | Positions per second | Average depth in 5 seconds |
| --- | ---: | ---: | ---: | ---: |
| Remus-WHITE | 431,212 | 100% | 5,183 | 3.1 |
| Remus-GOLD | 84,812 | 20% | 4,511 | 4.9 |

## What to expect

Remus-GOLD is the only version whose gain over Remus-WHITE is larger than its error margin in the teacher's 10-minute league, and it gains more the longer the clock, because null moves and late move reductions save work only at depth 3 and deeper.

## Check it

Check it from inside this folder with `uv run pytest`, and rate it against Stockfish with `uv run estimate_elo.py`. From the top Remus folder, `uv run scripts/version_league.py --rate-only --player GOLD` shows its score against every other version in the teacher's league.
