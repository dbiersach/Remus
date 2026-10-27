# Enhancement stations: one color, one idea

## The big picture

Remus-WHITE is the finished Day 9 Remus with none of the enhancements. It already
searches with alpha-beta, quiescence, move ordering, iterative deepening, and a
clock. Ten ideas can make it stronger. Each pair builds
one of them, so the class can measure which idea adds the most strength.

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
| RED | Transposition table | Remember positions already searched, so one position reached in two move orders is scored once | `probe()` in `transposition_table.py` | 11 |
| GREEN | Opening book | Play the first moves of well-known openings from a book | `load_book()` in `opening_book.py` | 22 |
| BLUE | Killer moves | Try quiet moves that caused a cutoff at the same depth right after the captures | `remember_killer()` in `search.py` | 6 |
| PINK | Principal variation search | Search the first move with the full window and the rest with a cheap null window | `search_later_move()` in `search.py` | 6 |
| YELLOW | Draw sense | Score a repeated position, or one at the fifty-move limit, as 0 inside the search | `is_draw_in_search()` in `search.py` | 2 |
| PURPLE | Pawn structure | Penalize doubled and isolated pawns, reward passed pawns | `pawn_structure()` in `evaluation.py` | 30 |
| CYAN | Mating bonus | With a big lead, drive the losing king to the edge | `mating_bonus()` in `evaluation.py` | 24 |
| ORANGE | Null-move pruning | If passing the turn still wins in a shallow search, a real move will too | `make_null_move()` and `undo_null_move()` in `search.py` | 8 |
| BROWN | Late move reductions | Search late, quiet moves one ply shallower, and in full only if they surprise | `reduction()` in `search.py` | 3 |
| GRAY | King safety | Reward pawns that shelter the king while the enemy queen is on the board | `king_safety()` in `evaluation.py` | 20 |

Every station stays under the 40-line limit for one period.

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

Twenty games take about an hour with two games at once. Nobody needs to watch, so
every laptop runs its own color against Remus-WHITE at the same time. Remus-WHITE
also plays in the color-on-color matches, to show how far each station climbs above
its starting point. In the games file every player is named `Remus-<COLOR>`, such as
`Remus-WHITE`, so a player name never reads like the side to move.

## Puzzle questions

1. Why does every station play the same opponent instead of each other?
2. The YELLOW station types only 2 lines. Why can such a small change still win games?
3. Which stations change the score Remus finds at a fixed depth, and which only find
   the same score faster?
