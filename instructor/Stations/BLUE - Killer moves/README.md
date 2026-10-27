# Remus-BLUE: Killer moves

Try quiet moves that caused a cutoff at the same depth right after the captures.

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `remember_killer()` in `search.py`.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py BLUE`, which plays Remus-BLUE against Remus-WHITE and adds every game to games/remus_games.pgn.
