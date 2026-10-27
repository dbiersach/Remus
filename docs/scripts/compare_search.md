# compare_search.py: Prove that alpha-beta saves work

*First appears in `instructor/Day 08 - Search ahead with alpha-beta/period2`.*

## The big picture

Alpha-beta should find the same score as negamax with much less work. This file
checks that on ten positions.

## Where this piece fits

compare_search.py uses search.py and fen.py. It is a Day 8 experiment.

- **Uses:** [`fen.py`](fen.md), [`search.py`](search.md)
- **Used by:** no other Remus file

## Words to know

- **node:** one position the search visits.

## What it stores

Each line shows both searches at depth 3. Alpha-beta visits less than a fifth of the
positions, with the same score.

## How it works

1. Load each of the ten positions.
2. Search it with `negamax()`, then with `alpha_beta()`.
3. Check that the scores match and print both node counts.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
main()
    state_from_fen()  [fen.py]
    negamax()  [search.py]
    alpha_beta()  [search.py]
```

## Try it

From inside a period folder that has the file, run:

```bash
uv run compare_search.py
```

You should see: Ten lines like `negamax 24,942 positions, alpha-beta 4,226 positions, same score`.

## Puzzle questions

1. Which position saved the most work? Why might that be?

## Slides

Slides 8.5 in the [slide plan](../slide_plan.md).
