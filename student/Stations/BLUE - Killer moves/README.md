# BLUE station: Killer moves

Try quiet moves that caused a cutoff at the same depth right after the captures.

This folder is the plain Day 9 Remus plus this one enhancement. The pair writes `remember_killer()` in `search.py`.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py "BLUE - Killer moves"`, which plays this Remus against the plain Day 9 Remus and adds every game to games/remus_games.pgn.
