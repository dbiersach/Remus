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

[`remus-niram_same_algorithms.md`](remus-niram_same_algorithms.md) shows that Niram
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
`misc/designer/version_league.py --niram --rate-only --event "Niram league 1"
--book-start` rebuilds the table from the saved games. The Version column names the
Remus version each Rust copy matches, and the Folder column links its Python engine
folder.

[`remus_versions.md`](../students/remus_versions.md#the-league-table) holds the table of
the league: rank, wins, draws, losses, score, and Elo over WHITE for every version.

Each version played 110 games. The ranges of Remus-GOLD, Remus-RED, and Remus-BLUE stay
above 0, Remus-BLUE's only just: +67.1 +/- 66.5 runs from +0.6 to +133.6. Every other
enhanced engine's range includes 0. Remus-YELLOW and
Remus-GRAY both scored 46.5 points, and Remus-YELLOW ranks above because it beat
Remus-GRAY 5.5 to 4.5. [`remus_versions.md`](../students/remus_versions.md) explains the league
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
every position ([`remus-niram_same_algorithms.md`](remus-niram_same_algorithms.md)), and both scored
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

## Rank every version again: version_league.py

`misc/designer/version_league.py` is a course designer tool: no student or teacher
runs it in class. Run from the top Remus folder, it plays a round robin: each of the 12 versions
(Remus-WHITE, the ten enhanced engines, and Remus-GOLD) plays each other version 6 times,
396 games in all, or as many times as `--games` asks. Then it fits one Elo rating to every version from every enhanced engine
game in the games file, the games of `version_match.py` included, with Remus-WHITE
pinned at 0. Each rating is that version's gain over Remus-WHITE. The league plays
at 10 minutes a side with no increment, because Remus in Python searches too slowly
for shorter games to show what an enhancement adds. `--minutes` and `--increment`
name another clock, and the script rates the games of each clock apart from the
others, since a version that searches deeper can gain more with more time to think.

```bash
uv run misc/designer/version_league.py --at-once 16   # the round robin, 16 games at a time
uv run misc/designer/version_league.py --rate-only    # only the ratings, from the saved games
uv run misc/designer/version_league.py --at-once 16 --event "Station league 2"
                                                # a new league, rated apart from the others
uv run misc/designer/version_league.py --book-start   # GREEN's and GOLD's games from move 1
```

The six opening moves hand every version a short book, so they hide most of what the
book of Remus-GREEN and Remus-GOLD is worth. With `--book-start`, every game with
GREEN or GOLD starts from the starting position instead. Their book picks among its
moves at random, so their games still differ from each other, while the other pairings
keep the openings. Rate such a league with `--book-start` as well.

The designer's league ran on Niram, Rust copies of all 12 versions that picked the
same moves as Remus about 15 times faster, so a 10-minute Niram game searched about
as many positions as a 2.5-hour Remus game. Only Niram is kept, in
`engines/Niram` ([`remus-niram_same_algorithms.md`](../designer/remus-niram_same_algorithms.md) shows that the two match), but
the league's games stay in the games file. `--niram --rate-only` rates them apart
from Remus games, with Niram-WHITE pinned at 0, and `version_elo.py --niram` plays
Niram against Stockfish ([`engines_elo.md`](../designer/engines_elo.md) gives its rating).

Without `--at-once`, the league plays one game per processor thread. Give it the
number of cores or fewer, because each game needs a whole core to itself to use its
clock fairly.

The fit works like `estimate_elo.py`: it moves each rating until the points the Elo
formula expects for a version equal the points it really scored. One pretend draw
against Remus-WHITE keeps a perfect score from giving an endless rating. A rating
of +60 plus or minus 80 means the true gain most likely lies between -20 and +140,
so two versions whose ranges overlap have not been told apart yet.

An engine that sends no move within its clock plus 10 seconds loses the game, with
the Termination "engine sent no move", so one silent engine cannot hold up the rest
of the league. Anything an engine prints to stderr, such as the traceback of a
crash, is saved with the game's names and opening in `misc/games/engine_errors.log`.

The league can stop partway, such as when a laptop restarts. Run it again and it
plays only the games that are not in the games file yet. A 10-minute Remus game lasts
about 16 minutes on average, so a 24-core computer playing 16 games at a time finishes
about one game a minute and the 396-game league in about 7 hours. A 4-core laptop
playing 4 games at a time needs about a day.

## How big is each version?

The table counts the lines of Python code in each version. A line counts only when
it holds code: comment lines, docstrings, and blank lines do not count. The count
covers only the engine's own `.py` files, the ones `uci_engine.py` loads directly or
through another module when Lucas Chess runs that version. Test files and tools such
as `perft.py` and `play_match.py` do not count.

| Version | Enhancement | Engine files | Code lines | Lines over WHITE |
| --- | --- | ---: | ---: | ---: |
| Remus-WHITE | No enhancements | 12 | 1,058 | 0 |
| Remus-GRAY | King safety | 12 | 1,088 | +30 |
| Remus-YELLOW | Draw sense | 12 | 1,100 | +42 |
| Remus-CYAN | Mating bonus | 12 | 1,088 | +30 |
| Remus-PINK | Principal variation search | 12 | 1,110 | +52 |
| Remus-ORANGE | Null-move pruning | 12 | 1,137 | +79 |
| Remus-BROWN | Late move reductions | 12 | 1,110 | +52 |
| Remus-PURPLE | Pawn structure | 12 | 1,095 | +37 |
| Remus-GREEN | Opening book | 14 | 1,200 | +142 |
| Remus-BLUE | Killer moves | 12 | 1,112 | +54 |
| Remus-RED | Transposition table | 13 | 1,145 | +87 |
| Remus-GOLD | All enhancements | 15 | 1,491 | +433 |

Remus-GOLD holds 433 more code lines than Remus-WHITE. The ten enhanced engines add 605
lines when each one is counted on its own, so GOLD needs 172 fewer. Most enhanced engines
change the same search loop in `search.py`, and GOLD holds one copy of that loop
with all ten ideas inside it. GREEN adds the most lines of any single enhancement, 142,
because its book reads moves in SAN and so loads `notation.py` as well.

[The program overview](../students/remus_program_overview.md#remus-gold-code-lines-script-by-script) splits
Remus-GOLD's 1,491 code lines among its 15 engine scripts.

## Run it again

The course designer runs these commands; no student or teacher needs them in
class. From the top Remus folder on a computer with at least 24 physical cores, after
`cargo build --release` inside `engines/Niram`, this command plays the bracket run:

```
uv run misc/designer/version_elo.py --bracket --colors WHITE GOLD --niram --workers 24
```

A bracket run that stops partway picks up from the games already in
`misc/games/remus_games.pgn`. `--rounds` counts every round, the saved ones included,
so `--rounds 16` adds 8 more rounds to each engine, and `--round-games` sets the
games per engine in each round. Without `--bracket`, `version_elo.py` plays every
version at four fixed Stockfish levels under the Event "Engine Elo test", `--colors`
picks the versions, and `--report-only` prints the tables from the saved games
without playing any. Keep `--workers` at or below the number of physical cores,
because pure-Python Remus plays weaker when it shares a core.
