# Enhancement stations: one color, one idea

## The big picture

Remus-WHITE is the finished Day 9 Remus with none of the enhancements. It already
searches with alpha-beta, quiescence, move ordering, iterative deepening, and a
clock. Ten ideas can make it stronger. On Day 9, in periods 2 and 3, each pair builds
one of them, so the class can measure which idea adds the most strength. In period 4
every pair starts its matches, which run with nobody watching while the pairs write
the mate solver.

Each station has a color instead of a number or a letter, so no station sounds
better than another before the games are played.

## Where the stations live

`instructor/Stations` holds `WHITE - No enhancements` and one folder per station,
such as `RED - Transposition table`. The WHITE folder is a complete, runnable copy of
the finished Day 9 Remus (`instructor/Day 09 .../period4`), and each station folder is
that copy plus one enhancement. `student/Stations`
holds the same folders with the pair's functions stubbed.

`make_station_folders.py` builds the folders from the Day 9 and Day 10 code.
`GOLD - All enhancements` holds Remus-GOLD, a copy of the finished Day 10 Remus with
all ten enhancements at once. Remus-GOLD stays out of the color matches;
`uv run estimate_elo.py` inside its folder rates it against Stockfish.

## The ten stations

| Color | Enhancement | The idea in one line | The pair writes | Lines to type |
| --- | --- | --- | --- | --- |
| RED | Transposition table | Remember positions already searched, so one position reached in two move orders is scored once | `store()` in `transposition_table.py` and `probe()` in `transposition_table.py`, plus 1 test in `test_upgrades.py` | 27 |
| GREEN | Opening book | Play the first moves of well-known openings from a book | `load_book()` in `opening_book.py` and `book_move()` in `opening_book.py` | 24 |
| BLUE | Killer moves | Try quiet moves that caused a cutoff at the same depth right after the captures | `remember_killer()` in `search.py` and `order_moves()` in `move_ordering.py`, plus 1 test in `test_upgrades.py` | 22 |
| PINK | Principal variation search | Search the first move with the full window and the rest with a cheap null window | `search_later_move()` in `search.py`, plus 2 tests in `test_upgrades.py` | 18 |
| YELLOW | Draw sense | Score a repeated position, or one at the fifty-move limit, as 0 inside the search | `is_draw_in_search()` in `search.py`, plus 3 tests in `test_upgrades.py` | 16 |
| PURPLE | Pawn structure | Penalize doubled and isolated pawns, reward passed pawns | `pawn_structure()` in `evaluation.py` | 30 |
| CYAN | Mating bonus | With a big lead, drive the losing king to the edge | `mating_bonus()` in `evaluation.py` | 24 |
| ORANGE | Null-move pruning | If passing the turn still wins in a shallow search, a real move will too | `make_null_move()` in `search.py` and `undo_null_move()` in `search.py`, plus 2 tests in `test_upgrades.py` | 23 |
| BROWN | Late move reductions | Search late, quiet moves one ply shallower, and in full only if they surprise | `reduction()` in `search.py`, plus 2 tests in `test_upgrades.py` | 18 |
| GRAY | King safety | Reward pawns that shelter the king while the enemy queen is on the board | `king_safety()` in `evaluation.py` | 20 |

Every station asks for 16 to 30 typed lines, under the 40-line limit for one period. Where the enhancement itself is short, the pair also writes the tests that prove it works, such as the test that a null window answers only "better or not?", so every pair spends the station thinking about its idea rather than waiting.

## Words to know

- **Elo gap:** the rating difference that a match score suggests. A 75 percent
  score means a gap of about +191.
- **yardstick:** Remus-WHITE. Every station plays the same opponent, so
  the gaps compare fairly.
- **null window:** a search window one point wide, (alpha, alpha + 1). It answers
  only "better or not?", which takes far less work than an exact score.

## How a station search works

Each search station adds one new function to `search.py` beside
`alpha_beta_with_quiescence`, and `think()` calls the new function. The new function
is the Day 9 search with one change, so a pair can compare the two side by side:

| Color | New search function | What changes |
| --- | --- | --- |
| RED | `table_search` | Look up the position before searching; store the result after |
| BLUE | `killer_search` | Pass this ply's killers to `order_moves()`; remember a quiet move that cuts off |
| PINK | `pvs_search` | Search every move after the first with `search_later_move()` |
| YELLOW | `draw_sense_search` | Return 0 at once when `is_draw_in_search()` says so |
| ORANGE | `null_move_search` | Before the moves, try a pass with a search 2 plies shallower |
| BROWN | `reduced_search` | Cut one ply from late, quiet moves; search again in full on a surprise |

The evaluation stations (PURPLE, CYAN, GRAY) add one term to `evaluate()` and one
line to `explain_evaluation()`. The GREEN station asks the book before searching, in
both `uci_engine.py` and `console_game.py`.

## Measure the gain: station_match.py

`instructor/Stations/station_match.py` plays a station's Remus against Remus-WHITE,
or against another station, at 1 minute plus 0.6 seconds a move. It adds
every game to `games/remus_games.pgn` and prints the score and the Elo gap.

```bash
uv run station_match.py RED            # Remus-RED against Remus-WHITE, 20 games
uv run station_match.py RED BLUE       # Remus-RED against Remus-BLUE
```

Twenty games take about 20 to 30 minutes with two games at once: each game lasts
about two minutes, because each side has 1 minute plus 0.6 seconds a move. Nobody needs to watch, so
every laptop runs its own color against Remus-WHITE at the same time. Remus-WHITE
also plays in the color-on-color matches, to show how far each station climbs above
its starting point. In the games file every player is named `Remus-<COLOR>`, such as
`Remus-WHITE`, so a player name never reads like the side to move.

### Why the games start from openings

Remus plays the same move every time it sees the same position. Two games between
the same two versions from the starting position would be one game played twice.
Each pair of games therefore starts from one of 32 well-known openings, three moves
deep for each side, such as the Ruy Lopez or the Queen's Gambit, and each version
takes White once. The games file stores the opening in a `StartMoves` header.

## Rank every version: station_league.py

`instructor/Stations/station_league.py` plays a round robin: each of the 12 versions
(Remus-WHITE, the ten stations, and Remus-GOLD) plays each other version 6 times,
396 games in all. Then it fits one Elo rating to every version from every station
game in the games file, the games of `station_match.py` included, with Remus-WHITE
pinned at 0. Each rating is that version's gain over Remus-WHITE. The league plays
at 1 minute plus 0.6 seconds a move unless `--minutes` and `--increment` name another
clock, and it rates the games of each clock apart from the others, since a version
that searches deeper can gain more with more time to think.

```bash
uv run station_league.py                # the round robin, then the ratings
uv run station_league.py --rate-only    # only the ratings, from the saved games
uv run station_league.py --minutes 10 --increment 0 --at-once 16
                                        # 10-minute games, 16 at a time
```

The fit works like `estimate_elo.py`: it moves each rating until the points the Elo
formula expects for a version equal the points it really scored. One pretend draw
against Remus-WHITE keeps a perfect score from giving an endless rating. A rating
of +60 plus or minus 80 means the true gain most likely lies between -20 and +140,
so two versions whose ranges overlap have not been told apart yet.

The league can stop partway, such as when a laptop restarts. Run it again and it
plays only the games that are not in the games file yet. With one game per processor
core, a 4-core computer plays about 2 games a minute, so the whole league takes
about 3 hours and 20 minutes.

### The teacher's league run

The teacher's run of all 396 games (October 2026) gave these ratings:

| Rank | Version | Score | Elo vs WHITE |
| --- | --- | --- | --- |
| 1 | Remus-GOLD | 65.2% | +99 +/- 87 |
| 2 | Remus-PURPLE | 55.3% | +34 +/- 84 |
| 3 | Remus-YELLOW | 53.8% | +24 +/- 84 |
| 4 | Remus-ORANGE | 51.5% | +10 +/- 84 |
| 5 | Remus-RED | 50.0% | +0 +/- 84 |
| 6 | Remus-WHITE | 50.0% | 0 (pinned) |
| 7 | Remus-BLUE | 49.2% | -5 +/- 84 |
| 8 | Remus-BROWN | 47.7% | -14 +/- 84 |
| 9 | Remus-PINK | 44.7% | -34 +/- 84 |
| 10 | Remus-GRAY | 44.7% | -34 +/- 84 |
| 11 | Remus-GREEN | 43.9% | -39 +/- 84 |
| 12 | Remus-CYAN | 43.9% | -39 +/- 84 |

Only Remus-GOLD, with all ten enhancements, has a range that stays above 0, and only
just: +99 plus or minus 87 runs from +12 to +186. Every single station's range
includes 0, so one enhancement alone changes Remus by less than 66 games can measure
at 1 minute a game.

## How big is each version?

The table counts the lines of Python code in each version. A line counts only when
it holds code: comment lines, docstrings, and blank lines do not count. The count
covers only the engine's own `.py` files, the ones `uci_engine.py` loads directly or
through another module when Lucas Chess runs that version. Test files and tools such
as `perft.py`, `play_match.py`, and `show_board.py` do not count, and neither do the
Day 10 science files in the GOLD folder.

| Version | Enhancement | Engine files | Code lines | Lines over WHITE |
| --- | --- | --- | --- | --- |
| Remus-WHITE | No enhancements | 12 | 1,107 | 0 |
| Remus-RED | Transposition table | 13 | 1,192 | +85 |
| Remus-GREEN | Opening book | 14 | 1,226 | +119 |
| Remus-BLUE | Killer moves | 12 | 1,164 | +57 |
| Remus-PINK | Principal variation search | 12 | 1,157 | +50 |
| Remus-YELLOW | Draw sense | 12 | 1,149 | +42 |
| Remus-PURPLE | Pawn structure | 12 | 1,145 | +38 |
| Remus-CYAN | Mating bonus | 12 | 1,137 | +30 |
| Remus-ORANGE | Null-move pruning | 12 | 1,182 | +75 |
| Remus-BROWN | Late move reductions | 12 | 1,159 | +52 |
| Remus-GRAY | King safety | 12 | 1,133 | +26 |
| Remus-GOLD | All enhancements | 15 | 1,509 | +402 |

Remus-GOLD holds 402 more code lines than Remus-WHITE. The ten stations add 574
lines when each one is counted on its own, so GOLD needs 172 fewer. Most stations
change the same search loop in `search.py`, and GOLD holds one copy of that loop
with all ten ideas inside it. GREEN adds the most lines of any single station, 119,
because its book reads moves in SAN and so loads `notation.py` as well.

## Puzzle questions

1. Why does every station play the same opponent instead of each other?
2. The YELLOW station's whole enhancement is a 2-line function. Why can such a small change still win games?
3. Which stations change the score Remus finds at a fixed depth, and which only find
   the same score faster?
4. In the teacher's league, no single station measured clearly stronger than
   Remus-WHITE, but Remus-GOLD did. How can ten small gains that each hide inside the
   error bar add up to one gain that shows?
4. Remus-GOLD has every enhancement. Why might it gain less than the ten gains added up?
