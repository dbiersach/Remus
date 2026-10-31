# Remus-ORANGE: Null-move pruning

Let the opponent move twice in a shallow search. If Remus is still too far ahead, the opponent would never allow this position, so stop searching it.

## Learning objectives

By the end of Day 9, each student pair can:

- Explain the idea of this enhancement in two sentences. **Measured by:** The student pair explains the idea to another student pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `run_tests.py` passes in the version folder.
- Run a fair experiment: same opening, both piece colors. **Measured by:** In the Day 9 battles, `play_battle.py` in the version folder plays both 10-minute games with no illegal moves or crashes when the student pair presses Run in VS Code, and the student pair says why two games cannot show which enhancement is stronger.

## The idea, with an example

Somewhere in the search, Remus is a knight ahead in a line it is checking. Earlier in the tree, the opponent already found a different move that keeps the game even. That earlier choice is beta: any line better for Remus than beta, the opponent will simply avoid. Before searching its 35 real moves here, Remus-ORANGE tries a cheap test. It passes, so the opponent gets two moves in a row, and searches 2 plies shallower than usual. If Remus still scores at least beta after giving away a whole move, then a real move would do even better, because moving is almost always better than passing. The opponent will never allow this position, so Remus stops searching it without trying one real move.

## Why it makes Remus stronger

Most positions deep in a search are lopsided, and the null move removes them with one shallow search instead of a full one. The positions saved go into searching the close lines one ply deeper.

## What it costs

An extra shallow search at every position 3 or more plies from the leaves, which is wasted when the test fails. The test can also be wrong. In zugzwang, every legal move makes the position worse, and passing would be the best move if it were allowed; this happens mostly in pawn endings. So Remus never passes when it is in check, when it has only king and pawns, right after a pass, or at the root.

## Measured against Remus-WHITE

Each version searched the ten positions of the designer's benchmark, `misc/designer/remus_benchmark.py`, one depth at a time up to depth 4, on one computer. Fewer positions for the same depth means a smaller search tree. Positions per second shows what each position costs. The last column gave each position 5 seconds, the way a game does, and averages the deepest search that finished.

| Version | Positions to finish depth 4 | Share of Remus-WHITE's | Positions per second | Average depth in 5 seconds |
| --- | ---: | ---: | ---: | ---: |
| Remus-WHITE | 431,212 | 100% | 5,183 | 3.1 |
| Remus-ORANGE | 273,470 | 63% | 5,709 | 3.5 |

## What to expect

Far fewer positions for the same depth once the search reaches depth 3 and deeper, and the same moves in most positions. The saving grows with depth, so null moves help most at longer clocks.

## Where your code fits

`null_move_search()` in `search.py` calls `make_null_move()`, searches the pass with the window (-beta, -beta + 1) at `depth - 1 - NULL_MOVE_REDUCTION`, and calls `undo_null_move()` in a `finally` block. A pass changes the side to move, clears the en passant target, and adds a history entry, and `undo_null_move()` must restore all three exactly, like every undo in Remus.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus in `00 Remus-WHITE - No enhancements` beside it, plus this one enhancement. The student pair writes `make_null_move()` in `search.py`, `undo_null_move()` in `search.py`, `test_null_move_and_undo_restore_the_state()` in `test_upgrades.py`, `test_null_move_search_saves_work_and_keeps_the_state()` in `test_upgrades.py`.

## The changes and why

### `make_null_move()` in `search.py`

Passes the turn without moving a piece, and returns the en passant target so it can be put back. The opponent then moves twice in a row, and if Remus still scores at least beta, the opponent would never allow the position, so the search can stop early.

### `undo_null_move()` in `search.py`

Takes the pass back: removes its history entry, gives the turn back, and restores the en passant target. Like every undo in Remus, it must restore the state exactly.

### `test_null_move_and_undo_restore_the_state()` in `test_upgrades.py`

Makes a pass and takes it back, then compares the whole state with the start. A null move that leaves one thing changed, such as the en passant target, would corrupt every search after it.

### `test_null_move_search_saves_work_and_keeps_the_state()` in `test_upgrades.py`

Counts positions: the null-move search must visit fewer than the Day 9 search at the same depth and leave the position unchanged. The count is the evidence that the pass saves work.

## Check it

Check the work by opening `run_tests.py` in this folder and pressing Run. Then open `basic_test.py` in VS Code and press Run: Remus-ORANGE plays one 2-minute game against Remus-WHITE, which shows that the engine plays legal moves to the end of a game. In the Day 9 battles, follow the numbered steps at the top of `play_battle.py`: copy the visiting student pair's engine folder into `engines/student`, set `VISITING_ENGINE` to the visitor's engine color, and press Run. Remus-ORANGE plays it twice at 10 minutes a side, once with each piece color, and both games go into misc/games/remus_games.pgn. Each script runs `misc/designer/version_match.py`, which plays the games.

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `make_null_move()` | 400 | 5 | `test_upgrades.py::test_null_move_and_undo_restore_the_state` |
| `search.py` | `undo_null_move()` | 422 | 3 | `test_upgrades.py::test_null_move_and_undo_restore_the_state` |
| `test_upgrades.py` | `test_null_move_and_undo_restore_the_state()` | 21 | 6 | `run_tests.py` |
| `test_upgrades.py` | `test_null_move_search_saves_work_and_keeps_the_state()` | 31 | 9 | `run_tests.py` |

Lines to type in all: 23. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `make_null_move()` in `search.py`

**Where:** lines 415 to 419 of `search.py`, inside `make_null_move()`, in place of the stub below the docstring. It is called by `null_move_search()` in `search.py`.

```python
400 | def make_null_move(state: dict) -> Square | None:
401 |     """
      ...
413 |         The en passant target before the null move, which undo_null_move restores.
414 |     """
415 +     en_passant = state["en_passant"]
416 +     state["turn"] = opponent(state["turn"])
417 +     state["en_passant"] = None
418 +     state["history"].append(position_key(state))
419 +     return en_passant
420 |
421 |
422 | def undo_null_move(state: dict, en_passant: Square | None) -> None:
```

**How it works:** A null move is a pass: the side to move gives the turn away without moving a piece. The function saves the en passant target first, because the undo needs it back. `opponent` flips the turn from "w" to "b" or back. A pass cancels any en passant capture, so the target becomes None. The new position's key goes onto the history, so the repetition rules still see every position the search visits, and the saved target is returned for `undo_null_move`.

### `undo_null_move()` in `search.py`

**Where:** lines 424 to 426 of `search.py`, inside `undo_null_move()`, in place of the stub below the docstring. It is called by `null_move_search()` in `search.py`.

```python
422 | def undo_null_move(state: dict, en_passant: Square | None) -> None:
423 |     """Take back a null move, restoring the side to move and the en passant target."""
424 +     state["history"].pop()
425 +     state["turn"] = opponent(state["turn"])
426 +     state["en_passant"] = en_passant
427 |
428 |
429 | def has_pieces(board: Board, color: str) -> bool:
```

**How it works:** The undo takes the three steps of `make_null_move` back in reverse order: it removes the last history key, flips the turn back, and puts back the en passant target that `make_null_move` returned.

### `test_null_move_and_undo_restore_the_state()` in `test_upgrades.py`

**Where:** lines 23 to 28 of `test_upgrades.py`, inside `test_null_move_and_undo_restore_the_state()`, in place of the stub below the docstring. `run_tests.py` runs it with every other test in the folder.

```python
21 | def test_null_move_and_undo_restore_the_state() -> None:
22 |     """Expected: a pass gives Black the turn, and its undo restores the exact state."""
23 +     state = state_from_fen(ITALIAN)
24 +     before = state_snapshot(state)
25 +     en_passant = make_null_move(state)
26 +     assert state["turn"] == "b"
27 +     undo_null_move(state, en_passant)
28 +     assert state_snapshot(state) == before
29 |
30 |
31 | def test_null_move_search_saves_work_and_keeps_the_state() -> None:
```

**How it works:** The test takes a snapshot of the Italian opening, makes a null move, and checks that Black now has the turn. After `undo_null_move` the snapshot must match exactly: same board, turn, en passant target, clocks, and history.

### `test_null_move_search_saves_work_and_keeps_the_state()` in `test_upgrades.py`

**Where:** lines 33 to 41 of `test_upgrades.py`, inside `test_null_move_search_saves_work_and_keeps_the_state()`, in place of the stub below the docstring. `run_tests.py` runs it with every other test in the folder.

```python
31 | def test_null_move_search_saves_work_and_keeps_the_state() -> None:
32 |     """The upgraded search visits fewer positions than plain alpha-beta at depth 4."""
33 +     state = state_from_fen(ITALIAN)
34 +     before = state_snapshot(state)
35 +     plain = SearchInfo()
36 +     upgraded = SearchInfo()
37 +     alpha_beta_with_quiescence(state, 4, 0, *WIDE, plain)
38 +     _, pv = null_move_search(state, 4, 0, *WIDE, upgraded)
39 +     assert upgraded.nodes < plain.nodes
40 +     assert pv
41 +     assert state_snapshot(state) == before
```

**How it works:** Two `SearchInfo` records count positions: `plain` for ordinary alpha-beta and `upgraded` for the null-move search, both at depth 4 on the Italian opening. The asserts check that the upgraded search visits fewer positions, that it returns a line of moves, and that the state snapshot is unchanged afterward.
