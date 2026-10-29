# Remus-RED: Transposition table

Remember positions already searched, so the same position reached in two move orders is scored once.

## Learning objectives

By the end of Day 9, each student pair can:

- Explain the idea of this enhancement in two sentences. **Measured by:** The student pair explains the idea to another student pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `run_tests.py` passes in the version folder.
- Run a fair experiment: same opening, both piece colors. **Measured by:** In the Day 9 battles, `play_battle.py` in the version folder plays both 10-minute games with no illegal moves or crashes when the student pair presses Run in VS Code, and the student pair says why two games cannot show which enhancement is stronger.

## The idea, with an example

1. Nf3 Nf6 2. d4 and 1. d4 Nf6 2. Nf3 reach the same position by two different move orders. Chess players call that a transposition.

![The position after 1. Nf3 Nf6 2. d4, Black to move](../../../misc/docs/images/boards/red_transposition.svg)

*The green arrows are White's two moves, Nf3 and d4, and the blue arrow is Black's Nf6. Play them in either order and the board ends up the same.*

A search meets transpositions all the time: Remus playing Nf3 then d4 against ...Nf6 and ...e6 reaches one position four ways. Remus-WHITE searches that position four times. Remus-RED searches it once, writes the result in a dict (the transposition table), and looks it up the other three times.

Each entry, keyed by `position_key`, holds the depth searched, the score, the move that was best, and a bound that says how much the score can be trusted. Alpha-beta often stops early, so a score is not always exact:

- `EXACT`: the search found the true score.
- `LOWER`: a move caused a cutoff, so the true score is at least this much.
- `UPPER`: no move beat alpha, so the true score is at most this much.

`probe()` answers from the table only when the stored search went at least as deep as the one needed and the bound settles the question. A lower bound of +120 settles a search that only asks "is it at least +100?" (beta = 100), but not one that asks for the exact score.

## Why it makes Remus stronger

A lookup replaces a whole subtree. Even when the stored score cannot be used, because it is too shallow or its bound does not settle the question, the stored best move is tried first. Iterative deepening makes this pay twice: the depth 3 search fills the table with best moves that put the depth 4 search's best move first almost everywhere, and alpha-beta prunes most when the best move comes first.

## What it costs

One dict lookup and one dict write per position. The key is already in the game history, so it costs nothing to build. The table starts empty for every move and holds one entry per position searched, a few hundred thousand at most, which a laptop's memory holds easily. Mate scores are not stored, because a mate score counts plies from the root, so the same position gets a different mate score at a different ply.

## Measured against Remus-WHITE

Each version searched the ten positions of `compare_search.py`, one depth at a time up to depth 4, on one computer. Fewer positions for the same depth means a smaller search tree. Positions per second shows what each position costs. The last column gave each position 5 seconds, the way a game does, and averages the deepest search that finished.

| Version | Positions to finish depth 4 | Share of Remus-WHITE's | Positions per second | Average depth in 5 seconds |
| --- | ---: | ---: | ---: | ---: |
| Remus-WHITE | 431,212 | 100% | 5,183 | 3.1 |
| Remus-RED | 243,223 | 56% | 4,994 | 3.7 |

## What to expect

Remus-RED is the only engine with one enhancement that rated clearly above Remus-WHITE in the designer's league: +101 plus or minus 67. Fewer positions for the same depth, and the biggest savings in endgames, where a few pieces shuffle between the same squares and nearly every position is reached many ways. Positions per second stay close to Remus-WHITE's.

## Where your code fits

`table_search()` in `search.py` replaces Remus-WHITE's search. At the top of every position it calls `probe()`, and if the answer is a score, it returns at once. After a cutoff it calls `store()` with `LOWER`; after searching every move it calls `store()` with `EXACT` if a move beat alpha and `UPPER` if none did. `store()` keeps the deeper of two results for the same position.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus in `00 WHITE - No enhancements` beside it, plus this one enhancement. The student pair writes `store()` in `transposition_table.py`, `probe()` in `transposition_table.py`, `test_transposition_table_bounds()` in `test_upgrades.py`.

## The changes and why

### `store()` in `transposition_table.py`

Saves what one search learned about a position under its key: the depth, the score, whether that score is exact or only a bound, and the best move. A dict holds the table, so looking a position up again costs one step.

### `probe()` in `transposition_table.py`

Looks up a position in the table and returns a stored score only when it answers this search: it was searched deep enough, and its bound fits the window. One position reached by two move orders is then searched once.

### `test_transposition_table_bounds()` in `test_upgrades.py`

Proves the rules of `probe()` with three made-up entries before any real search uses them. A bound is the tricky part: "at least 80" settles a window whose beta is 70, but says nothing useful when beta is 100.

## Check it

Check the work by opening `run_tests.py` in this folder and pressing Run. Then open `smoke_test.py` in VS Code and press Run: Remus-RED plays one 2-minute game against Remus-WHITE, which shows that the engine plays legal moves to the end of a game. In the Day 9 battles, follow the numbered steps at the top of `play_battle.py`: copy the visiting student pair's engine folder into `engines/student`, set `VISITING_ENGINE` to the visitor's engine color, and press Run. Remus-RED plays it twice at 10 minutes a side, once with each piece color, and both games go into misc/games/remus_games.pgn. Each script runs `version_match.py` from the folder above this one.

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `transposition_table.py` | `store()` | 25 | 3 | `test_upgrades.py::test_transposition_table_bounds` |
| `transposition_table.py` | `probe()` | 34 | 11 | `test_upgrades.py::test_transposition_table_bounds` |
| `test_upgrades.py` | `test_transposition_table_bounds()` | 17 | 13 | `run_tests.py` |

Lines to type in all: 27. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `store()` in `transposition_table.py`

**Where:** lines 29 to 31 of `transposition_table.py`, inside `store()`, in place of the stub below the docstring. It is called by `table_search()` in `search.py`.

```python
25 | def store(
26 |     table: dict, key: str, depth: int, score: int, bound: str, best: Move | None
27 | ) -> None:
28 |     """Save a search result for a position, keeping the deeper of two results."""
29 +     old = table.get(key)
30 +     if old is None or depth >= old["depth"]:
31 +         table[key] = {"depth": depth, "score": score, "bound": bound, "best": best}
32 |
33 |
34 | def probe(table: dict, key: str, depth: int, alpha: int, beta: int) -> int | None:
```

**How it works:** `table.get(key)` returns what the table already holds for this position, or None. The new result is saved when there is no old one, or when the new search went at least as deep (`depth >= old["depth"]`), because a deeper search is worth more. The entry is a small dict with the depth, the score, the bound (EXACT, LOWER, or UPPER), and the best move.

### `probe()` in `transposition_table.py`

**Where:** lines 56 to 66 of `transposition_table.py`, inside `probe()`, in place of the stub below the docstring. It is called by `table_search()` in `search.py`.

```python
34 | def probe(table: dict, key: str, depth: int, alpha: int, beta: int) -> int | None:
35 |     """
     ...
54 |         or an upper bound at or below alpha (no improvement). Otherwise None.
55 |     """
56 +     entry = table.get(key)
57 +     if entry is None or entry["depth"] < depth:
58 +         return None
59 +     score = entry["score"]
60 +     if entry["bound"] == EXACT:
61 +         return score
62 +     if entry["bound"] == LOWER and score >= beta:
63 +         return score
64 +     if entry["bound"] == UPPER and score <= alpha:
65 +         return score
66 +     return None
67 |
68 |
69 | def best_stored_move(table: dict, key: str) -> Move | None:
```

**How it works:** The function returns a score only when the stored result answers the question this search asks. A missing entry, or one searched less deeply than `depth`, returns None. An EXACT score always answers. A LOWER bound means the true score is at least the stored score, so it answers only when it reaches `beta`: that is already a cutoff. An UPPER bound means the true score is at most the stored score, so it answers only when it is at or below `alpha`: the move cannot improve on the best so far. Anything else returns None, and the position is searched.

### `test_transposition_table_bounds()` in `test_upgrades.py`

**Where:** lines 20 to 32 of `test_upgrades.py`, inside `test_transposition_table_bounds()`, in place of the stub below the docstring. `run_tests.py` runs it with every other test in the folder.

```python
17 | def test_transposition_table_bounds() -> None:
18 |     """Expected: an exact entry answers at its depth; a bound answers only when it
19 |     settles the window."""
20 +     table = {}
21 +     best = Move((6, 4), (4, 4))
22 +     store(table, "a", 3, 50, EXACT, best)
23 +     store(table, "b", 3, 80, LOWER, None)
24 +     store(table, "c", 3, -20, UPPER, None)
25 +     assert probe(table, "a", 3, -100, 100) == 50
26 +     assert probe(table, "a", 4, -100, 100) is None  # Not searched deep enough
27 +     assert probe(table, "b", 3, -100, 70) == 80  # At least 80 is a cutoff above beta 70
28 +     assert (
29 +         probe(table, "b", 3, -100, 100) is None
30 +     )  # At least 80 does not settle beta 100
31 +     assert probe(table, "c", 3, 0, 100) == -20  # At most -20 cannot beat alpha 0
32 +     assert best_stored_move(table, "a") == best
33 |
34 |
35 | def test_two_move_orders_reach_one_position_key() -> None:
```

**How it works:** The test fills an empty table by hand with three made-up positions, "a", "b", and "c", one for each kind of bound. Each assert then asks one question. Position a's exact 50 answers at depth 3 but not at depth 4, which was never searched. Position b is at least 80: that settles a window whose beta is 70 (a cutoff), but not one whose beta is 100. Position c is at most -20, which cannot beat alpha 0. The last line checks that the best move of position a was kept.
