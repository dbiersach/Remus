# Remus-GREEN: Opening book

Play the first moves of well-known openings from a book instead of searching.

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `load_book()` in `opening_book.py`.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py GREEN`, which plays Remus-GREEN against Remus-WHITE and adds every game to games/remus_games.pgn.
