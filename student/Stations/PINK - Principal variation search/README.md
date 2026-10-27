# PINK station: Principal variation search

Search the first move with the full window and every other move with a cheap null window first.

This folder is the plain Day 9 Remus plus this one enhancement. The pair writes `search_later_move()` in `search.py`.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py "PINK - Principal variation search"`, which plays this Remus against the plain Day 9 Remus and adds every game to games/remus_games.pgn.
