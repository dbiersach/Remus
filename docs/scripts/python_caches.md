# python_caches.py: Remember answers in a dict

*Day 9, period 2. The lab file is `student/Day 09 - Add the clock and build the stations/period2/python_caches.py`, and the answers are in `instructor/Day 09 - Add the clock and build the stations/period2/python_caches_instructor.py`.*

## The big picture

A program that computes the same answer twice wastes the second computation. A dict
used as a cache keeps each answer under a key, so the second request takes no time.
This lab caches perft counts, measures a distance with `math.dist()`, and repeats
random numbers with `random.seed()`.

## Where this piece fits

The lab runs in the Day 9, period 2 folder. The RED station's transposition table
caches search results the same way, and the CYAN station measures king distances.

- **Uses:** [`perft.py`](perft.md), [`game_state.py`](game_state.md)
- **Used by:** nothing; it is practice for the stations in [`transposition_table.py`](transposition_table.md) and [`evaluation.py`](evaluation.md)

## Words to know

- **cache:** a dict of answers already computed.
- **tuple key:** a key made of several values, such as `("start", 3)`.
- **math.dist():** the straight-line distance between two points.

## How it works

1. Part #1: `remembered_perft()` computes a count only when its key is missing from the cache.
2. Part #2: measure the distance from d4 to g7.
3. Part #3: seed the random generator so a roll repeats.

The pair types 7 lines.

## Try it

Open `python_caches.py` in `student/Day 09 - Add the clock and build the stations/period2` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: 8,902 twice, the second at once; 4.243 squares; and True.

## Puzzle questions

1. What would go wrong if the cache key held the depth but not the position?
2. Seeding the generator makes every run roll the same numbers. Why does a test that uses random moves need that?
