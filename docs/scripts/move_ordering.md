# move_ordering.py: Try the best moves first

*First appears in `instructor/Day 09 - Search faster with alpha-beta/period3`.*

## The big picture

Alpha-beta saves the most work when it tries a strong move first. This file sorts
the moves so the likely best ones come first.

Big captures by small pieces go first. Pawn takes queen comes before queen takes pawn.

## Where this piece fits

move_ordering.py uses board.py and evaluation.py. search.py calls it at every position.

- **Uses:** [`board.py`](board.md), [`evaluation.py`](evaluation.md), [`moves.py`](moves.md)
- **Uses only in its self-check:** [`fen.py`](fen.md), [`legal_moves.py`](legal_moves.md)
- **Used by:** [`search.py`](search.md)

## Words to know

- **MVV-LVA:** Most Valuable Victim, Least Valuable Attacker. A rule for sorting captures.
- **killer move:** a quiet move that worked well in a nearby position. It is tried early (Day 10).
- **quiet move:** a move that does not capture or promote.

## What it stores

How moves are ranked, best first:

1. The `first` move: the best move from the last search.
2. Captures, by MVV-LVA score.
3. Killer moves (Day 10).
4. All other quiet moves.

## How it works

1. `mvv_lva_score()` gives each capture a number: ten times the victim's value, minus the attacker's value.
2. `order_moves()` sorts the moves by that number, biggest first.
3. The `first` move and killer moves get extra points to move them up.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
order_moves()
    mvv_lva_score()
        piece_at()  [board.py]
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `mvv_lva_score` | Scores a capture: big victim and small attacker score high. | Day 9, period 3 |
| `order_moves` | Sorts the moves so the likely best ones come first. | Day 9, period 3 |

## Try it

From inside a period folder that has the file, run:

```bash
uv run move_ordering.py
```

You should see: The first two moves of a test position: pawn takes queen, then queen takes rook.

## Puzzle questions

1. Which comes first: knight takes rook, or rook takes knight? Why?
2. Why does sorting not change the score that alpha-beta finds?

## Slides

Slides 9.4, 10.4 in the [slide plan](../slide_plan.md).
