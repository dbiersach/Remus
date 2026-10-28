# Rating every Remus version against Stockfish

Twelve versions of Remus played Stockfish 19 on David's PC on 2026-10-27: Remus-WHITE
(the finished Day 9 Remus with no enhancements), the ten color versions, and
Remus-GOLD (all ten enhancements). `scripts/version_elo.py` ran the
games and fit the ratings, and every game is in `games/remus_games.pgn` under the
Event "Station Elo test".

## How the games were played

| Setting | Value |
| --- | --- |
| Opponent | Stockfish 19 from Lucas Chess, 1 thread, `UCI_LimitStrength` on |
| Stockfish levels (UCI_Elo) | 1320 (its weakest), 1615, 1910, 2205, 2500 |
| Games per version and level | 6: Remus took White in 3 and Black in 3 |
| Clock | 10 minutes a side, no increment |
| Games in all | 12 versions x 5 levels x 6 games = 360 |
| Games at once | 16, one per core of an i9-13900F (24 cores) |
| Run time | 22,676 seconds, about 6 hours 18 minutes |

Each version ran from a frozen copy of its version folder, so a change to the color version
code during the run could not change a version partway through its games. Every game
started from the normal starting position. Stockfish at a limited strength picks among
several moves at random, so no two games repeated.

## The ratings

A version's rating is the Elo whose expected total score against the five Stockfish
levels equals the version's real total score, the same method `estimate_elo.py` uses.
The margin is a 95 percent interval. Each cell under a Stockfish level shows the
points Remus scored out of 6 at that level (a win is 1, a draw is 1/2).

| Rank | Version | Elo | 95% margin | Score | SF 1320 | SF 1615 | SF 1910 | SF 2205 | SF 2500 |
| ---: | --- | ---: | ---: | ---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Remus-GREEN | 2036 | +/- 184 | 17.5/30 | 6/6 | 3.5/6 | 3/6 | 2.5/6 | 2.5/6 |
| 2 | Remus-GOLD | 1960 | +/- 184 | 16/30 | 5/6 | 5/6 | 2/6 | 2.5/6 | 1.5/6 |
| 3 | Remus-PURPLE | 1910 | +/- 183 | 15/30 | 6/6 | 3/6 | 2.5/6 | 2/6 | 1.5/6 |
| 4 | Remus-WHITE | 1885 | +/- 183 | 14.5/30 | 6/6 | 3/6 | 1.5/6 | 1.5/6 | 2.5/6 |
| 5 | Remus-PINK | 1885 | +/- 183 | 14.5/30 | 5/6 | 4.5/6 | 2.5/6 | 1/6 | 1.5/6 |
| 6 | Remus-GRAY | 1885 | +/- 183 | 14.5/30 | 6/6 | 2.5/6 | 3/6 | 1.5/6 | 1.5/6 |
| 7 | Remus-RED | 1860 | +/- 184 | 14/30 | 6/6 | 3.5/6 | 3/6 | 1/6 | 0.5/6 |
| 8 | Remus-ORANGE | 1834 | +/- 184 | 13.5/30 | 6/6 | 2/6 | 3/6 | 1/6 | 1.5/6 |
| 9 | Remus-YELLOW | 1758 | +/- 184 | 12/30 | 2.5/6 | 4/6 | 1/6 | 3/6 | 1.5/6 |
| 10 | Remus-CYAN | 1733 | +/- 185 | 11.5/30 | 6/6 | 1.5/6 | 2/6 | 0.5/6 | 1.5/6 |
| 11 | Remus-BLUE | 1707 | +/- 185 | 11/30 | 4/6 | 5/6 | 1/6 | 1/6 | 0/6 |
| 12 | Remus-BROWN | 1629 | +/- 187 | 9.5/30 | 5/6 | 1/6 | 2/6 | 1/6 | 0.5/6 |

All 360 games pooled into one player give **1841 +/- 53**.

## Seven games Stockfish lost on time

Remus never lost on time and never played an illegal move, and no engine crashed.
Stockfish lost 7 games on time. The referee charges each side the wall-clock time
around every move, and with 16 games sharing one Python process, that time includes
the referee's own waiting, which Stockfish cannot see on its clock. The table above
counts those 7 games as Remus wins. Without them, five ratings drop:

| Version | Elo, all games | Elo without the 7 | Games left |
| --- | ---: | ---: | ---: |
| Remus-GREEN | 2036 | 2019 +/- 190 | 29 |
| Remus-GOLD | 1960 | 1937 +/- 190 | 29 |
| Remus-RED | 1860 | 1849 +/- 188 | 29 |
| Remus-WHITE | 1885 | 1835 +/- 184 | 29 |
| Remus-ORANGE | 1834 | 1788 +/- 186 | 29 |
| Remus-YELLOW | 1758 | 1660 +/- 189 | 28 |

The other six versions lost no game this way and keep their ratings. Remus-YELLOW
owed 2 of its 12 points to these games. `version_elo.py` gives Stockfish one second
of `Move Overhead` on every move, so a later run keeps time in reserve for the
referee's waiting.

## How the games ended

| Stockfish level | Remus mated | Remus was mated | Draw by repetition | Stockfish lost on time |
| ---: | ---: | ---: | ---: | ---: |
| 1320 | 60 | 5 | 7 | 0 |
| 1615 | 34 | 30 | 7 | 1 |
| 1910 | 15 | 36 | 19 | 2 |
| 2205 | 7 | 45 | 17 | 3 |
| 2500 | 5 | 45 | 21 | 1 |
| All | 121 | 161 | 71 | 7 |

Every decided game ended in checkmate, and every draw came by threefold repetition.
No game reached the fifty-move rule, stalemate, or insufficient material.

## Reading the numbers with care

**The versions are mostly tied.** Every margin is about +/- 185 Elo, because 30 games
cannot pin a rating more tightly. Two versions differ clearly only when their
intervals do not overlap, and only Remus-GREEN at the top and Remus-BROWN at the
bottom come close to that. Remus-GREEN, the opening-book color version, rated highest, but
with margins this wide its lead over Remus-GOLD and Remus-WHITE can be chance.

**The ratings run high.** An earlier run of Remus-GOLD with `estimate_elo.py`, at 1 minute plus
0.6 seconds a move, rated it about 1520 +/- 136. Stockfish calibrates `UCI_Elo` at that short
clock. At 10 minutes Remus searches far deeper than at 1 minute, while Stockfish at a
limited strength still makes its built-in random mistakes. The 10-minute ratings
therefore measure Remus at a long clock on a scale set at a short clock.

**Remus beats the 2500 setting by catching its blunders.** Full-strength Stockfish
(depth 16) replayed two of Remus's checkmate wins over Stockfish 2500:

- Game 2500.5, Remus-CYAN as White, 14 moves. The position was level until Stockfish
  recaptured 12...Qxf6, which allows mate in 2 (13. Bb5+ Ke7 14. Qd7#). Recapturing
  12...gxf6 avoids the mate.
- Game 2500.4, Remus-PURPLE as Black, 43 moves. Stockfish's 14. Kd1 dropped about
  3.5 pawns and allowed 14...Nf2+, a knight fork of the king and the rook on h1.
  Remus then converted the extra material to mate.

Neither losing move is one that full-strength Stockfish chooses. At 2500, Remus
scored mostly by punishing a rare gross blunder from the weakened Stockfish, and by
21 draws by repetition, not by outplaying it.

## Run it again

From the top Remus folder on a computer with at least 16 physical cores:

```
uv run scripts/version_elo.py --workers 16
```

A run that stops partway picks up from the games already in `games/remus_games.pgn`.
`uv run scripts/version_elo.py --report-only` prints the table from the saved games without
playing any. Keep `--workers` at or below the number of physical cores, because
pure-Python Remus plays weaker when it shares a core.
