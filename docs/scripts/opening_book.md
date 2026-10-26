# opening_book.py

Plays the first moves from a list of known openings.

First appears in `Day 10 - Upgrade Remus and add Science AI`.

## What it does

`opening_book.txt` holds one opening per line in SAN, such as
`e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7`. While a game follows a book line, Remus
plays a book move at once instead of searching.

## Data structure

The book is a dict from `position_key` to a list of moves: 97 positions from 13
lines. After 1. e4, the list holds e5, c5, e6, and c6.

## Program flow

`load_book` replays every line from the start position with `parse_san`, so every book
move is checked by Remus's own move generator; a typo is reported and the rest of
that line is skipped. A missing file gives an empty book. `book_move` returns a
random book move, or `None`, and `uci_engine.py` then searches as usual.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `load_book` | 10 | Read an opening book file into a dict from position key to book moves. |
| `book_move` | 10 | Return a random book move for this position, or None when out of book. |

## Try it

From inside a Day folder that has the file:

```bash
uv run opening_book.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 10.8.
