# ORANGE station: Null-move pruning

Pass the turn in a shallow search: if passing still wins, a real move will too, so stop early.

This folder is the plain Day 9 Remus plus this one enhancement. The pair writes `make_null_move()` in `search.py`, `undo_null_move()` in `search.py`.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py "ORANGE - Null-move pruning"`, which plays this Remus against the plain Day 9 Remus and adds every game to games/remus_games.pgn.
