# Remus-RED: Transposition table

Remember positions already searched, so the same position reached in two move orders is scored once.

## Learning objectives

By the end of the station, each pair can:

- Explain the idea of the station's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the station folder.
- Run a fair experiment against Remus-WHITE: same opening, both colors. **Measured by:** In the Day 10 tournament, `uv run station_match.py <COLOR>` plays both 10-minute games with no illegal moves or crashes, and the pair says why two games cannot show whether the enhancement helps.

## The idea, with an example

1. Nf3 Nf6 2. d4 and 1. d4 Nf6 2. Nf3 reach the same position by two different move orders. Chess players call that a transposition. A search meets transpositions all the time: Remus playing Nf3 then d4 against ...Nf6 and ...e6 reaches one position four ways. Remus-WHITE searches that position four times. Remus-RED searches it once, writes the result in a dict (the transposition table), and looks it up the other three times.

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

Fewer positions for the same depth, and the biggest savings in endgames, where a few pieces shuffle between the same squares and nearly every position is reached many ways. Positions per second stay close to Remus-WHITE's.

## Where your code fits

`table_search()` in `search.py` replaces Remus-WHITE's search. At the top of every position it calls `probe()`, and if the answer is a score, it returns at once. After a cutoff it calls `store()` with `LOWER`; after searching every move it calls `store()` with `EXACT` if a move beat alpha and `UPPER` if none did. `store()` keeps the deeper of two results for the same position.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus, plus this one enhancement. The pair writes `store()` in `transposition_table.py`, `probe()` in `transposition_table.py`, `test_transposition_table_bounds()` in `test_upgrades.py`.

## The changes and why

### `store()` in `transposition_table.py`

Saves what one search learned about a position under its key: the depth, the score, whether that score is exact or only a bound, and the best move. A dict holds the table, so looking a position up again costs one step.

### `probe()` in `transposition_table.py`

Looks up a position in the table and returns a stored score only when it answers this search: it was searched deep enough, and its bound fits the window. One position reached by two move orders is then searched once.

### `test_transposition_table_bounds()` in `test_upgrades.py`

Proves the rules of `probe()` with three made-up entries before any real search uses them. A bound is the tricky part: "at least 80" settles a window whose beta is 70, but says nothing useful when beta is 100.

## Check it

Check the work from inside this folder with `uv run pytest`. In the Day 10 tournament, `uv run station_match.py RED` in the Stations folder plays Remus-RED against Remus-WHITE twice, once with each color, at 10 minutes a side, and adds both games to games/remus_games.pgn.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `transposition_table.py` | `store()` | 25 | 3 | `test_upgrades.py::test_transposition_table_bounds` |
| `transposition_table.py` | `probe()` | 34 | 11 | `test_upgrades.py::test_transposition_table_bounds` |
| `test_upgrades.py` | `test_transposition_table_bounds()` | 17 | 13 | `uv run pytest` |

Lines to type in all: 27. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
