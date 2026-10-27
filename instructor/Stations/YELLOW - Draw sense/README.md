# Remus-YELLOW: Draw sense

Score a repeated position, or one at the fifty-move limit, as a draw inside the search.

## Learning objectives

By the end of the station, each pair can:

- Explain the idea of the station's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the station folder.
- Measure the enhancement against Remus-WHITE. **Measured by:** `uv run station_match.py <COLOR>` finishes, and the pair reads its Elo gap and margin from the output.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `is_draw_in_search()` in `search.py`, `test_draw_sense_search_agrees_with_alpha_beta()` in `test_upgrades.py`, `test_a_repeated_position_is_a_draw()` in `test_upgrades.py`, `test_the_fifty_move_limit_is_a_draw()` in `test_upgrades.py`.

## The changes and why

### `is_draw_in_search()` in `search.py`

Says a position is a draw when it already appeared earlier in the game or the search, or when the fifty-move limit is reached. Then Remus aims for a repetition when losing and avoids one when winning.

### `test_draw_sense_search_agrees_with_alpha_beta()` in `test_upgrades.py`

In a position with no repetition, draw sense must change nothing, so the station search and the Day 9 search must find the same score.

### `test_a_repeated_position_is_a_draw()` in `test_upgrades.py`

Plays Nf3 Nf6 Ng1 Ng8, which brings back the starting position, and checks that `is_draw_in_search()` says draw only after the knights come home.

### `test_the_fifty_move_limit_is_a_draw()` in `test_upgrades.py`

Loads a FEN whose halfmove clock is 100 and checks that it counts as a draw. The FEN carries the clock, so no game needs to be played.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py YELLOW`, which plays Remus-YELLOW against Remus-WHITE and adds every game to games/remus_games.pgn.
