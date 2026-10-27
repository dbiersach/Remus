# Remus-PINK: Principal variation search

Search the first move with the full window and every other move with a cheap null window first.

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `search_later_move()` in `search.py`.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py PINK`, which plays Remus-PINK against Remus-WHITE and adds every game to games/remus_games.pgn.
