# Remus-YELLOW: Draw sense

Score a repeated position, or one at the fifty-move limit, as a draw inside the search.

## Learning objectives

By the end of Day 9, each student pair can:

- Explain the idea of this enhancement in two sentences. **Measured by:** The student pair explains the idea to another student pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `run_tests.py` passes in the version folder.
- Run a fair experiment: same opening, both piece colors. **Measured by:** In the Day 9 battles, `play_battle.py` in the version folder plays both 10-minute games with no illegal moves or crashes when the student pair presses Run in VS Code, and the student pair says why two games cannot show which enhancement is stronger.

## The idea, with an example

Remus-WHITE is a rook behind, and the opponent's king can be checked forever. Inside its search, Remus-WHITE scores the position after the third repetition as a rook behind, because nothing in its search knows that the game ends there as a draw. So it avoids the checks and loses slowly. Remus-YELLOW scores any position that already appeared in the game or in the search line as 0, a draw, and so does a position after 100 half moves with no capture or pawn move (the fifty-move rule). It sees that the checks save half a point and plays them.

## Why it makes Remus stronger

The same knowledge works the other way. A side that is ahead stops repeating positions, because a repetition scores 0 instead of its +300 lead. A repetition can only be claimed after the third time, but the search treats the second time as a draw: if repeating once is the best either side can do, it can repeat again.

## What it costs

`is_draw_in_search()` counts the position key in the game history at every position, a short list scan. Positions per second stay close to Remus-WHITE's, and the search saves work when it meets a repetition, because a draw ends that line at once.

## Measured against Remus-WHITE

Each version searched the ten positions of `compare_search.py`, one depth at a time up to depth 4, on one computer. Fewer positions for the same depth means a smaller search tree. Positions per second shows what each position costs. The last column gave each position 5 seconds, the way a game does, and averages the deepest search that finished.

| Version | Positions to finish depth 4 | Share of Remus-WHITE's | Positions per second | Average depth in 5 seconds |
| --- | ---: | ---: | ---: | ---: |
| Remus-WHITE | 431,212 | 100% | 5,183 | 3.1 |
| Remus-YELLOW | 431,138 | 100% | 5,048 | 3.1 |

## What to expect

More draws in lost positions and fewer accidental draws in won ones. The benchmark positions below start with no game history, so they hold almost no repetitions and the numbers match Remus-WHITE's; the difference shows up in games.

## Where your code fits

`draw_sense_search()` in `search.py` calls `is_draw_in_search()` at the top of every position below the root, before any move is generated. The root is skipped, because Remus must still choose a move there.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus in `00 WHITE - No enhancements` beside it, plus this one enhancement. The student pair writes `is_draw_in_search()` in `search.py`, `test_draw_sense_search_agrees_with_alpha_beta()` in `test_upgrades.py`, `test_a_repeated_position_is_a_draw()` in `test_upgrades.py`, `test_the_fifty_move_limit_is_a_draw()` in `test_upgrades.py`.

## The changes and why

### `is_draw_in_search()` in `search.py`

Says a position is a draw when it already appeared earlier in the game or the search, or when the fifty-move limit is reached. Then Remus aims for a repetition when losing and avoids one when winning.

### `test_draw_sense_search_agrees_with_alpha_beta()` in `test_upgrades.py`

In a position with no repetition, draw sense must change nothing, so the version search and the Day 9 search must find the same score.

### `test_a_repeated_position_is_a_draw()` in `test_upgrades.py`

Plays Nf3 Nf6 Ng1 Ng8, which brings back the starting position, and checks that `is_draw_in_search()` says draw only after the knights come home.

### `test_the_fifty_move_limit_is_a_draw()` in `test_upgrades.py`

Loads a FEN whose halfmove clock is 100 and checks that it counts as a draw. The FEN carries the clock, so no game needs to be played.

## Check it

Check the work by opening `run_tests.py` in this folder and pressing Run. Then open `smoke_test.py` in VS Code and press Run: Remus-YELLOW plays one 2-minute game against Remus-WHITE, which shows that the engine plays legal moves to the end of a game. In the Day 9 battles, follow the numbered steps at the top of `play_battle.py`: copy the visiting student pair's engine folder into `engines/student`, set `VISITING_ENGINE` to the visitor's engine color, and press Run. Remus-YELLOW plays it twice at 10 minutes a side, once with each piece color, and both games go into misc/games/remus_games.pgn. Each script runs `version_match.py` from the folder above this one.
