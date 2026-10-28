# Remus-PINK: Principal variation search

Search the first move with the full window and every other move with a cheap null window first.

## Learning objectives

By the end of Day 9, each pair can:

- Explain the idea of the color version's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `uv run pytest` passes in the version folder.
- Run a fair experiment: same opening, both colors. **Measured by:** In the Day 9 battles, `play_battle.py` in the version folder plays both 10-minute games with no illegal moves or crashes when the pair presses Run in VS Code, and the pair says why two games cannot show which enhancement is stronger.

## The idea, with an example

After Remus has searched its first move and found it scores +30, the only question about each other move is "is it better than +30?" Remus-WHITE searches every move with the full window, alpha to beta, to find its exact score. Remus-PINK searches the later moves with a null window from +30 to +31. A null window has no room between alpha and beta, so every reply either fails low (worse than +30) or fails high (better), and cutoffs come at once. Only a move that fails high gets a second search with the full window to find how much better it is.

## Why it makes Remus stronger

With good move ordering the first move is usually the best one, so most later moves fail low on the cheap null-window search and never need a full one. This is principal variation search, PVS: the first move is searched as the principal variation, and the rest only have to prove that they are worse.

## What it costs

A move that turns out better than the first one is searched twice. PVS saves work only when the move ordering is good; with poor ordering the re-searches can cost more than the null windows save.

## Measured against Remus-WHITE

Each version searched the ten positions of `compare_search.py`, one depth at a time up to depth 4, on one computer. Fewer positions for the same depth means a smaller search tree. Positions per second shows what each position costs. The last column gave each position 5 seconds, the way a game does, and averages the deepest search that finished.

| Version | Positions to finish depth 4 | Share of Remus-WHITE's | Positions per second | Average depth in 5 seconds |
| --- | ---: | ---: | ---: | ---: |
| Remus-WHITE | 431,212 | 100% | 5,183 | 3.1 |
| Remus-PINK | 289,419 | 67% | 5,765 | 3.3 |

## What to expect

Fewer positions for the same depth, and the same move in almost every position, because PVS changes how much Remus searches, not what it finds. PVS gains much more in Remus-GOLD, where the table and the killers make the first move the best one far more often.

## Where your code fits

`pvs_search()` in `search.py` searches the first move with the full window and calls `search_later_move()` for every other move. The move is already made when `search_later_move()` runs, and the score comes back from the opponent's point of view, so the code flips its sign and the window, as negamax does.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus in `period1`, plus this one enhancement. The pair writes `search_later_move()` in `search.py`, `test_pvs_search_agrees_with_alpha_beta()` in `test_upgrades.py`, `test_a_null_window_answers_only_better_or_not()` in `test_upgrades.py`.

## The changes and why

### `search_later_move()` in `search.py`

Searches a later move with a null window first, which only answers "better or not?", and searches again with the full window only on a surprise. Most later moves are worse, so the cheap question is usually enough.

### `test_pvs_search_agrees_with_alpha_beta()` in `test_upgrades.py`

PVS must be a faster way to the same answer, never a different answer. The test searches one position with the Day 9 search and with PVS and compares the scores, and checks that the position is unchanged afterward.

### `test_a_null_window_answers_only_better_or_not()` in `test_upgrades.py`

Shows what a null window really returns. With a window one point wide, the score only says whether the exact score is above alpha or not, so the test tries an alpha 50 below the exact score and one 50 above it. That yes-or-no answer is why PVS must search again when a move surprises it.

## Check it

Check the work from inside this folder with `uv run pytest`. Then open `smoke_test.py` in VS Code and press Run: Remus-PINK plays one 2-minute game against Remus-WHITE, which shows that the engine plays legal moves to the end of a game. In the Day 9 battles, copy the visiting pair's color folder into the `engines` folder, open `play_battle.py`, press Run, and type the visitor's color: Remus-PINK plays it twice at 10 minutes a side, once with each color, and both games go into misc/games/remus_games.pgn. Each script runs `version_match.py` from the `engines` folder above this one.

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `search_later_move()` | 396 | 6 | `uv run pytest` |
| `test_upgrades.py` | `test_pvs_search_agrees_with_alpha_beta()` | 14 | 7 | `uv run pytest` |
| `test_upgrades.py` | `test_a_null_window_answers_only_better_or_not()` | 23 | 5 | `uv run pytest` |

Lines to type in all: 18. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
