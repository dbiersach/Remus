# Remus-GRAY: King safety

While the enemy queen is on the board, reward pawns that shelter the king.

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `king_safety()` in `evaluation.py`.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py GRAY`, which plays Remus-GRAY against Remus-WHITE and adds every game to games/remus_games.pgn.
