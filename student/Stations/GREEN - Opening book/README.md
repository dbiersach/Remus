# Remus-GREEN: Opening book

Play the first moves of well-known openings from a book instead of searching.

## Learning objectives

By the end of the station, each pair can:

- Explain the idea of the station's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the station folder.
- Measure the enhancement against Remus-WHITE. **Measured by:** `uv run station_match.py <COLOR>` finishes, and the pair reads its Elo gap and margin from the output.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `load_book()` in `opening_book.py`, `book_move()` in `opening_book.py`.

## The changes and why

### `load_book()` in `opening_book.py`

Reads the book file line by line, checks every SAN move with Remus's own rules, and stores the moves by position. A missing file or a typo only prints a note, so a bad book never stops Remus from playing.

### `book_move()` in `opening_book.py`

Looks the position up in the book and picks one of its moves at random, or returns None when the game has left the book. The random pick keeps Remus from playing the same opening every game.

Check the work from inside this folder with `uv run pytest`. Then measure the gain from the Stations folder with `uv run station_match.py GREEN`, which plays Remus-GREEN against Remus-WHITE and adds every game to games/remus_games.pgn.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `opening_book.py` | `load_book()` | 31 | 22 | `test_upgrades.py::test_opening_book_is_legal_and_answers_e4`, `test_upgrades.py::test_book_typo_is_skipped_without_touching_stdout`, `test_upgrades.py::test_missing_book_never_stops_play` |
| `opening_book.py` | `book_move()` | 51 | 2 | `test_upgrades.py::test_opening_book_is_legal_and_answers_e4`, `test_upgrades.py::test_missing_book_never_stops_play` |

Lines to type in all: 24. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` line. Delete those three lines and write the body in their place.
