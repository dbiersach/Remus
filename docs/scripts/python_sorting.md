# python_sorting.py: Sort, start at minus infinity, time it

*Day 8, period 2. The lab file is `labs/day08/python_sorting.py`, and the answers are in `labs/day08/instructor/python_sorting_instructor.py`.*

## The big picture

Three small tools make the search faster and easier to measure. A loop that
inserts each capture behind every bigger one puts the most promising captures first, a best value that starts at minus
infinity is beaten by the first real value, and `time.perf_counter()` measures how
long the work takes.

## Where this piece fits

The lab runs in the Day 8, period 2 folder and times `perft()` from `perft.py`. The
same period, `alpha_beta()` starts alpha at the lowest score, and `compare_search.py`
times negamax against alpha-beta.

- **Uses:** [`perft.py`](perft.md), [`game_state.py`](game_state.md)
- **Used by:** nothing; it is practice for [`search.py`](search.md), [`move_ordering.py`](move_ordering.md), and [`compare_search.py`](compare_search.md)

## Words to know

- **insert():** puts an item into a list at a chosen place, such as `ordered.insert(0, piece)` for the front.
- **float("inf"):** infinity: larger than every number, so `-float("inf")` is smaller than every number.
- **time.perf_counter():** a clock for measuring how long code runs.

## How it works

1. Part #1: sort the victims, most valuable first: each piece steps past every piece worth at least as much, then goes in.
2. Part #2: find the best victim with a best value that starts at minus infinity.
3. Part #3: time `perft(3)` from the start position.

The pair types 19 lines.

## Try it

From inside `student/Day 08 - Search ahead with alpha-beta/period2`, run:

```bash
uv run python_sorting.py
```

You should see: `['q', 'r', 'n', 'p']`, the best victim q worth 9, and 8,902 positions with the run time.

## Puzzle questions

1. Why does Part #2 start below every value instead of at 0?
2. How much longer does `perft(4)` take than `perft(3)`? Guess first.
