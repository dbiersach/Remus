# Remus-YELLOW: Draw sense

Score a repeated position, or one at the fifty-move limit, as a draw inside the search.

## Learning objectives

By the end of the station, each pair can:

- Explain the idea of the station's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the station folder.
- Measure the enhancement against Remus-WHITE. **Measured by:** `uv run station_match.py <COLOR>` finishes, and the pair reads its Elo gap and margin from the output.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `is_draw_in_search()` in `search.py`.

## The changes and why

### `is_draw_in_search()` in `search.py`

Says a position is a draw when it already appeared earlier in the game or the search, or when the fifty-move limit is reached. Then Remus aims for a repetition when losing and avoids one when winning.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py YELLOW`, which plays Remus-YELLOW against Remus-WHITE and adds every game to games/remus_games.pgn.
