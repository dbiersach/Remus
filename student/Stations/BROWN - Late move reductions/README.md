# BROWN station: Late move reductions

Search late, quiet moves one ply shallower, and in full only if they surprise.

This folder is the plain Day 9 Remus plus this one enhancement. The pair writes `reduction()` in `search.py`.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py "BROWN - Late move reductions"`, which plays this Remus against the plain Day 9 Remus and adds every game to games/remus_games.pgn.
