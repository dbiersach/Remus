# YELLOW station: Draw sense

Score a repeated position, or one at the fifty-move limit, as a draw inside the search.

This folder is the plain Day 9 Remus plus this one enhancement. The pair writes `is_draw_in_search()` in `search.py`.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py "YELLOW - Draw sense"`, which plays this Remus against the plain Day 9 Remus and adds every game to games/remus_games.pgn.
