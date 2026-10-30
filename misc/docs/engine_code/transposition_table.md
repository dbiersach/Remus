# transposition_table.py: Remember positions already searched

*Lives in Remus-GOLD, in the teacher's `engines/instructor/11 GOLD - All enhancements`, the engine of Day 10.*

## The big picture

You can reach the same position by different move orders. Searching it twice wastes
time.

This file is Remus's memory. It is a plain Python dict. The key is the position. The
value is what the search learned about it.

## Where this piece fits

transposition_table.py uses game_state.py and moves.py. Only `upgraded_search()` in search.py uses it (Day 10).

- **Uses:** [`moves.py`](moves.md)
- **Uses only in its self-check:** [`fen.py`](fen.md), [`game_state.py`](game_state.md)
- **Used by:** [`search.py`](search.md)

## Words to know

- **transposition:** the same position reached by a different order of moves.
- **bound:** a score that may be exact, or only a lower or upper limit.
- **probe:** look up a position in the table.

## What it stores

One table entry:

```python
table[key] = {"depth": 3, "score": 25, "bound": "exact", "best": Move(...)}
```

| Bound | What the score means |
| --- | --- |
| `exact` | The true score at that depth |
| `lower` | The true score is at least this much |
| `upper` | The true score is at most this much |

## How it works

1. After searching a position, `store()` saves the depth, score, bound, and best move.
2. Before searching, `probe()` looks the position up.
3. If the stored search was deep enough, the search can reuse the score.
4. Even if not, `best_stored_move()` gives a strong move to try first.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
store()

probe()

best_stored_move()
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `store` | Saves what the search learned about a position. | Remus-GOLD |
| `probe` | Returns a saved score, if it can answer this search. | Remus-GOLD |
| `best_stored_move` | Returns the best move saved for a position. | Remus-GOLD |

## Try it

Open `transposition_table.py` from the `11 GOLD - All enhancements` folder in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: A saved score found at depth 3, and `None` when the search asks for depth 4.

## Puzzle questions

1. Name two move orders that reach the same position.
2. Why can a depth 2 result not answer a depth 4 search?

## Slides

Slides 9.6, 9.7 in the [slide plan](../course/slide_plan.md).
