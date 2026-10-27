# Remus-YELLOW: Draw sense

Score a repeated position, or one at the fifty-move limit, as a draw inside the search.

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `is_draw_in_search()` in `search.py`.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py YELLOW`, which plays Remus-YELLOW against Remus-WHITE and adds every game to games/remus_games.pgn.
