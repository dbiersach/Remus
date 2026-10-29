# How strong each Remus engine plays

This page rates the twelve Remus versions, Remus-WHITE (the finished Day 9 Remus with
no enhancements), the ten color versions, and Remus-GOLD (all ten enhancements), plus
Niram, the Rust copy of Remus-GOLD. Two yardsticks measure them:

1. **The league** plays the versions against each other. It measures the gaps between
   versions well, because every game pits two Remus versions of nearly equal strength.
2. **Stockfish** at a limited strength (`UCI_Elo`) puts each version on an Elo scale
   that people outside the class know. It measures the size of a rating well, but it
   cannot sort versions that sit only 30 or 40 Elo apart.

[`remus-niram parity.md`](remus-niram%20parity.md) shows that Niram picks exactly the same
moves as Remus-GOLD, so the two differ only in speed.

## The league: every version against the others

The designer's league holds 660 games at 10 minutes a side, every
version against every other version 10 times, 5 with each piece color. It ran on Niram,
the Rust twins of the 12 versions, which pick the same moves as Remus about 50 times
faster. The 450 games between versions without a book started from 32 openings; the
210 games with Remus-GREEN or Remus-GOLD started from the starting position, so
their book played from move 1. Each rating is the version's gain over Remus-WHITE,
pinned at 0, with a 95 percent margin. `misc/scripts/version_league.py --niram
--rate-only --event "Niram league 1" --book-start` rebuilds the table from the saved
games.

| Rank | Version | Folder | Wins-draws-losses | Score | Elo vs WHITE |
| ---: | --- | --- | --- | ---: | ---: |
| 1 | Remus-GOLD | [11 GOLD](../../../engines/instructor/11%20GOLD%20-%20All%20enhancements) | 79-30-1 | 85.5% | +339 +/- 91 |
| 2 | Remus-RED | [10 RED](../../../engines/instructor/10%20RED%20-%20Transposition%20table) | 27-71-12 | 56.8% | +101 +/- 67 |
| 3 | Remus-BLUE | [09 BLUE](../../../engines/instructor/09%20BLUE%20-%20Killer%20moves) | 20-74-16 | 51.8% | +67 +/- 67 |
| 4 | Remus-GREEN | [08 GREEN](../../../engines/instructor/08%20GREEN%20-%20Opening%20book) | 22-67-21 | 50.5% | +58 +/- 66 |
| 5 | Remus-PURPLE | [07 PURPLE](../../../engines/instructor/07%20PURPLE%20-%20Pawn%20structure) | 16-76-18 | 49.1% | +49 +/- 66 |
| 6 | Remus-BROWN | [06 BROWN](../../../engines/instructor/06%20BROWN%20-%20Late%20move%20reductions) | 6-89-15 | 45.9% | +28 +/- 66 |
| 7 | Remus-ORANGE | [05 ORANGE](../../../engines/instructor/05%20ORANGE%20-%20Null-move%20pruning) | 8-84-18 | 45.5% | +25 +/- 67 |
| 8 | Remus-PINK | [04 PINK](../../../engines/instructor/04%20PINK%20-%20Principal%20variation%20search) | 10-79-21 | 45.0% | +22 +/- 67 |
| 9 | Remus-CYAN | [03 CYAN](../../../engines/instructor/03%20CYAN%20-%20Mating%20bonus) | 12-74-24 | 44.5% | +19 +/- 67 |
| 10 | Remus-YELLOW | [02 YELLOW](../../../engines/instructor/02%20YELLOW%20-%20Draw%20sense) | 14-65-31 | 42.3% | +4 +/- 67 |
| 11 | Remus-GRAY | [01 GRAY](../../../engines/instructor/01%20GRAY%20-%20King%20safety) | 10-73-27 | 42.3% | +4 +/- 67 |
| 12 | Remus-WHITE | [00 WHITE](../../../engines/instructor/00%20WHITE%20-%20No%20enhancements) | 7-76-27 | 40.9% | 0 (pinned) |

Each version played 110 games. Remus-GOLD and Remus-RED are the only versions whose
range stays above 0; every other color version's range includes 0. Remus-YELLOW and
Remus-GRAY both scored 46.5 points, and Remus-YELLOW ranks above because it beat
Remus-GRAY 5.5 to 4.5. [`remus_versions.md`](remus_versions.md) explains the league
and each enhancement.

## The Stockfish rating plan

`misc/scripts/version_elo.py` plays every Remus version against Stockfish at 10
minutes a side, from frozen copies of the version folders, and adds every game to
`misc/games/remus_games.pgn` under the Event "Engine Elo test". The plan below has
not been played yet, so this page has no results from it.

| Setting | Value |
| --- | --- |
| Opponent | The newest Stockfish from [stockfishchess.org](https://stockfishchess.org/), the universal Windows build in `~/stockfish`, 1 thread, `UCI_LimitStrength` on, 1 second of `Move Overhead` |
| Remus levels (UCI_Elo) | 1650, 1800, 1950, 2100 |
| Niram levels (UCI_Elo) | 2000, 2200, 2400, 2600 |
| Games per version and level | 12: the version takes White in 6 and Black in 6 |
| Clock | 10 minutes a side, no increment |
| Games in all | 12 Remus versions x 48 + Niram x 48 = 624 |
| Games at once | 20 on an i9-13900F (24 cores) |
| Expected run time | about 9 hours, at about 17 minutes a game |

**Why these levels.** A game teaches the most about a rating when its result is
hardest to predict, at a 50 percent expected score. A game Remus is sure to win tells
almost nothing: in the first Stockfish run below, 10 of the 12 versions scored at least 5
of 6 against Stockfish 1320. All 360 games of that run pooled into one player give
1841, so the four Remus levels sit 150 Elo apart on both sides of 1850. Niram
searches about 50 times as many positions in the same time, so its levels sit higher.
Every Remus version plays the same four levels, so an error in how Stockfish sets one
level shifts every version alike and leaves their order untouched.

**How tight the ratings get.** One game at an even score carries a standard
deviation of 0.5 points, and a rating's 95 percent margin shrinks with the square root
of the games played. With 48 games near an even score, each version's margin comes to
about +/- 100 Elo, about half the +/- 185 of the first Stockfish run. Draws narrow it
further: the script measures each margin from how far every real score landed from
its expected score, so a version that draws often earns a narrower margin. The 576
Remus games pooled together pin the scale for the whole family to about +/- 30.

**What the run can and cannot show.** Two margins of +/- 100 combine to about
+/- 140 on a difference, so the run separates two versions 140 Elo or more apart,
such as Remus-GOLD and Remus-WHITE, which stand 339 Elo apart in the league above. It
cannot sort the nine color versions that sit within 70 Elo of Remus-WHITE in the
league: a gap of 35 Elo would take about 800 games per version. The league stays the
measure of those small gaps, and the Stockfish run places the whole group on a
familiar scale. A run that stops partway resumes from the
saved games, and running it again with `--games 24` adds a second 48 games per
version and brings each margin to about +/- 70.

**The scale runs high at 10 minutes.** Stockfish calibrates `UCI_Elo` at 60 seconds
plus 0.6 seconds a move. A limited Stockfish picks its move from a shallow search
plus a random choice among its best few moves, so a longer clock barely helps it,
while Remus searches several plies deeper at 10 minutes than at 1 minute. A 10-minute
rating therefore measures Remus at a long clock on a scale set at a short one, and it
reads higher than a rating from short games: an earlier `estimate_elo.py` run of
Remus-GOLD at 1 minute plus 0.6 seconds rated it about 1520 +/- 136.

## The first Stockfish run

In the first Stockfish run, twelve versions of Remus played Stockfish 19 on the course
designer's PC, with the
games under the Event "Station Elo test". The new run uses its own Event, so these
360 games stay out of its ratings.

### How the games were played

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

### The ratings

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

### Seven games Stockfish lost on time

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

### How the games ended

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

### Reading the numbers with care

**The versions are mostly tied.** Every margin is about +/- 185 Elo, because 30 games
cannot pin a rating more tightly. Two versions differ clearly only when their
intervals do not overlap, and only Remus-GREEN at the top and Remus-BROWN at the
bottom come close to that. Remus-GREEN, the opening-book color version, rated highest, but
with margins this wide its lead over Remus-GOLD and Remus-WHITE can be chance.

**The ratings run high,** for the reason the plan above gives.

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

The course designer runs these commands; no student or teacher needs them in
class. From the top Remus folder on a computer with at least 20 physical cores, after
`cargo build --release` inside `engines/Niram`:

```
uv run misc/scripts/version_elo.py --workers 20 --niram
```

A run that stops partway picks up from the games already in
`misc/games/remus_games.pgn`. `uv run misc/scripts/version_elo.py --report-only`
prints the tables from the saved games without playing any, and `--colors WHITE GOLD`
plays only the versions of those engine colors. Keep `--workers` at or below the number of physical cores,
because pure-Python Remus plays weaker when it shares a core.
