# python_caches.py: Remember answers in a dict

*Day 9, period 2. The lab file is `Day 09 - Add the clock and build enhanced engines/period2/student/python_caches.py`, and the answers are in `Day 09 - Add the clock and build enhanced engines/period2/instructor/python_caches_instructor.py`.*

## The big picture

A program that computes the same answer twice wastes the second computation. A dict
used as a cache keeps each answer under a key, so the second request takes no time.
This lab caches the number of paths a lone knight can take (a small perft), measures a distance with `math.dist()`, and repeats
random numbers with `random.seed()`.

## Where this piece fits

The lab runs in the Day 9, period 2 folder. Remus-RED's transposition table
caches search results the same way, and Remus-CYAN measures king distances.

- **Uses:** nothing outside the standard library; `knight_perft()` sits in the lab file itself
- **Used by:** nothing; it is practice for the enhanced engines in [`transposition_table.py`](../code/transposition_table.md) and [`evaluation.py`](../code/evaluation.md)

## Words to know

- **cache:** a dict of answers already computed.
- **tuple key:** a key made of several values, such as `((7, 6), 8)`, the square g1 and a depth of 8.
- **math.dist():** the straight-line distance between two points.

## How it works

1. Part #1: `knight_perft()` counts every path a lone knight can take in 8 moves from g1, and `remembered_perft()` computes that count only when its key is missing from the cache.
2. Part #2: measure the distance from d4 to g7.
3. Part #3: seed the random generator so a roll repeats.

The student pair types 7 lines.

## Try it

Open `python_caches.py` in `Day 09 - Add the clock and build enhanced engines/period2/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: 811,156 twice, the second at once; 4.243 squares; and True.

## Puzzle questions

1. What would go wrong if the cache key held the depth but not the square?
2. Seeding the generator makes every run roll the same numbers. Why does a test that uses random moves need that?
