# opening_book.py: Play known openings without thinking

*Lives in Remus-GOLD, in `engines/instructor/11 Remus-GOLD - All enhancements`, the engine of Day 10, and in its own enhanced engine (Day 9).*

## The big picture

Strong players know the first few moves of popular openings by heart. Remus can
too.

opening_book.txt lists 43 openings, one per line, in SAN, each with a `#` comment
above it that names the opening, such as `# Sicilian Defense, Najdorf Variation`.

The book also holds 13 traps that snag beginners, such as Scholar's Mate and the
Fried Liver Attack. A trap line starts with `White:` or `Black:`, the side that
defends. Remus stores only the defender's moves from it, so Remus answers 3. Qh5
with 3... g6 at once but never plays 3. Qh5 itself. While a game follows one of
those lines, Remus plays the next book move right away.

## Where this piece fits

opening_book.py uses notation.py, make_move.py, and game_state.py. uci_engine.py uses it in Remus-GREEN and Remus-GOLD.

- **Uses:** [`fen.py`](fen.md), [`game_state.py`](game_state.md), [`make_move.py`](make_move.md), [`moves.py`](moves.md), [`notation.py`](notation.md)
- **Used by:** [`uci_engine.py`](uci_engine.md)

## Words to know

- **opening:** the first few moves of a game, often with a famous name.
- **book move:** a move taken from the opening list instead of from search.
- **out of book:** the game has left every line in the list.
- **trap:** a move that sets bait. A beginner who takes the bait loses quickly.

## What it stores

A line in opening_book.txt:

```text
e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7
```

The book becomes a dict from position key to a list of moves. After 1. e4, the list
holds e5, c5, e6, c6, d6, d5, and Nf6.

## How it works

1. `load_book()` reads opening_book.txt one line at a time and skips blank lines and
   lines that start with `#`. `read_defender()` splits off a `White:` or `Black:` mark.
2. It plays each line from the start, checking every move with `parse_san()`.
3. For each position on the way, it records the next move. On a trap line it records
   only the defender's moves.
4. A typo stops that one line. A missing file gives an empty book. Remus reports both on standard error, so Lucas Chess never sees them.
5. `book_move()` picks one of the recorded moves, or None when out of book.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
load_book()
    read_defender()
    state_from_fen()  [fen.py]
    make_move()  [make_move.py]
    parse_san()  [notation.py]
    position_key()  [game_state.py]

book_move()
    position_key()  [game_state.py]
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `read_defender` | Splits a book line into the side that may use it and its moves. | Remus-GOLD |
| `load_book` | Reads the opening file into a dict of positions and moves. | Remus-GOLD |
| `book_move` | Picks a book move for this position, or None. | Remus-GOLD |

## Try it

Open `opening_book.py` from the `11 Remus-GOLD - All enhancements` folder in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: `Book positions: 285`, the first moves in the book, and a reply to 1. e4.

## Puzzle questions

1. Add a line for your favorite opening. How many new positions did it add?
2. Why does Remus check every book move with its own move generator?

## Slides

Slides 9.15 in the [slide plan](../course/slide_plan.md).
