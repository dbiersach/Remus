# Remus-ORANGE: Null-move pruning

Let the opponent move twice in a shallow search. If Remus is still too far ahead, the opponent would never allow this position, so stop searching it.

## Learning objectives

By the end of Day 9, each student pair can:

- Explain the idea of the color version's enhancement in two sentences. **Measured by:** The student pair explains the idea to another student pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `run_tests.py` passes in the version folder.
- Run a fair experiment: same opening, both piece colors. **Measured by:** In the Day 9 battles, `play_battle.py` in the version folder plays both 10-minute games with no illegal moves or crashes when the student pair presses Run in VS Code, and the student pair says why two games cannot show which enhancement is stronger.

## The idea, with an example

Somewhere in the search, Remus is a knight ahead in a line it is checking. Earlier in the tree, the opponent already found a different move that keeps the game even. That earlier choice is beta: any line better for Remus than beta, the opponent will simply avoid. Before searching its 35 real moves here, Remus-ORANGE tries a cheap test. It passes, so the opponent gets two moves in a row, and searches 2 plies shallower than usual. If Remus still scores at least beta after giving away a whole move, then a real move would do even better, because moving is almost always better than passing. The opponent will never allow this position, so Remus stops searching it without trying one real move.

## Why it makes Remus stronger

Most positions deep in a search are lopsided, and the null move removes them with one shallow search instead of a full one. The positions saved go into searching the close lines one ply deeper.

## What it costs

An extra shallow search at every position 3 or more plies from the leaves, which is wasted when the test fails. The test can also be wrong. In zugzwang, every legal move makes the position worse, and passing would be the best move if it were allowed; this happens mostly in pawn endings. So Remus never passes when it is in check, when it has only king and pawns, right after a pass, or at the root.

## Measured against Remus-WHITE

Each version searched the ten positions of `compare_search.py`, one depth at a time up to depth 4, on one computer. Fewer positions for the same depth means a smaller search tree. Positions per second shows what each position costs. The last column gave each position 5 seconds, the way a game does, and averages the deepest search that finished.

| Version | Positions to finish depth 4 | Share of Remus-WHITE's | Positions per second | Average depth in 5 seconds |
| --- | ---: | ---: | ---: | ---: |
| Remus-WHITE | 431,212 | 100% | 5,183 | 3.1 |
| Remus-ORANGE | 273,470 | 63% | 5,709 | 3.5 |

## What to expect

Far fewer positions for the same depth once the search reaches depth 3 and deeper, and the same moves in most positions. The saving grows with depth, so null moves help most at longer clocks.

## Where your code fits

`null_move_search()` in `search.py` calls `make_null_move()`, searches the pass with the window (-beta, -beta + 1) at `depth - 1 - NULL_MOVE_REDUCTION`, and calls `undo_null_move()` in a `finally` block. A pass changes the side to move, clears the en passant target, and adds a history entry, and `undo_null_move()` must restore all three exactly, like every undo in Remus.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus in `period1`, plus this one enhancement. The student pair writes `make_null_move()` in `search.py`, `undo_null_move()` in `search.py`, `test_null_move_and_undo_restore_the_state()` in `test_upgrades.py`, `test_null_move_search_saves_work_and_keeps_the_state()` in `test_upgrades.py`.

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

Check the work by opening `run_tests.py` in this folder and pressing Run. Then open `smoke_test.py` in VS Code and press Run: Remus-ORANGE plays one 2-minute game against Remus-WHITE, which shows that the engine plays legal moves to the end of a game. In the Day 9 battles, follow the numbered steps at the top of `play_battle.py`: copy the visiting student pair's engine folder into the `engines` folder, set `VISITING_ENGINE` to the visitor's engine color, and press Run. Remus-ORANGE plays it twice at 10 minutes a side, once with each piece color, and both games go into misc/games/remus_games.pgn. Each script runs `version_match.py` from the `engines` folder above this one.

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `make_null_move()` | 398 | 5 | `test_upgrades.py::test_null_move_and_undo_restore_the_state` |
| `search.py` | `undo_null_move()` | 418 | 3 | `test_upgrades.py::test_null_move_and_undo_restore_the_state` |
| `test_upgrades.py` | `test_null_move_and_undo_restore_the_state()` | 21 | 6 | `run_tests.py` |
| `test_upgrades.py` | `test_null_move_search_saves_work_and_keeps_the_state()` | 30 | 9 | `run_tests.py` |

Lines to type in all: 23. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
