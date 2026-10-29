# Remus-PINK: Principal variation search

Search the first move with the full window and every other move with a cheap null window first.

## Learning objectives

By the end of Day 9, each student pair can:

- Explain the idea of the color version's enhancement in two sentences. **Measured by:** The student pair explains the idea to another student pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `run_tests.py` passes in the version folder.
- Run a fair experiment: same opening, both piece colors. **Measured by:** In the Day 9 battles, `play_battle.py` in the version folder plays both 10-minute games with no illegal moves or crashes when the student pair presses Run in VS Code, and the student pair says why two games cannot show which enhancement is stronger.

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

This folder is Remus-WHITE, the finished Day 9 Remus in `00 WHITE - No enhancements` beside it, plus this one enhancement. The student pair writes `search_later_move()` in `search.py`, `test_pvs_search_agrees_with_alpha_beta()` in `test_upgrades.py`, `test_a_null_window_answers_only_better_or_not()` in `test_upgrades.py`.

## The changes and why

### `search_later_move()` in `search.py`

Searches a later move with a null window first, which only answers "better or not?", and searches again with the full window only on a surprise. Most later moves are worse, so the cheap question is usually enough.

### `test_pvs_search_agrees_with_alpha_beta()` in `test_upgrades.py`

PVS must be a faster way to the same answer, never a different answer. The test searches one position with the Day 9 search and with PVS and compares the scores, and checks that the position is unchanged afterward.

### `test_a_null_window_answers_only_better_or_not()` in `test_upgrades.py`

Shows what a null window really returns. With a window one point wide, the score only says whether the exact score is above alpha or not, so the test tries an alpha 50 below the exact score and one 50 above it. That yes-or-no answer is why PVS must search again when a move surprises it.

## Check it

Check the work by opening `run_tests.py` in this folder and pressing Run. Then open `smoke_test.py` in VS Code and press Run: Remus-PINK plays one 2-minute game against Remus-WHITE, which shows that the engine plays legal moves to the end of a game. In the Day 9 battles, follow the numbered steps at the top of `play_battle.py`: copy the visiting student pair's engine folder into `engines/student`, set `VISITING_ENGINE` to the visitor's engine color, and press Run. Remus-PINK plays it twice at 10 minutes a side, once with each piece color, and both games go into misc/games/remus_games.pgn. Each script runs `version_match.py` from the folder above this one.

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `search_later_move()` | 396 | 6 | `run_tests.py` |
| `test_upgrades.py` | `test_pvs_search_agrees_with_alpha_beta()` | 14 | 7 | `run_tests.py` |
| `test_upgrades.py` | `test_a_null_window_answers_only_better_or_not()` | 25 | 5 | `run_tests.py` |

Lines to type in all: 18. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `search_later_move()` in `search.py`

**Where:** lines 423 to 428 of `search.py`, inside `search_later_move()`, in place of the stub below the docstring. It is called by `pvs_search()` in `search.py`.

```text
396 | def search_later_move(
      ...
421 |         the full window to find the exact score.
422 |     """
423 +     score, line = pvs_search(state, depth, ply, -alpha - 1, -alpha, info)
424 +     score = -score
425 +     if alpha < score < beta:  # A surprise: search it again with the full window
426 +         score, line = pvs_search(state, depth, ply, -beta, -alpha, info)
427 +         score = -score
428 +     return score, line
429 |
430 |
431 | def pvs_search(
```

**How it works:** This is the heart of principal variation search. The first call to `pvs_search` uses a null window, `-alpha - 1` to `-alpha`, a window one point wide. It costs little and answers one question: is this move better than the best move so far? The minus signs flip the window and the score, as in every negamax call. If the score lands strictly between `alpha` and `beta`, the move surprised us by being better, so the code searches it again with the full window, `-beta` to `-alpha`, to learn its exact score. Most moves are not better, so most moves need only the cheap search.

### `test_pvs_search_agrees_with_alpha_beta()` in `test_upgrades.py`

**Where:** lines 16 to 22 of `test_upgrades.py`, inside `test_pvs_search_agrees_with_alpha_beta()`, in place of the stub below the docstring. `run_tests.py` runs it with every other test in the folder.

```text
14 | def test_pvs_search_agrees_with_alpha_beta() -> None:
15 |     """The color version saves work but finds the same score at the same depth."""
16 +     state = state_from_fen(ITALIAN)
17 +     before = state_snapshot(state)
18 +     plain_score, _ = alpha_beta_with_quiescence(state, 3, 0, *WIDE, SearchInfo())
19 +     score, pv = pvs_search(state, 3, 0, *WIDE, SearchInfo())
20 +     assert score == plain_score
21 +     assert pv
22 +     assert state_snapshot(state) == before
23 |
24 |
25 | def test_a_null_window_answers_only_better_or_not() -> None:
```

**How it works:** The test runs the plain search, `alpha_beta_with_quiescence`, and the color version's `pvs_search` on the Italian opening at depth 3. The asserts check that both find the same score, that PVS returns a line of moves, and that the state snapshot is unchanged, which proves the search undid every move it made. `*WIDE` unpacks the pair of numbers into `alpha` and `beta`.

### `test_a_null_window_answers_only_better_or_not()` in `test_upgrades.py`

**Where:** lines 27 to 31 of `test_upgrades.py`, inside `test_a_null_window_answers_only_better_or_not()`, in place of the stub below the docstring. `run_tests.py` runs it with every other test in the folder.

```text
25 | def test_a_null_window_answers_only_better_or_not() -> None:
26 |     """A null window (alpha, alpha + 1) says only whether the exact score beats alpha."""
27 +     state = state_from_fen(ITALIAN)
28 +     exact, _ = pvs_search(state, 3, 0, *WIDE, SearchInfo())
29 +     for alpha in (exact - 50, exact + 50):
30 +         score, _ = pvs_search(state, 3, 0, alpha, alpha + 1, SearchInfo())
31 +         assert (score > alpha) == (exact > alpha)
```

**How it works:** First the test finds the exact score with the wide window. Then it tries two null windows, one 50 points below the exact score and one 50 points above. A null-window search does not promise the exact score, only the right side of `alpha`: the assert checks that `score > alpha` agrees with `exact > alpha` both times.
