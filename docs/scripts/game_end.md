# game_end.py: Is the game over?

*First appears in `instructor/Day 07 - Play full games in En Croissant`.*

## The big picture

A game can end in checkmate. It can also end in a draw, for five different reasons.

This file checks each reason in turn. It says who won and why, or None if the game
goes on.

## Where this piece fits

game_end.py uses attacks.py and legal_moves.py. console_game.py uses it to stop the game.

- **Uses:** [`attacks.py`](attacks.md), [`board.py`](board.md), [`legal_moves.py`](legal_moves.md)
- **Uses only in its self-check:** [`fen.py`](fen.md)
- **Used by:** [`console_game.py`](console_game.md)

## Words to know

- **checkmate:** the king is in check and has no legal move. The other side wins.
- **stalemate:** no legal move, but not in check. The game is a draw.
- **insufficient material:** neither side has enough pieces left to checkmate.
- **threefold repetition:** the same position appears three times. The game is a draw.
- **fifty-move rule:** fifty moves each with no capture and no pawn move. The game is a draw.

## What it stores

`game_result()` returns a pair, such as `("0-1", "checkmate")` or
`("1/2-1/2", "stalemate")`. It returns `None` while the game goes on.

## How it works

1. No legal moves? If in check, checkmate. If not, stalemate.
2. Too few pieces to mate? Draw by insufficient material.
3. Position seen three times? Draw by repetition.
4. Halfmove clock at 100? Draw by the fifty-move rule.
5. Otherwise the game goes on.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
game_result()
    insufficient_material()
    legal_moves()  [legal_moves.py]
    in_check()  [attacks.py]
    repetition_count()
```

## The functions

| Function | What it does | Day |
| --- | --- | --- |
| `insufficient_material` | Says True if neither side can ever checkmate. | 7 |
| `repetition_count` | Counts how many times this position has appeared. | 7 |
| `game_result` | Says who won and why, or None if the game goes on. | 7 |

## Try it

From inside a Day folder that has the file, run:

```bash
uv run game_end.py
```

You should see: Fool's mate as `('0-1', 'checkmate')`, a stalemate, a draw with king and knight, and `None` for the start.

## Puzzle questions

1. Why is king and knight against king a draw?
2. Why does the fifty-move rule check for 100 and not 50?

## Slides

Slides 7.4, 7.5 in the [slide plan](../slide_plan.md).
