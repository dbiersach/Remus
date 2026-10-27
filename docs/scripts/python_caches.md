# python_caches.py: Remember answers in a dict

*Day 9, period 2. The lab file is `labs/day09/python_caches.py`, and the answers are in `labs/day09/instructor/python_caches_instructor.py`.*

## The big picture

A program that computes the same answer twice wastes the second computation. A dict
used as a cache keeps each answer under a key, so the second request takes no time.
This lab caches perft counts, measures a distance with `math.dist()`, repeats random
numbers with `random.seed()`, and watches a teacher demo of `threading.Event`.

## Where this piece fits

The lab runs in the Day 9, period 2 folder. The RED station's transposition table
caches search results the same way, the CYAN station measures king distances, and
`think()` in `search.py` stops through a `threading.Event`.

- **Uses:** [`perft.py`](perft.md), [`game_state.py`](game_state.md)
- **Used by:** nothing; it is practice for the stations in [`transposition_table.py`](transposition_table.md) and [`evaluation.py`](evaluation.md)

## Words to know

- **cache:** a dict of answers already computed.
- **tuple key:** a key made of several values, such as `("start", 3)`.
- **math.dist():** the straight-line distance between two points.
- **threading.Event:** a flag one thread sets and another thread checks, used to stop a search.

## How it works

1. Part #1: `remembered_perft()` computes a count only when its key is missing from the cache.
2. Part #2: measure the distance from d4 to g7.
3. Part #3: seed the random generator so a roll repeats.
4. Part #4 is a teacher demo: a thread counts until another thread sets the stop flag.

The pair types 7 lines.

## Try it

From inside `student/Day 09 - Add the clock and build the stations/period2`, run:

```bash
uv run python_caches.py
```

You should see: 8,902 twice, the second at once; 4.243 squares; True; and the count the thread reached.

## Puzzle questions

1. What would go wrong if the cache key held the depth but not the position?
2. Why does the UCI engine need a stop flag instead of waiting for the search to finish?
