# How strong each Remus engine plays

This page rates the twelve Remus versions: Remus-WHITE (the finished Day 9 Remus with
no enhancements), the ten enhanced engines, and Remus-GOLD (all ten enhancements),
plus Niram, the Rust copy of Remus-GOLD. Two yardsticks measure them:

1. **The league** plays all twelve versions against each other. It measures the gaps
   between versions well, because every game pits two Remus versions of nearly equal
   strength.
2. **Stockfish** at a limited strength (`UCI_Elo`) puts Remus-WHITE, Remus-GOLD, and
   Niram on an Elo scale that people outside the class know. It measures the size of
   a rating well, but it cannot sort versions that sit only 30 or 40 Elo apart.

[`remus-niram same algorithms.md`](remus-niram%20same%20algorithms.md) shows that Niram
runs the same algorithms as Remus-GOLD and picks the same moves at the same depth. The
two engines differ in speed, and the speed gap makes Niram far stronger with a clock.

## The league: every version against the others, in Rust

The designer's league did not play the Python engines. It played Rust copies of all
12 versions, Niram-WHITE to Niram-GOLD, which run the same algorithms as the Python
versions and pick the same moves, only much faster. That is why its games carry the
Event "Niram league 1" and why `version_league.py` needs `--niram` to rate them. The
Rust copies let 660 games at 10 minutes a side finish in one night, and they search
deep enough for every enhancement to show what it adds. Only Niram, the copy of
Remus-GOLD, is kept in `engines/Niram`; the games of the other copies stay in the
games file.

Every version played every other version 10 times, 5 with each piece color. The 450
games between versions without a book started from 32 openings; the 210 games with
GREEN or GOLD started from the starting position, so their book played from move 1. The
games file also holds 210 earlier GREEN and GOLD games started from the openings;
`--book-start` leaves those out.
Each rating is the version's gain over WHITE, pinned at 0, with a 95 percent margin.
`misc/scripts/version_league.py --niram --rate-only --event "Niram league 1"
--book-start` rebuilds the table from the saved games. The Version column names the
Remus version each Rust copy matches, and the Folder column links its Python engine
folder.

| Rank | Version | Folder | Wins-draws-losses | Score | Elo vs WHITE |
| ---: | --- | --- | --- | ---: | ---: |
| 1 | Remus-GOLD | [11 Remus-GOLD](../../../engines/instructor/11%20Remus-GOLD%20-%20All%20enhancements) | 79-30-1 | 85.5% | +339 +/- 91 |
| 2 | Remus-RED | [10 Remus-RED](../../../engines/instructor/10%20Remus-RED%20-%20Transposition%20table) | 27-71-12 | 56.8% | +101 +/- 67 |
| 3 | Remus-BLUE | [09 Remus-BLUE](../../../engines/instructor/09%20Remus-BLUE%20-%20Killer%20moves) | 20-74-16 | 51.8% | +67 +/- 66 |
| 4 | Remus-GREEN | [08 Remus-GREEN](../../../engines/instructor/08%20Remus-GREEN%20-%20Opening%20book) | 22-67-21 | 50.5% | +58 +/- 66 |
| 5 | Remus-PURPLE | [07 Remus-PURPLE](../../../engines/instructor/07%20Remus-PURPLE%20-%20Pawn%20structure) | 16-76-18 | 49.1% | +49 +/- 66 |
| 6 | Remus-BROWN | [06 Remus-BROWN](../../../engines/instructor/06%20Remus-BROWN%20-%20Late%20move%20reductions) | 6-89-15 | 45.9% | +28 +/- 66 |
| 7 | Remus-ORANGE | [05 Remus-ORANGE](../../../engines/instructor/05%20Remus-ORANGE%20-%20Null-move%20pruning) | 8-84-18 | 45.5% | +25 +/- 66 |
| 8 | Remus-PINK | [04 Remus-PINK](../../../engines/instructor/04%20Remus-PINK%20-%20Principal%20variation%20search) | 10-79-21 | 45.0% | +22 +/- 67 |
| 9 | Remus-CYAN | [03 Remus-CYAN](../../../engines/instructor/03%20Remus-CYAN%20-%20Mating%20bonus) | 12-74-24 | 44.5% | +19 +/- 67 |
| 10 | Remus-YELLOW | [02 Remus-YELLOW](../../../engines/instructor/02%20Remus-YELLOW%20-%20Draw%20sense) | 14-65-31 | 42.3% | +4 +/- 67 |
| 11 | Remus-GRAY | [01 Remus-GRAY](../../../engines/instructor/01%20Remus-GRAY%20-%20King%20safety) | 10-73-27 | 42.3% | +4 +/- 67 |
| 12 | Remus-WHITE | [00 Remus-WHITE](../../../engines/instructor/00%20Remus-WHITE%20-%20No%20enhancements) | 7-76-27 | 40.9% | 0 (pinned) |

Each version played 110 games. The ranges of Remus-GOLD, Remus-RED, and Remus-BLUE stay
above 0, Remus-BLUE's only just: +67.1 +/- 66.5 runs from +0.6 to +133.6. Every other
enhanced engine's range includes 0. Remus-YELLOW and
Remus-GRAY both scored 46.5 points, and Remus-YELLOW ranks above because it beat
Remus-GRAY 5.5 to 4.5. [`remus_versions.md`](remus_versions.md) explains the league
and each enhancement.

At Python speed the gaps shrink, because the Python engines search fewer plies in the
same 10 minutes. In the Python match further down, Remus-GOLD beat Remus-WHITE by
about +147, less than half of the +339 its Rust copy gained here.

## The Stockfish bracket run

Remus-WHITE, Remus-GOLD, and Niram each played 64 games against Stockfish 19 at 10
minutes a side, under the Event "Engine Elo bracket" in `misc/games/remus_games.pgn`.
The run took 2 hours 31 minutes for 192 games, 24 at once on the course designer's PC.
No engine crashed or lost on time.

| Setting | Value |
| --- | --- |
| Opponent | Stockfish 19 from [stockfishchess.org](https://stockfishchess.org/), the universal Windows build in `~/stockfish` (the same build Lucas Chess installs), 1 thread, `UCI_LimitStrength` on, `Move Overhead` 1000 ms (a 1-second safety cushion: Stockfish still has its full 10 minutes, but plans each move as if 1 second less were left, so the delay of passing moves between programs never makes it lose on time) |
| Rounds | 8, with 8 games per engine in each round: 4 with White and 4 with Black |
| Clock | 10 minutes a side, no increment |
| Games in all | 3 engines x 64 = 192 |
| Games at once | 24 on an i9-13900F (24 cores) |
| Run time | 9,048 seconds, about 2 hours 31 minutes |

**How the bracket works.** A game teaches the most about a rating when its result is
hardest to predict, at a 50 percent expected score, so the run aims Stockfish at each
engine's strength. Round 1 starts from a guess: Stockfish 1850 for Remus-WHITE, 2000
for Remus-GOLD, and 2500 for Niram. After each round, the script rates the engine
from all of its games so far and sets the next round's Stockfish level to that rating,
rounded to a multiple of 25. The levels close in on the rating, so most games land near
an even score.

### The ratings

A rating is the Elo whose expected total score against the Stockfish levels it met
equals the engine's real total score, the same method `estimate_elo.py` uses. The
margin is a 95 percent interval, measured from how far every real score landed from
its expected score.

| Rank | Engine | Elo | 95% margin | Score |
| ---: | --- | ---: | ---: | ---: |
| 1 | Niram | 2354 | +/- 80 | 31/64 |
| 2 | Remus-GOLD | 1731 | +/- 77 | 31/64 |
| 3 | Remus-WHITE | 1681 | +/- 79 | 24.5/64 |

All 128 Python Remus games pooled into one player give **1706 +/- 55**.

The ratings after each round show the bracket settling:

| After round | Remus-WHITE | Remus-GOLD | Niram |
| ---: | ---: | ---: | ---: |
| 1 | 1894 | 1745 | 2363 |
| 2 | 1831 | 1721 | 2322 |
| 3 | 1769 | 1670 | 2369 |
| 4 | 1735 | 1684 | 2359 |
| 5 | 1714 | 1692 | 2348 |
| 6 | 1684 | 1725 | 2326 |
| 7 | 1682 | 1732 | 2332 |
| 8 | 1681 | 1731 | 2354 |

Each engine's score at each Stockfish level it met:

| Engine | Stockfish levels, in round order | Score at each level |
| --- | --- | --- |
| Remus-WHITE | 1850, 1900, 1825, 1775, 1725, 1725, 1675, 1675 | 1675: 8/16, 1725: 5/16, 1775: 2.5/8, 1825: 2/8, 1850: 4.5/8, 1900: 2.5/8 |
| Remus-GOLD | 2000, 1750, 1725, 1675, 1675, 1700, 1725, 1725 | 1675: 9/16, 1700: 6/8, 1725: 11/24, 1750: 3.5/8, 2000: 1.5/8 |
| Niram | 2500, 2375, 2325, 2375, 2350, 2350, 2325, 2325 | 2325: 16/24, 2350: 6/16, 2375: 6.5/16, 2500: 2.5/8 |

### What the bracket shows

**Niram rates about 620 Elo above Remus-GOLD.** The two engines pick the same move in
every position ([`remus-niram same algorithms.md`](remus-niram%20same%20algorithms.md)), and both scored
31 of 64. Niram scored its 31 points against Stockfish set about 600 Elo higher. The
whole gap comes from speed: Niram searches about 15 times as many positions in the
same 10 minutes, deep enough for null-move pruning, late move reductions, and the
transposition table to pay off.

**Remus-GOLD finished 50 Elo above Remus-WHITE, but the bracket alone cannot call
that a win.** Two margins of about +/- 78 combine to about +/- 110 on a difference.
Remus-GOLD trailed Remus-WHITE for the first five rounds and moved ahead in rounds 6
to 8. At Python speed Remus-GOLD reaches only a few plies in 10 minutes, so most of its
enhancements get little chance to work, and its evaluation costs about three times as
much per position as Remus-WHITE's.

**Remus-GOLD and Niram score less with Black.** Over all 64 games, Remus-GOLD and
Niram each scored 19.5 of 32 with White and 11.5 of 32 with Black, while Remus-WHITE
scored 13 of 32 with White and 11.5 of 32 with Black. Moving first helps Stockfish
when Remus plays Black, but Remus-WHITE shows only a small gap, so the larger gap may
come from how Remus-GOLD plays Black, perhaps its opening book. Thirty-two games with
each piece color cannot settle the cause.

**Elo is not fully transitive.** An engine can beat another head to head and still
score the same against a third. Remus-GOLD shares Remus-WHITE's search and
evaluation, so its enhancements aim at exactly the mistakes Remus-WHITE makes.
Stockfish wins mostly with tactics deeper than either Remus sees.

**The scale runs high at 10 minutes.** Stockfish calibrates `UCI_Elo` at 60 seconds
plus 0.6 seconds a move. A limited Stockfish picks its move from a shallow search
plus a random choice among its best few moves, so a longer clock barely helps it,
while Remus searches several plies deeper at 10 minutes than at 1 minute. A 10-minute
rating therefore measures Remus at a long clock on a scale set at a short one, so it
reads higher than a rating from short games would.

### Remus-GOLD against Remus-WHITE in Python

The bracket left the two Python engines within each other's margins, so they also
played each other directly: 20 games at 10 minutes a side, all at once, with each
engine taking White in 10. Each pair of games started from one of the 3-move
openings in `version_match.py`, so Remus-GOLD's book did not play. The games sit in
`misc/games/remus_games.pgn` under the Event "Station match Remus-GOLD vs Remus-WHITE".

| Engine | Wins | Draws | Losses | Score | Elo gap |
| --- | ---: | ---: | ---: | ---: | ---: |
| Remus-GOLD | 11 | 6 | 3 | 14/20 | +147 +/- about 135 |

Remus-GOLD scored 6.5 of 10 with White and 7.5 of 10 with Black. Remus-GOLD clearly
beats Remus-WHITE head to head, by less than half of the +339 that the Rust copies
showed in the league, because Python reaches shallower depths where the enhancements
help less. Against Stockfish the same two engines stand only 50 Elo apart: Remus-GOLD's
enhancements punish Remus-WHITE's own blind spots more than they help against an
opponent with different ones.

## Run it again

The course designer runs these commands; no student or teacher needs them in
class. From the top Remus folder on a computer with at least 24 physical cores, after
`cargo build --release` inside `engines/Niram`, this command plays the bracket run:

```
uv run misc/scripts/version_elo.py --bracket --colors WHITE GOLD --niram --workers 24
```

A bracket run that stops partway picks up from the games already in
`misc/games/remus_games.pgn`. `--rounds` counts every round, the saved ones included,
so `--rounds 16` adds 8 more rounds to each engine, and `--round-games` sets the
games per engine in each round. Without `--bracket`, `version_elo.py` plays every
version at four fixed Stockfish levels under the Event "Engine Elo test", `--colors`
picks the versions, and `--report-only` prints the tables from the saved games
without playing any. Keep `--workers` at or below the number of physical cores,
because pure-Python Remus plays weaker when it shares a core.
