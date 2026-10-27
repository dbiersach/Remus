# GREEN station: Opening book

Play the first moves of well-known openings from a book instead of searching.

This folder is the plain Day 9 Remus plus this one enhancement. The pair writes `load_book()` in `opening_book.py`.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py "GREEN - Opening book"`, which plays this Remus against the plain Day 9 Remus and adds every game to games/remus_games.pgn.
