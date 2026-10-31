# game_state.py: Everything the board does not show

*First appears in `Day 02 - Make and undo moves/period3/instructor`.*

## The big picture

A picture of the board does not tell the whole story. Whose turn is it? Can White
still castle? This file keeps those facts next to the board.

All the facts live together in one Python dict called the state.

## Where this piece fits

game_state.py sits right on top of board.py. Every file that makes moves or reads the turn uses it.

- **Uses:** [`board.py`](board.md)
- **Used by:** [`attacks.py`](attacks.md), [`fen.py`](fen.md), [`legal_moves.py`](legal_moves.md), [`make_move.py`](make_move.md), [`move_generation.py`](move_generation.md), [`opening_book.py`](opening_book.md), [`search.py`](search.md)

## Words to know

- **dict:** a Python dictionary. It stores values under names, like `state["turn"]`.
- **castling rights:** which castling moves are still allowed, written as letters like `KQkq`.
- **en passant:** a special pawn capture, allowed only right after a pawn moves two squares.
- **position key:** a short piece of text that describes a position, used to spot repeats.

## What it stores

```python
state = {
    "board": board,          # The 8x8 grid
    "turn": "w",             # Whose move: "w" or "b"
    "castling": "KQkq",      # Castling moves still allowed
    "en_passant": None,      # Square a pawn just skipped, or None
    "halfmove_clock": 0,     # Moves since the last capture or pawn move
    "fullmove_number": 1,    # Goes up by one after Black moves
    "history": [key],        # Every position so far (added on Day 7)
}
```

## How it works

1. `new_game()` builds the state for the start of a game.
2. `color_of()`, `is_white()`, and `opponent()` answer small questions about piece colors.
3. `position_key()` writes the position as one line of text. Two equal keys mean the same position.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
new_game()
    new_board()  [board.py]
    position_key()

color_of()
    is_white()

opponent()
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `new_game` | Makes the state for a brand new game. | Day 2, period 3 |
| `is_white` | Says True if a piece letter is uppercase (White). | Day 2, period 3 |
| `color_of` | Says "w", "b", or None for an empty square. | Day 2, period 3 |
| `opponent` | Gives the other side's piece color. | Day 2, period 3 |
| `position_key` | Writes the position as text, so Remus can tell when a position repeats. | Day 7, period 1 |

## How the file grows

- **Day 2, period 3:** `new_game`, `is_white`, `color_of`, `opponent`
- **Day 7, period 1:** `position_key`

## Try it

Open `game_state.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: The start board, `Side to move: w`, and the piece colors of a few pieces.

## Puzzle questions

1. After 1. e4, what are `turn` and `en_passant`?
2. Why does the position key leave out the move clocks?

## Slides

Slides 2.1, 7.1 in the [slide plan](../../teachers/slide_plan.md).
