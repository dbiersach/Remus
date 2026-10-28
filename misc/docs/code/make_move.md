# make_move.py: Make a move, then take it back

*First appears in `Day 02 - Make and undo moves/period4/instructor`.*

## The big picture

Search tries thousands of moves to see what happens. After each try, it must put
the board back exactly as it was.

This file does both jobs. `make_move()` plays a move and hands back an undo record.
`undo_move()` uses that record to rewind the game.

## Where this piece fits

make_move.py uses board.py, game_state.py, and moves.py. Legal moves, perft, search, and the UCI engine all depend on it.

- **Uses:** [`board.py`](board.md), [`game_state.py`](game_state.md), [`moves.py`](moves.md)
- **Used by:** [`console_game.py`](console_game.md), [`legal_moves.py`](legal_moves.md), [`notation.py`](notation.md), [`opening_book.py`](opening_book.md), [`perft.py`](perft.md), [`search.py`](search.md), [`uci_engine.py`](uci_engine.md)

## Words to know

- **undo record:** a dict that remembers everything a move changed.
- **captured piece:** the enemy piece removed by a move, or `.` if none.
- **snapshot:** the whole state written as text, so two states are easy to compare.
- **halfmove clock:** counts moves since the last capture or pawn move. It is for the fifty-move rule.

## What it stores

The undo record for 1. e4 looks like this:

```python
{"move": Move((6, 4), (4, 4)), "piece": "P", "captured": ".",
 "castling": "KQkq", "en_passant": None,
 "halfmove_clock": 0, "fullmove_number": 1,
 "rook_move": None, "en_passant_victim": None}
```

It holds the old values, from before the move.

## How it works

1. Save the old values in the undo record.
2. Move the piece. Castling also moves the rook. En passant also removes a pawn. Promotion swaps the pawn for a new piece.
3. Update the clocks, castling rights, en passant square, and turn.
4. Add the new position key to the history.
5. Later, `undo_move()` does all of this backward.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
make_move()
    piece_at()  [board.py]
    set_piece()  [board.py]
    update_castling_rights()
    opponent()  [game_state.py]
    en_passant_victim_square()
    castling_rook_move()
    position_key()  [game_state.py]

undo_move()
    set_piece()  [board.py]
    opponent()  [game_state.py]
    piece_at()  [board.py]

state_snapshot()
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `update_castling_rights` | Removes castling letters when a king or rook moves or is captured. | Day 5, period 2 |
| `en_passant_victim_square` | Finds the pawn that an en passant capture removes. | Day 5, period 3 |
| `castling_rook_move` | Finds where the rook goes when the king castles. | Day 5, period 2 |
| `make_move` | Plays a move on the state and returns the undo record. | Day 2, period 4 |
| `undo_move` | Takes back a move using its undo record. | Day 2, period 4 |
| `state_snapshot` | Writes the whole state as text, to check that undo worked. | Day 2, period 4 |

## How the file grows

- **Day 2, period 4:** `make_move`, `undo_move`, `state_snapshot`
- **Day 5, period 2:** `update_castling_rights`, `castling_rook_move`
- **Day 5, period 3:** `en_passant_victim_square`

## Try it

Open `make_move.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: A board after 15 moves made and undone, then `back at the start: True`.

## Puzzle questions

1. Why must the undo record keep the old castling rights?
2. What would go wrong in search if `undo_move()` forgot the en passant square?

## Slides

Slides 2.3, 2.4, 2.5, 5.2, 5.3, 5.4 in the [slide plan](../course/slide_plan.md).
