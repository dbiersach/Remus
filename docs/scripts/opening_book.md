# opening_book.py: Play known openings without thinking

*First appears in `instructor/Day 10 - Upgrade Remus and add Science AI`.*

## The big picture

Strong players know the first few moves of popular openings by heart. Remus can
too.

opening_book.txt lists openings, one per line, in SAN. While a game follows one of
those lines, Remus plays the next book move right away.

## Where this piece fits

opening_book.py uses notation.py, make_move.py, and game_state.py. uci_engine.py and console_game.py use it on Day 10.

- **Uses:** [`fen.py`](fen.md), [`game_state.py`](game_state.md), [`make_move.py`](make_move.md), [`moves.py`](moves.md), [`notation.py`](notation.md)
- **Used by:** [`console_game.py`](console_game.md), [`uci_engine.py`](uci_engine.md)

## Words to know

- **opening:** the first few moves of a game, often with a famous name.
- **book move:** a move taken from the opening list instead of from search.
- **out of book:** the game has left every line in the list.

## What it stores

A line in opening_book.txt:

```text
e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7
```

The book becomes a dict from position key to a list of moves. After 1. e4, the list
holds e5, c5, e6, and c6.

## How it works

1. `load_book()` reads opening_book.txt one line at a time.
2. It plays each line from the start, checking every move with `parse_san()`.
3. For each position on the way, it records the next move.
4. A typo stops that one line. A missing file gives an empty book.
5. `book_move()` picks one of the recorded moves, or None when out of book.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
load_book()
    state_from_fen()  [fen.py]
    make_move()  [make_move.py]
    parse_san()  [notation.py]
    position_key()  [game_state.py]

book_move()
    position_key()  [game_state.py]
```

## The functions

| Function | What it does | Day |
| --- | --- | --- |
| `load_book` | Reads the opening file into a dict of positions and moves. | 10 |
| `book_move` | Picks a book move for this position, or None. | 10 |

## Try it

From inside a Day folder that has the file, run:

```bash
uv run opening_book.py
```

You should see: `Book positions: 97`, the first moves in the book, and a reply to 1. e4.

## Puzzle questions

1. Add a line for your favorite opening. How many new positions did it add?
2. Why does Remus check every book move with its own move generator?

## Slides

Slides 10.8 in the [slide plan](../slide_plan.md).
