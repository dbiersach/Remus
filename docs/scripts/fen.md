# fen.py: A whole position in one line

*First appears in `instructor/Day 06 - Count positions and read FEN/period4`.*

## The big picture

FEN is a way to write a whole chess position on one line. Every chess program can
read it, so Remus can load any position you find online.

This file reads FEN into a game state and writes a game state back out as FEN.

## Where this piece fits

fen.py uses board.py and game_state.py. Tests, puzzles, the UCI engine, and many self-checks use it to set up positions.

- **Uses:** [`board.py`](board.md), [`game_state.py`](game_state.md)
- **Used by:** [`compare_search.py`](compare_search.md), [`console_game.py`](console_game.md), [`opening_book.py`](opening_book.md), [`uci_engine.py`](uci_engine.md)

## Words to know

- **FEN:** Forsyth-Edwards Notation, a one-line text for a chess position.
- **field:** one part of the FEN line. The parts are split by spaces.
- **placement:** the first field: where every piece stands.

## What it stores

The starting position in FEN:

```text
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
|                                         | |  |   | | |
pieces, rank 8 first, / between ranks     | |  |   | | move number
                                 side to move  |   | halfmove clock
                                   castling rights  en passant square
```

A digit means that many empty squares. `8` is a whole empty rank.

## How it works

1. `state_from_fen()` splits the line into its six fields.
2. `board_from_placement()` turns the first field into the 8x8 board.
3. The other fields fill in the turn, castling, en passant square, and clocks.
4. `state_to_fen()` runs the other way, using `fen_placement()`.
5. `print_state()` shows a state the way a person reads it: the board, each FEN
   field with its meaning, and the whole FEN line.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
state_from_fen()
    board_from_placement()
    position_key()  [game_state.py]
    parse_square()  [board.py]

state_to_fen()
    square_name()  [board.py]
    fen_placement()

print_state()
    print_board()  [board.py]
    square_name()  [board.py]
    state_to_fen()
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `fen_placement` | Writes the board as the first FEN field. | Day 6, period 4 |
| `board_from_placement` | Reads the first FEN field into a board. | Day 6, period 4 |
| `state_from_fen` | Reads a full FEN line into a game state. | Day 6, period 4 |
| `state_to_fen` | Writes a game state as a full FEN line. | Day 6, period 4 |
| `print_state` | Prints the board, each FEN field with its meaning, and the FEN line. | Day 6, period 4 |

## Try it

From inside a period folder that has the file, run:

```bash
uv run fen.py
```

You should see: the board after 1. e4 with Black to move and en passant square e3,
the FEN line for that position, then `Start FEN read and written back unchanged: True`.

## Puzzle questions

1. What does `4P3` mean in a FEN rank?
2. After 1. e4, which FEN field changes from `-` to `e3`?

## Slides

Slides 6.4 in the [slide plan](../slide_plan.md).
