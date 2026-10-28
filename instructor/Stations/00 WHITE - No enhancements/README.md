# Remus-WHITE: No enhancements

Remus-WHITE is the finished Day 9 Remus with none of the ten enhancements. Every station starts from it, and every station match measures against it.

## The idea, with an example

Remus-WHITE thinks the way the class built it through Day 9. `think()` searches 1 ply deep, then 2, then 3, until its time for the move runs out, and plays the best move of the deepest search that finished. Each search is alpha-beta: once one reply shows a move is worse than a move already found, Remus stops looking at that move. At the end of every line, quiescence keeps playing captures until the position is quiet, so Remus never stops counting in the middle of a trade. Captures are tried first, most valuable victim and least valuable attacker first (MVV-LVA), and the best move of the last depth is tried before everything else.

## Why it matters

Every color station is Remus-WHITE plus exactly one change. Playing each station against Remus-WHITE is a fair experiment: same openings, both colors, and only one thing different.

## What it costs

Remus-WHITE is pure Python, so it searches only a few thousand positions a second. Most of them are quiescence positions at the ends of lines. With 10 minutes for a game, Remus thinks about 20 seconds a move and usually finishes depth 4 or 5 in the middlegame.

## Measured against Remus-WHITE

Each version searched the ten positions of `compare_search.py`, one depth at a time up to depth 4, on one computer. Fewer positions for the same depth means a smaller search tree. Positions per second shows what each position costs. The last column gave each position 5 seconds, the way a game does, and averages the deepest search that finished.

| Version | Positions to finish depth 4 | Share of Remus-WHITE's | Positions per second | Average depth in 5 seconds |
| --- | ---: | ---: | ---: | ---: |
| Remus-WHITE | 431,212 | 100% | 5,183 | 3.1 |

## What to expect

Remus-WHITE is pinned at 0 in every league table, so every other version's rating is its gain or loss against Remus-WHITE.

## Check it

Check it from inside this folder with `uv run pytest`. From the Stations folder, `uv run station_match.py WHITE RED` plays it against a station.
