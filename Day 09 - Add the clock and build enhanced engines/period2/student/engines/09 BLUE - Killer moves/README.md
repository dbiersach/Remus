# Remus-BLUE: Killer moves

Try quiet moves that caused a cutoff at the same depth right after the captures.

## Learning objectives

By the end of Day 9, each pair can:

- Explain the idea of the color version's enhancement in two sentences. **Measured by:** The pair explains the idea to another pair, who can restate it.
- Add the enhancement without breaking the rules. **Measured by:** `run_tests.py` passes in the version folder.
- Run a fair experiment: same opening, both piece colors. **Measured by:** In the Day 9 battles, `play_battle.py` in the version folder plays both 10-minute games with no illegal moves or crashes when the pair presses Run in VS Code, and the pair says why two games cannot show which enhancement is stronger.

## The idea, with an example

Black has just made a weak move, and White's quiet move Qh5 threatens mate on f7. Deep in the search, the same Qh5 refutes many different Black moves at the same ply: almost any Black move that does not defend f7 loses to it. Remus-WHITE tries the captures first, then the quiet moves in the order the generator found them, so it may try 20 quiet moves before Qh5 each time. Remus-BLUE remembers Qh5 as a killer move for that ply, because it caused a cutoff there, and tries it right after the captures in every other position at the same ply.

## Why it makes Remus stronger

Alpha-beta cuts off a position as soon as one move is good enough to refute it. The sooner that move comes, the fewer moves are searched. Captures are easy to rank by value, but quiet moves have no such order. Killers give the quiet moves an order learned from the search itself.

## What it costs

Very little: two moves stored per ply, and a check whether each quiet move is one of them while ordering. Positions per second stay close to Remus-WHITE's.

## Measured against Remus-WHITE

Each version searched the ten positions of `compare_search.py`, one depth at a time up to depth 4, on one computer. Fewer positions for the same depth means a smaller search tree. Positions per second shows what each position costs. The last column gave each position 5 seconds, the way a game does, and averages the deepest search that finished.

| Version | Positions to finish depth 4 | Share of Remus-WHITE's | Positions per second | Average depth in 5 seconds |
| --- | ---: | ---: | ---: | ---: |
| Remus-WHITE | 431,212 | 100% | 5,183 | 3.1 |
| Remus-BLUE | 328,889 | 76% | 4,998 | 3.4 |

## What to expect

Fewer positions for the same depth, most of all in quiet middlegame positions with many moves. A killer that is a capture or a promotion is not stored, because captures and promotions are already ordered first.

## Where your code fits

`killer_search()` in `search.py` calls `remember_killer()` whenever a quiet move causes a cutoff, and passes the killers of the next ply to `order_moves()` in `move_ordering.py`. `order_moves()` scores captures by MVV-LVA, gives a killer `KILLER_SCORE` (50, below every capture and above every other quiet move), and puts the best move of the last depth in front of them all.

## The files

This folder is Remus-WHITE, the finished Day 9 Remus in `period1`, plus this one enhancement. The pair writes `remember_killer()` in `search.py`, `order_moves()` in `move_ordering.py`, `test_killers_keep_two_quiet_moves()` in `test_upgrades.py`.

## The changes and why

### `remember_killer()` in `search.py`

Keeps up to two quiet moves per ply that caused a cutoff. A move that refuted one position often refutes its neighbors, so trying it early saves work.

### `order_moves()` in `move_ordering.py`

Sorts the moves so captures come first by MVV-LVA, then this ply's killer moves, then every other move. The earlier a good move comes, the sooner alpha-beta cuts off the rest.

### `test_killers_keep_two_quiet_moves()` in `test_upgrades.py`

Feeds three cutoff moves to `remember_killer()` and checks that only the two newest stay, newest first. Writing the expected list before running the test is how a pair shows it understands the two slots.

## Check it

Check the work by opening `run_tests.py` in this folder and pressing Run. Then open `smoke_test.py` in VS Code and press Run: Remus-BLUE plays one 2-minute game against Remus-WHITE, which shows that the engine plays legal moves to the end of a game. In the Day 9 battles, copy the visiting pair's color folder into the `engines` folder, open `play_battle.py`, press Run, and type the visitor's engine color: Remus-BLUE plays it twice at 10 minutes a side, once with each piece color, and both games go into misc/games/remus_games.pgn. Each script runs `version_match.py` from the `engines` folder above this one.

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `remember_killer()` | 397 | 6 | `test_upgrades.py::test_killers_keep_two_quiet_moves` |
| `move_ordering.py` | `order_moves()` | 52 | 16 | `test_search.py::test_capture_moves_and_mvv_lva` |
| `test_upgrades.py` | `test_killers_keep_two_quiet_moves()` | 21 | 5 | `run_tests.py` |

Lines to type in all: 27. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
