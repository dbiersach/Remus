# Enhanced engines: one idea each

## The big picture

Remus-WHITE is the finished Day 9 Remus with none of the enhancements. It already
searches with alpha-beta, quiescence, move ordering, iterative deepening, and a
clock. Ten ideas can make it stronger. On Day 9, in periods 2 and 3, each student pair builds
one of them, so the class can measure which idea adds the most strength. In period 4
the student pairs carry their enhanced engines to each other's laptops and play battles to find
out which enhanced engine is strongest.

Each engine folder carries a color in its name, such as `10 Remus-RED`, instead of a number or
a letter. The color is only a label that tells the folders apart, so no engine sounds
better than another before the games are played.

## Where the enhanced engines live

The Remus versions live in the `engines` folder at the top of the Remus folder, which
holds four folders:

| Folder | Holds |
| --- | --- |
| `engines/instructor` | `00 Remus-WHITE - No enhancements` to `11 Remus-GOLD - All enhancements`, the finished engines, and `12 Remus-PLATINUM - Ten more enhancements`, the course designer's engine with ten more |
| `engines/Niram-GOLD` | Niram-GOLD, Remus-GOLD rewritten in Rust, a course designer's tool |
| `engines/Niram-PLATINUM` | Niram-PLATINUM, Remus-PLATINUM rewritten in Rust, a course designer's tool |
| `engines/student` | `00 Remus-WHITE - No enhancements` to `10 Remus-RED - Transposition table`, with the functions each student pair writes stubbed |

`00 Remus-WHITE - No enhancements` is Remus-WHITE, a copy of the Day 9 `period1`
folder without `show_board.py`, which only the Day 1 and Day 3 lessons run: the Day 9 Remus at the end of period 1, when its engine is finished and before
the student pairs start their enhanced engines. Each engine folder from `01 Remus-GRAY` to
`10 Remus-RED`, such as `10 Remus-RED - Transposition table`, starts as the same engine with one
enhancement added. From period 2 to the end of the day, each student pair works only in
its own engine folder in `engines/student`, so periods 2, 3, and 4 of Day 9 hold no
engine code of their own. No student pair edits `00 Remus-WHITE` after period 1: it stays
plain Remus so every enhancement has something to be measured against. The number in front of each enhanced engine ranks it by its rating
over Remus-WHITE in the designer's 10-minute league (below), from 01 Remus-GRAY to 10 Remus-RED.

`11 Remus-GOLD - All enhancements` is Remus-GOLD, the finished Remus of Day 10 with all ten
enhancements at once. No student pair writes GOLD, so only `engines/instructor` holds
it. `make_version_folders.py` copies Remus-WHITE and builds the ten enhanced engines from
the Day 9 `period1` code and Remus-GOLD.

## Remus Engine Enhancements

| Folder | Enhancement | The idea in one line | The student pair writes | Lines to type |
| --- | --- | --- | --- | --- |
| 01 Remus-GRAY | King safety | Reward pawns that shelter the king while the enemy queen is on the board | `king_safety()` in `evaluation.py` | 24 |
| 02 Remus-YELLOW | Draw sense | Score a repeated position, or one at the fifty-move limit, as 0 inside the search | `is_draw_in_search()` in `search.py`, plus 3 tests in `test_upgrades.py` | 16 |
| 03 Remus-CYAN | Mating bonus | With a big lead, drive the losing king to the edge | `mating_bonus()` in `evaluation.py` | 24 |
| 04 Remus-PINK | Principal variation search | Search the first move with the full window and the rest with a cheap null window | `search_later_move()` in `search.py`, plus 2 tests in `test_upgrades.py` | 18 |
| 05 Remus-ORANGE | Null-move pruning | Let the opponent move twice; if Remus is still too far ahead, the opponent would never allow this position, so stop searching it | `make_null_move()` in `search.py` and `undo_null_move()` in `search.py`, plus 2 tests in `test_upgrades.py` | 23 |
| 06 Remus-BROWN | Late move reductions | Search late, quiet moves one ply shallower, and in full only if they surprise | `reduction()` in `search.py`, plus 2 tests in `test_upgrades.py` | 18 |
| 07 Remus-PURPLE | Pawn structure | Penalize doubled and isolated pawns, reward passed pawns | `pawn_structure()` in `evaluation.py` | 29 |
| 08 Remus-GREEN | Opening book | Play the first moves of well-known openings from a book | `load_book()` in `opening_book.py` and `book_move()` in `opening_book.py` | 26 |
| 09 Remus-BLUE | Killer moves | Try quiet moves that caused a cutoff at the same depth right after the captures | `remember_killer()` in `search.py` and `order_moves()` in `move_ordering.py`, plus 1 test in `test_upgrades.py` | 27 |
| 10 Remus-RED | Transposition table | Remember positions already searched, so one position reached in two move orders is scored once | `store()` in `transposition_table.py` and `probe()` in `transposition_table.py`, plus 1 test in `test_upgrades.py` | 27 |

Every enhanced engine asks for 16 to 29 typed lines, under the 40-line limit for one period. Where the enhancement itself is short, the student pair also writes the tests that prove it works, such as the test that a null window answers only "better or not?", so every student pair spends both periods thinking about its idea rather than waiting.

## Words to know

- **Elo gap:** the rating difference that a match score suggests. A 75 percent
  score means a gap of about +191.
- **yardstick:** Remus-WHITE. Every enhanced engine plays the same opponent, so
  the gaps compare fairly.
- **null window:** a search window one point wide, (alpha, alpha + 1). It answers
  only "better or not?", which takes far less work than an exact score.

## How an enhanced engine search works

Each search enhancement adds one new function to `search.py` beside
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

The evaluation enhancements (PURPLE, CYAN, GRAY) add one term to `evaluate()` and one
line to `explain_evaluation()`. Remus-GREEN asks the book before searching, in
`uci_engine.py`.

## How the ten add up to Remus-GOLD

Remus-GOLD, in `engines/instructor/11 Remus-GOLD - All enhancements`, is Remus-WHITE
with all ten enhancements in one folder. No student pair writes it. It is there to
show how ten ideas that each live alone in an enhanced engine fit together inside one
engine, and it is the engine Day 10 plays in Lucas Chess. Its
[README](<../../engines/instructor/11 Remus-GOLD - All enhancements/README.md>)
measures it against Remus-WHITE.

### Which file each enhancement changes

Six of the ten enhancements change how Remus searches, three change how it scores a
position, and one asks a book before searching at all. Remus-GOLD keeps every file
of Remus-WHITE and changes these:

| File | What Remus-GOLD adds | Enhancement |
| --- | --- | --- |
| `evaluation.py` | `pawn_structure()`, `mating_bonus()`, and `king_safety()`, added into `evaluate()` and printed by `explain_evaluation()` | PURPLE, CYAN, GRAY |
| `transposition_table.py` | `store()`, `probe()`, and `best_stored_move()`, a plain dict from position key to entry | RED |
| `move_ordering.py` | `order_moves()` takes the stored move and this ply's killers | RED, BLUE |
| `opening_book.py` and `opening_book.txt` | `load_book()` and `book_move()` | GREEN |
| `search.py` | `upgraded_search()`, one function with six enhancements inside, and its helpers `is_draw_in_search()`, `null_move_cutoff()`, `search_later_move()`, `reduction()`, and `remember_killer()` | YELLOW, ORANGE, PINK, BROWN, BLUE, RED |
| `uci_engine.py` | Asks `book_move()` before `think()` | GREEN |

In an enhanced engine the new search function sits beside
`alpha_beta_with_quiescence()` under its own name, such as `table_search()`. In
Remus-GOLD all six search changes sit in the one function `upgraded_search()`, and
`think()` calls it. The older functions stay in the file, so a reader can compare
`alpha_beta_with_quiescence()` with `upgraded_search()` line by line and find each
enhancement.

### One move, from Lucas Chess to bestmove

1. Lucas Chess sends `position` and `go`. `uci_engine.py` asks
   `book_move(book, state)` first. When the book knows the position, that move goes
   straight back as `bestmove` and no search runs at all (GREEN).
2. Otherwise `think()` runs iterative deepening: `upgraded_search()` at depth 1,
   then 2, then 3, until the clock runs out, and the move of the last finished depth
   is sent. One `SearchInfo` lives through the whole think, so the transposition
   table and the killer moves filled at depth 3 are already there when depth 4
   starts.
3. At the leaves, `evaluate()` scores the position as the sum of five terms:
   material, placement, pawn structure, the mating bonus, and king safety. The last
   three are PURPLE, CYAN, and GRAY, one function each.

### The order of the steps inside upgraded_search

Each call of `upgraded_search()` looks at one position and runs these steps in this
order. The cheap questions come first, because any one of them can end the call
before the expensive work of generating and searching moves begins:

| Step | What happens | Enhancement |
| --- | --- | --- |
| 1 | Count the position and check the clock | Remus-WHITE |
| 2 | Draw sense: if the position has already appeared in the game or the search, or the fifty-move limit is reached, return 0 | YELLOW |
| 3 | Check extension: in check, look one ply deeper | Remus-WHITE |
| 4 | At depth 0, hand the position to `quiescence()` | Remus-WHITE |
| 5 | Table lookup: if `probe()` finds this position searched at least this deep, return the stored score | RED |
| 6 | Null move: pass the turn and search two plies shallower; if the score still reaches beta, return beta without generating moves. Skipped in check, near mate, and with only pawns left | ORANGE |
| 7 | Generate the legal moves; no moves is mate or stalemate | Remus-WHITE |
| 8 | Order the moves: the stored best move first, then captures by MVV-LVA, then this ply's killers, then the quiet moves | RED, BLUE, Remus-WHITE |
| 9 | Search the first move with the full window | Remus-WHITE |
| 10 | For every later move, `reduction()` cuts one ply from a late quiet move, and `search_later_move()` tries a null window first and searches again in full only when the move beats alpha | BROWN, PINK |
| 11 | On a cutoff, remember the move as a killer for this ply and store the score in the table as a lower bound | BLUE, RED |
| 12 | After the loop, store the score as exact or as an upper bound | RED |

Mate scores depend on the ply they are found at, so steps 11 and 12 leave them out of
the table, and a draw by repetition is tested before the table so that a stored
score never hides a repetition.

### Why the order matters

The enhancements lean on each other. Null-move pruning, principal variation search,
and late move reductions all assume that the first move tried is the best one, or
close to it, and that assumption only holds because the stored move and the killers
have already been put at the front of the list. A reduced or null-window search that
guesses wrong is caught by the full search that follows it, so a wrong guess costs
time but never a move. The table lookup comes before the null move because a dict
read is far cheaper than a shallower search. Draw sense comes before everything else
because a repetition inside the search is the one case where a stored score would
lie.

The strengths do not simply add. The league table below rates each enhanced engine
alone against Remus-WHITE, and Remus-GOLD against all of them, and
[`engines_elo.md`](../designer/engines_elo.md) rates Remus-WHITE and Remus-GOLD
against Stockfish. Two enhancements that each save work can save much of the same
work, and a sharper evaluation changes which moves the search cuts off. The pages in
[`engine_code/`](engine_code/) walk through each file:
[`search.md`](engine_code/search.md) draws the call tree of `upgraded_search()`,
[`evaluation.md`](engine_code/evaluation.md) the five terms, and
[`transposition_table.md`](engine_code/transposition_table.md) the stored entries.

## The Day 9 battles: version_match.py

`version_match.py`, in `misc/designer`, plays an enhanced engine's Remus against Remus-WHITE,
or against another enhanced engine, at 10 minutes a side. It adds every game to
`misc/games/remus_games.pgn` and prints the score.

Nobody types a command to run it. Every engine folder holds two short scripts that
run `version_match.py` for its own engine and pass it the folder that holds that engine folder, so a student pair (or the teacher) opens one in VS
Code and presses the Run Python File button:

| Script | When | What it plays |
| --- | --- | --- |
| `basic_test.py` | Day 9, period 3 | One 2-minute game against Remus-WHITE, to show the engine plays legal moves to the end |
| `play_battle.py` | Day 9, period 4 | A battle: two 10-minute games against a visiting enhanced engine, one with each piece color |

[`engines_elo.md`](../designer/engines_elo.md) explains how the course designer rates every version from these games, with `version_league.py` and against Stockfish.

In the Day 9 battles a visiting student pair brings its engine folder on a USB drive and
copies it over the folder of the same engine color in the host's `engines/student`, which
holds that engine with its functions still stubbed. The
host opens `play_battle.py` in its own engine folder, sets `VISITING_ENGINE` to the
visitor's engine color, such as `"RED"`, and presses Run. The numbered steps at the top
of `play_battle.py` walk through the whole battle. The two engines play twice from the same opening, once with each
piece color, about 20 minutes for both games. Each battle goes on the board as a row of the
class table, and the period has room for two rounds. The visitor's folder stays on the
host laptop when the visitor leaves: it replaces only the stubs of an engine color the host
student pair never writes, and the host's own engine folder is untouched. Two games cannot show which enhancement is
stronger, so the script prints no Elo gap for fewer than 10 games; while round 2
runs, each student pair puts its round 1 score into `demo_results.py` and sees how wide the
margin of error is. The teacher then shows the league table in
[`engines_elo.md`](../designer/engines_elo.md), which rates every Remus version from 110 games.
Nothing needs to run: the table is already written.

The Day 9 basic test plays one game on a short clock only to prove that the enhanced engine's
engine plays legal moves to the end; nobody reads its result.

In the games file every player is named `Remus-` and its engine color, such as `Remus-WHITE`, so
the name of a player never reads like the piece color it plays.

### Why the games start from openings

Remus plays the same move every time it sees the same position. Two games between
the same two versions from the starting position would be one game played twice.
Each pair of games therefore starts from one of 32 well-known openings, three moves
deep for each side, such as the Ruy Lopez or the Queen's Gambit, and each version
takes White once. The games file stores the opening in a `StartMoves` header.

## The league table

The teacher shows this table at the end of the Day 9 battles. The course designer ran a league of 660 games: every version played every
other version 10 times, 5 times with each piece color, at 10 minutes a side. The league
ran on Niram, the Rust twins of the 12 versions, which choose the same moves as
Remus about 15 times faster. A 10-minute Niram game therefore searches about as deep
as a Remus game of 2.5 hours, so the table shows what each enhancement adds with
plenty of time to think, deeper than a class laptop reaches in 10 minutes. The 450
games between versions without a book started from the 32 openings. The 210 games
with Remus-GREEN or Remus-GOLD started from the starting position (`--book-start`),
so their book played from move 1. No game ended on time, by a crash, or by an
illegal move.

| Rank | Version | Wins-draws-losses | Score | Elo vs WHITE |
| --- | --- | --- | --- | --- |
| 1 | Remus-GOLD | 79-30-1 | 85.5% | +339 +/- 91 |
| 2 | Remus-RED | 27-71-12 | 56.8% | +101 +/- 67 |
| 3 | Remus-BLUE | 20-74-16 | 51.8% | +67 +/- 66 |
| 4 | Remus-GREEN | 22-67-21 | 50.5% | +58 +/- 66 |
| 5 | Remus-PURPLE | 16-76-18 | 49.1% | +49 +/- 66 |
| 6 | Remus-BROWN | 6-89-15 | 45.9% | +28 +/- 66 |
| 7 | Remus-ORANGE | 8-84-18 | 45.5% | +25 +/- 66 |
| 8 | Remus-PINK | 10-79-21 | 45.0% | +22 +/- 67 |
| 9 | Remus-CYAN | 12-74-24 | 44.5% | +19 +/- 67 |
| 10 | Remus-YELLOW | 14-65-31 | 42.3% | +4 +/- 67 |
| 11 | Remus-GRAY | 10-73-27 | 42.3% | +4 +/- 67 |
| 12 | Remus-WHITE | 7-76-27 | 40.9% | 0 (pinned) |

Each version played 110 games. Remus-YELLOW and Remus-GRAY scored the same 46.5
points; Remus-YELLOW ranks above because it beat Remus-GRAY 5.5 to 4.5. The folder
numbers follow this table, from `01 Remus-GRAY` to `10 Remus-RED`.

Remus-GOLD, with all ten enhancements, wins most of its games: its +339 plus or minus
91 runs from +248 to +430, and it scored at least 6.5 of 10 against every other
version. Remus-RED, the transposition table, is the clearest gain from one enhancement,
with a range from +34 to +168. Remus-BLUE, the killer moves, clears 0 only just: its
range runs from +0.6 to +133.6. Every other enhanced engine's range includes 0, so one
of those enhancements alone changes Remus by less than 110 games can measure.
Most games end in a draw (the versions share one evaluation and one search), so each
game moves a rating by little.

The book changes Remus-GREEN's result. In the same league with every game started
from the 32 openings, Remus-GREEN scored 47 of 110 points and rated +7, last among
the enhanced engines. From the starting position it scored 55.5 points and rated +58.
Both ranges overlap, so the gain is likely but not proven. With the openings,
Remus-RED rated +132 and Remus-GOLD +340.

## Puzzle questions

1. Why does every enhanced engine play the same opponent instead of each other?
2. Remus-YELLOW's whole enhancement is a 2-line function. Why can such a small change still win games?
3. Which enhanced engines change the score Remus finds at a fixed depth, and which only find
   the same score faster?
4. In the designer's league, only Remus-RED and, just barely, Remus-BLUE among the engines
   with one enhancement measured stronger than Remus-WHITE, but Remus-GOLD gained far more. How can ten
   small gains that each hide inside the error bar add up to one gain that shows?
5. Remus-GREEN rated +7 when every game started three moves deep, and +58 when its
   games started from move 1. Why does the start of a game matter so much more to
   GREEN than to RED?
6. Remus-GOLD has every enhancement. Why might it gain less than the ten gains added up?
