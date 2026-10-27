# PURPLE station: Pawn structure

Penalize doubled and isolated pawns and reward passed pawns.

This folder is the plain Day 9 Remus plus this one enhancement. The pair writes `pawn_structure()` in `evaluation.py`.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py "PURPLE - Pawn structure"`, which plays this Remus against the plain Day 9 Remus and adds every game to games/remus_games.pgn.
