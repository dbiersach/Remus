# exchange.py: Count a whole exchange before it happens

*Appears only in `engines/instructor/12 Remus-PLATINUM - Ten more enhancements`, the course designer's engine.*

## The big picture

A capture is only good if it still wins after the other side takes back. A queen
that takes a pawn guarded by a knight wins 100 and then loses 900. This file adds
up a whole exchange on one square without searching: each side keeps taking back
with its cheapest piece, and each side may stop when taking back would lose.
Chess programmers call it static exchange evaluation, or SEE.

## Where this piece fits

- **Uses:** [`board.py`](board.md), [`evaluation.py`](evaluation.md) (the piece values), [`moves.py`](moves.md)
- **Uses only in its self-check:** [`fen.py`](fen.md)
- **Used by:** [`search.py`](search.md), in Remus-PLATINUM's quiescence search, which skips any capture that loses material

## Words to know

- **exchange:** a capture and every recapture on the same square.
- **least valuable attacker:** the cheapest piece that can capture on a square. A pawn goes before a knight, and a knight before a queen.
- **x-ray:** a piece lined up behind another one, such as a rook behind a rook. When the front piece captures, the back one can take next.

## Call tree

```
static_exchange()
├── exchange_value()
└── least_valuable_attacker()
    ├── exchange_value()
    └── attacks_square()
        └── step_toward()
```

## The functions

- `exchange_value()` gives a piece's value, with the king worth 10,000 so no exchange may win it.
- `step_toward()` gives one step, 1, -1, or 0, in the direction of a gap.
- `attacks_square()` says whether one piece attacks one square. A rook, bishop, or queen needs an empty line.
- `least_valuable_attacker()` finds the cheapest piece of one side that attacks a square.
- `static_exchange()` plays the exchange on a copy of the board and returns what the first capture wins or loses.

## Questions

1. White's queen on d1 takes a pawn on d5. A Black knight on f6 guards the pawn. What does `static_exchange()` return?
2. Why does the function work on a copy of the board?
3. Two White rooks stand on d1 and d2, and a Black rook guards the pawn on d5. Why does the rook on d1 join the exchange?
