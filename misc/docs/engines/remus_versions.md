# Color versions: one color, one idea

## The big picture

Remus-WHITE is the finished Day 9 Remus with none of the enhancements. It already
searches with alpha-beta, quiescence, move ordering, iterative deepening, and a
clock. Ten ideas can make it stronger. On Day 9, in periods 2 and 3, each student pair builds
one of them, so the class can measure which idea adds the most strength. In period 4
the student pairs carry their color versions to each other's laptops and play battles to find
out which engine color is strongest.

Each color version has an engine color instead of a number or a letter, so no color version sounds
better than another before the games are played.

## Where the color versions live

The Remus versions live in the `engines` folder at the top of the Remus folder, which
holds three folders:

| Folder | Holds |
| --- | --- |
| `engines/instructor` | `00 WHITE - No enhancements` to `11 GOLD - All enhancements`, the finished engines, and `version_match.py` |
| `engines/student` | `00 WHITE - No enhancements` to `10 RED - Transposition table`, with the functions each student pair writes stubbed, and `version_match.py` |
| `engines/Niram` | Niram, Remus-GOLD rewritten in Rust, a course designer's tool |

`00 WHITE - No enhancements` is Remus-WHITE, an exact copy of the Day 9 `period1`
folder: the Day 9 Remus at the end of period 1, when its engine is finished and before
the student pairs start their color versions. Each engine folder from `01 GRAY` to
`10 RED`, such as `10 RED - Transposition table`, is a complete copy of Remus-WHITE plus
one enhancement. From period 2 to the end of the day, each student pair works only in
its engine folder in `engines/student`, so periods 2, 3, and 4 of Day 9 hold no engine
code of their own. The number in front of each color version ranks it by its rating
over Remus-WHITE in the designer's 10-minute league (below), from 01 GRAY to 10 RED.

`11 GOLD - All enhancements` is Remus-GOLD, the finished Remus of Day 10 with all ten
enhancements at once. No student pair writes GOLD, so only `engines/instructor` holds
it. `make_version_folders.py` copies Remus-WHITE and builds the ten color versions from
the Day 9 `period1` code and Remus-GOLD.

## Remus Engine Enhancements

| Folder | Enhancement | The idea in one line | The student pair writes | Lines to type |
| --- | --- | --- | --- | --- |
| 01 GRAY | King safety | Reward pawns that shelter the king while the enemy queen is on the board | `king_safety()` in `evaluation.py` | 20 |
| 02 YELLOW | Draw sense | Score a repeated position, or one at the fifty-move limit, as 0 inside the search | `is_draw_in_search()` in `search.py`, plus 3 tests in `test_upgrades.py` | 16 |
| 03 CYAN | Mating bonus | With a big lead, drive the losing king to the edge | `mating_bonus()` in `evaluation.py` | 24 |
| 04 PINK | Principal variation search | Search the first move with the full window and the rest with a cheap null window | `search_later_move()` in `search.py`, plus 2 tests in `test_upgrades.py` | 18 |
| 05 ORANGE | Null-move pruning | Let the opponent move twice; if Remus is still too far ahead, the opponent would never allow this position, so stop searching it | `make_null_move()` in `search.py` and `undo_null_move()` in `search.py`, plus 2 tests in `test_upgrades.py` | 23 |
| 06 BROWN | Late move reductions | Search late, quiet moves one ply shallower, and in full only if they surprise | `reduction()` in `search.py`, plus 2 tests in `test_upgrades.py` | 18 |
| 07 PURPLE | Pawn structure | Penalize doubled and isolated pawns, reward passed pawns | `pawn_structure()` in `evaluation.py` | 30 |
| 08 GREEN | Opening book | Play the first moves of well-known openings from a book | `load_book()` in `opening_book.py` and `book_move()` in `opening_book.py` | 24 |
| 09 BLUE | Killer moves | Try quiet moves that caused a cutoff at the same depth right after the captures | `remember_killer()` in `search.py` and `order_moves()` in `move_ordering.py`, plus 1 test in `test_upgrades.py` | 27 |
| 10 RED | Transposition table | Remember positions already searched, so one position reached in two move orders is scored once | `store()` in `transposition_table.py` and `probe()` in `transposition_table.py`, plus 1 test in `test_upgrades.py` | 27 |

Every color version asks for 16 to 30 typed lines, under the 40-line limit for one period. Where the enhancement itself is short, the student pair also writes the tests that prove it works, such as the test that a null window answers only "better or not?", so every student pair spends both periods thinking about its idea rather than waiting.

## Words to know

- **Elo gap:** the rating difference that a match score suggests. A 75 percent
  score means a gap of about +191.
- **yardstick:** Remus-WHITE. Every color version plays the same opponent, so
  the gaps compare fairly.
- **null window:** a search window one point wide, (alpha, alpha + 1). It answers
  only "better or not?", which takes far less work than an exact score.

## How a color version search works

Each search color version adds one new function to `search.py` beside
`alpha_beta_with_quiescence`, and `think()` calls the new function. The new function
is the Day 9 search with one change, so a student pair can compare the two side by side:

| Engine color | New search function | What changes |
| --- | --- | --- |
| RED | `table_search` | Look up the position before searching; store the result after |
| BLUE | `killer_search` | Pass this ply's killers to `order_moves()`; remember a quiet move that cuts off |
| PINK | `pvs_search` | Search every move after the first with `search_later_move()` |
| YELLOW | `draw_sense_search` | Return 0 at once when `is_draw_in_search()` says so |
| ORANGE | `null_move_search` | Before the moves, try a pass with a search 2 plies shallower |
| BROWN | `reduced_search` | Cut one ply from late, quiet moves; search again in full on a surprise |

The evaluation color versions (PURPLE, CYAN, GRAY) add one term to `evaluate()` and one
line to `explain_evaluation()`. The GREEN color version asks the book before searching, in
both `uci_engine.py` and `console_game.py`.

## The Day 9 battles: version_match.py

`version_match.py`, in `engines/student` and `engines/instructor`, plays a color version's Remus against Remus-WHITE,
or against another color version, at 10 minutes a side. It adds every game to
`misc/games/remus_games.pgn` and prints the score.

Nobody types a command to run it. Every engine folder holds two short scripts that
run `version_match.py` for its own engine color, so a student pair (or the teacher) opens one in VS
Code and presses the Run Python File button:

| Script | When | What it plays |
| --- | --- | --- |
| `smoke_test.py` | Day 9, period 3 | One 2-minute game against Remus-WHITE, to show the engine plays legal moves to the end |
| `play_battle.py` | Day 9, period 4 | A battle: two 10-minute games against a visiting color version, one with each piece color |

In the Day 9 battles a visiting student pair brings its engine folder on a USB drive and
copies it over the folder of the same engine color in the host's `engines/student`, which
holds that engine color with its functions still stubbed. The
host opens `play_battle.py` in its own engine folder, sets `VISITING_ENGINE` to the
visitor's engine color, such as `"RED"`, and presses Run. The numbered steps at the top
of `play_battle.py` walk through the whole battle. The two engine colors play twice from the same opening, once with each
piece color, about 20 minutes for both games. Each battle goes on the board as a row of the
class table, and the period has room for two rounds. The visitor's folder stays on the
host laptop when the visitor leaves: it replaces only the stubs of an engine color the host
student pair never writes, and the host's own engine folder is untouched. Two games cannot show which enhancement is
stronger, so the script prints no Elo gap for fewer than 10 games; while round 2
runs, each student pair puts its round 1 score into `demo_results.py` and sees how wide the
margin of error is. The teacher then shows the league table in
[`engines_elo.md`](engines_elo.md), which rates every engine color from 110 games, along with
Remus-GOLD's score against every engine color and Remus-WHITE. Nothing needs to run: the
table is already written.

The Day 9 smoke test plays one game on a short clock only to prove that the color version's
engine plays legal moves to the end; nobody reads its result.

In the games file every player is named `Remus-` and its engine color, such as `Remus-WHITE`, so
the name of a player never reads like the piece color it plays.

### Why the games start from openings

Remus plays the same move every time it sees the same position. Two games between
the same two versions from the starting position would be one game played twice.
Each pair of games therefore starts from one of 32 well-known openings, three moves
deep for each side, such as the Ruy Lopez or the Queen's Gambit, and each version
takes White once. The games file stores the opening in a `StartMoves` header.

## Rank every version: version_league.py

`misc/scripts/version_league.py` is a course designer tool: no student or teacher
runs it in class. Run from the top Remus folder, it plays a round robin: each of the 12 versions
(Remus-WHITE, the ten color versions, and Remus-GOLD) plays each other version 6 times,
396 games in all, or as many times as `--games` asks. Then it fits one Elo rating to every version from every color version
game in the games file, the games of `version_match.py` included, with Remus-WHITE
pinned at 0. Each rating is that version's gain over Remus-WHITE. The league plays
at 10 minutes a side with no increment, because Remus in Python searches too slowly
for shorter games to show what an enhancement adds. `--minutes` and `--increment`
name another clock, and the script rates the games of each clock apart from the
others, since a version that searches deeper can gain more with more time to think.

```bash
uv run misc/scripts/version_league.py --at-once 16   # the round robin, 16 games at a time
uv run misc/scripts/version_league.py --rate-only    # only the ratings, from the saved games
uv run misc/scripts/version_league.py --at-once 16 --event "Station league 2"
                                                # a new league, rated apart from the others
uv run misc/scripts/version_league.py --book-start   # GREEN's and GOLD's games from move 1
```

The six opening moves hand every version a short book, so they hide most of what the
book of Remus-GREEN and Remus-GOLD is worth. With `--book-start`, every game with
GREEN or GOLD starts from the starting position instead. Their book picks among its
moves at random, so their games still differ from each other, while the other pairings
keep the openings. Rate such a league with `--book-start` as well.

The designer's league ran on Niram, Rust copies of all 12 versions that picked the
same moves as Remus about 50 times faster, so a 10-minute Niram game searched about
as many positions as an 8-hour Remus game. Only Niram is kept, in
`engines/Niram` ([`remus-niram parity.md`](remus-niram%20parity.md) shows that the two match), but
the league's games stay in the games file. `--niram --rate-only` rates them apart
from Remus games, with Niram-WHITE pinned at 0, and `version_elo.py --niram` plays
Niram against Stockfish.

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
plays only the games that are not in the games file yet. A 10-minute game lasts
about 16 minutes on average. The course designer's 24-core computer, playing 16 games at a
time, finished about one game a minute, so the whole league took about 7 hours. A
4-core laptop playing 4 games at a time needs about a day.

### The designer's league run

The course designer ran a league of 660 games: every version played every
other version 10 times, 5 times with each piece color, at 10 minutes a side. The league
ran on Niram, the Rust twins of the 12 versions, which choose the same moves as
Remus about 50 times faster. A 10-minute Niram game therefore searches about as deep
as a Remus game of 8 hours, so the table shows what each enhancement adds with
plenty of time to think, deeper than a class laptop reaches in 10 minutes. The 450
games between versions without a book started from the 32 openings. The 210 games
with Remus-GREEN or Remus-GOLD started from the starting position (`--book-start`),
so their book played from move 1. No game ended on time, by a crash, or by an
illegal move.

| Rank | Version | Wins-draws-losses | Score | Elo vs WHITE |
| --- | --- | --- | --- | --- |
| 1 | Remus-GOLD | 79-30-1 | 85.5% | +339 +/- 91 |
| 2 | Remus-RED | 27-71-12 | 56.8% | +101 +/- 67 |
| 3 | Remus-BLUE | 20-74-16 | 51.8% | +67 +/- 67 |
| 4 | Remus-GREEN | 22-67-21 | 50.5% | +58 +/- 66 |
| 5 | Remus-PURPLE | 16-76-18 | 49.1% | +49 +/- 66 |
| 6 | Remus-BROWN | 6-89-15 | 45.9% | +28 +/- 66 |
| 7 | Remus-ORANGE | 8-84-18 | 45.5% | +25 +/- 67 |
| 8 | Remus-PINK | 10-79-21 | 45.0% | +22 +/- 67 |
| 9 | Remus-CYAN | 12-74-24 | 44.5% | +19 +/- 67 |
| 10 | Remus-YELLOW | 14-65-31 | 42.3% | +4 +/- 67 |
| 11 | Remus-GRAY | 10-73-27 | 42.3% | +4 +/- 67 |
| 12 | Remus-WHITE | 7-76-27 | 40.9% | 0 (pinned) |

Each version played 110 games. Remus-YELLOW and Remus-GRAY scored the same 46.5
points; Remus-YELLOW ranks above because it beat Remus-GRAY 5.5 to 4.5. The folder
numbers follow this table, from `01 GRAY` to `10 RED`.

Remus-GOLD, with all ten enhancements, wins most of its games: its +339 plus or minus
91 runs from +248 to +430, and it scored at least 6.5 of 10 against every other
version. Remus-RED, the transposition table, is the only single enhancement whose
range stays above 0, from +34 to +168. Every other color version's range includes 0,
so one of those enhancements alone changes Remus by less than 110 games can measure.
Most games end in a draw (the versions share one evaluation and one search), so each
game moves a rating by little.

The book changes Remus-GREEN's result. In the same league with every game started
from the 32 openings, Remus-GREEN scored 47 of 110 points and rated +7, last among
the color versions. From the starting position it scored 55.5 points and rated +58.
Both ranges overlap, so the gain is likely but not proven. With the openings,
Remus-RED rated +132 and Remus-GOLD +340.

## How big is each version?

The table counts the lines of Python code in each version. A line counts only when
it holds code: comment lines, docstrings, and blank lines do not count. The count
covers only the engine's own `.py` files, the ones `uci_engine.py` loads directly or
through another module when Lucas Chess runs that version. Test files and tools such
as `perft.py`, `play_match.py`, and `show_board.py` do not count.

| Version | Enhancement | Engine files | Code lines | Lines over WHITE |
| --- | --- | --- | --- | --- |
| Remus-WHITE | No enhancements | 12 | 1,040 | 0 |
| Remus-RED | Transposition table | 13 | 1,125 | +85 |
| Remus-GREEN | Opening book | 14 | 1,172 | +132 |
| Remus-BLUE | Killer moves | 12 | 1,092 | +52 |
| Remus-PINK | Principal variation search | 12 | 1,090 | +50 |
| Remus-YELLOW | Draw sense | 12 | 1,082 | +42 |
| Remus-PURPLE | Pawn structure | 12 | 1,077 | +37 |
| Remus-CYAN | Mating bonus | 12 | 1,070 | +30 |
| Remus-ORANGE | Null-move pruning | 12 | 1,119 | +79 |
| Remus-BROWN | Late move reductions | 12 | 1,092 | +52 |
| Remus-GRAY | King safety | 12 | 1,070 | +30 |
| Remus-GOLD | All enhancements | 15 | 1,463 | +423 |

Remus-GOLD holds 423 more code lines than Remus-WHITE. The ten color versions add 589
lines when each one is counted on its own, so GOLD needs 166 fewer. Most color versions
change the same search loop in `search.py`, and GOLD holds one copy of that loop
with all ten ideas inside it. GREEN adds the most lines of any single color version, 132,
because its book reads moves in SAN and so loads `notation.py` as well.

## Puzzle questions

1. Why does every color version play the same opponent instead of each other?
2. The YELLOW color version's whole enhancement is a 2-line function. Why can such a small change still win games?
3. Which color versions change the score Remus finds at a fixed depth, and which only find
   the same score faster?
4. In the designer's league, only Remus-RED among the single color versions measured
   clearly stronger than Remus-WHITE, but Remus-GOLD gained far more. How can ten
   small gains that each hide inside the error bar add up to one gain that shows?
5. Remus-GREEN rated +7 when every game started three moves deep, and +58 when its
   games started from move 1. Why does the start of a game matter so much more to
   GREEN than to RED?
6. Remus-GOLD has every enhancement. Why might it gain less than the ten gains added up?
