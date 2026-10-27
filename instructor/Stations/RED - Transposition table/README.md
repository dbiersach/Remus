# RED station: Transposition table

Remember positions already searched, so the same position reached in two move orders is scored once.

This folder is the plain Day 9 Remus plus this one enhancement. The pair writes `probe()` in `transposition_table.py`.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py "RED - Transposition table"`, which plays this Remus against the plain Day 9 Remus and adds every game to games/remus_games.pgn.
