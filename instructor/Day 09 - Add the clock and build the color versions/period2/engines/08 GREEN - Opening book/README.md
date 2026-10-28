# Remus-GREEN: Opening book

Play the first moves of well-known openings from a book instead of searching.

## Learning objectives

By the end of Day 9, each pair can:

- Explain the idea of the color version's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the version folder.
- Run a fair experiment against Remus-WHITE: same opening, both colors. **Measured by:** In the Day 10 tournament, `play_tournament.py` in the version folder plays both 10-minute games with no illegal moves or crashes when the pair presses Run in VS Code, and the pair says why two games cannot show whether the enhancement helps.

## The idea, with an example

`opening_book.txt` holds 43 well-known openings, five moves for each side, written in SAN: `e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7` is the Ruy Lopez. `load_book()` plays every line on a board from the starting position and records, for each position it passes, which moves the book plays there. After 1. e4 the book holds seven replies: ...e5, ...c5, ...e6, ...c6, ...d5, ...d6, and ...Nf6. `book_move()` picks one of them at random, so Remus-GREEN does not play the same opening every game. Once the game leaves the book, Remus searches as usual.

## Why it makes Remus stronger

Searching the opening is slow and not very good: at depth 4 Remus cannot see why 1. e4 e5 2. Nf3 Nc6 3. Bb5 works. A book move costs no thinking time and comes from a century of human play. Every book move also passes through `parse_san()` and Remus's own legal move generator, so a typo in the book file is reported and skipped, never played.

## What it costs

Nothing during the search: the book is read once when the engine starts, and asking it is one dict lookup. Positions per second and positions per depth are the same as Remus-WHITE's, because the search itself does not change.

## Measured against Remus-WHITE

Each version searched the ten positions of `compare_search.py`, one depth at a time up to depth 4, on one computer. Fewer positions for the same depth means a smaller search tree. Positions per second shows what each position costs. The last column gave each position 5 seconds, the way a game does, and averages the deepest search that finished.

| Version | Positions to finish depth 4 | Share of Remus-WHITE's | Positions per second | Average depth in 5 seconds |
| --- | ---: | ---: | ---: | ---: |
| Remus-WHITE | 431,212 | 100% | 5,183 | 3.1 |
| Remus-GREEN | 431,212 | 100% | 5,049 | 3.2 |

## What to expect

The time saved goes to later moves. Remus thinks about one thirtieth of its remaining clock per move, so five instant book moves leave roughly a minute and a half more for the middlegame. Every version match game starts from one of 32 openings three moves deep, and 24 of those positions are in the book, so Remus-GREEN usually gets two more instant moves before it searches. The book saves the most time in games that start from the first move. In the teacher's league, Remus-GREEN rated +7 over Remus-WHITE when its games started three moves deep, and +58 when they started from the first move. The benchmark below never asks the book, so its numbers match Remus-WHITE's exactly.

## Where your code fits

`uci_engine.py` and `console_game.py` ask `book_move()` before they search. `None` means the position is not in the book, and the engine calls `think()` as Remus-WHITE does.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus in the `period2` folder above, plus this one enhancement. The pair writes `load_book()` in `opening_book.py`, `book_move()` in `opening_book.py`.

## The changes and why

### `load_book()` in `opening_book.py`

Reads the book file line by line, checks every SAN move with Remus's own rules, and stores the moves by position. A missing file or a typo only prints a note, so a bad book never stops Remus from playing.

### `book_move()` in `opening_book.py`

Looks the position up in the book and picks one of its moves at random, or returns None when the game has left the book. The random pick keeps Remus from playing the same opening every game.

## Check it

Check the work from inside this folder with `uv run pytest`. Then open `smoke_test.py` in VS Code and press Run: Remus-GREEN plays one 2-minute game against Remus-WHITE, which shows that the engine plays legal moves to the end of a game. In the Day 9 battles, copy the visiting pair's color folder into the `engines` folder, open `play_battle.py`, press Run, and type the visitor's color: Remus-GREEN plays it twice at 10 minutes a side, once with each color. In the Day 10 tournament, open `play_tournament.py` and press Run: Remus-GREEN plays Remus-WHITE twice, once with each color, at 10 minutes a side, and both games go into games/remus_games.pgn. Each script runs `version_match.py` from the `engines` folder above this one.
