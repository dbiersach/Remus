# Remus Program Overview

Remus is a chess engine in plain Python, built over ten workshop days. This page shows
how the pieces fit together. Each major script has its own page in
[`scripts/`](scripts/), and [`slide_plan.md`](slide_plan.md) lists the slides that
picture the data structures and the program flow.
[`lucas_chess_guide.md`](lucas_chess_guide.md) shows how to run Remus in Lucas Chess,
the chess app on every class laptop.

## How the code is organized

Each day of the workshop has its own folder inside `instructor/`, and each Day folder
holds four period folders, `period1` to `period4`, one for each class period:

| Folder | What the new code does compared to the day before |
| --- | --- |
| `Day 01 - Draw the board` | Holds the board as an 8x8 list and converts square names |
| `Day 02 - Make and undo moves` | Adds the game state, the `Move` record, and exact make and undo |
| `Day 03 - Generate piece moves` | Lists every move each piece can make by its movement rules |
| `Day 04 - Keep only legal moves` | Finds attacked squares and drops moves that leave the king in check |
| `Day 05 - Add castling, en passant, and promotion` | Completes the rules of movement |
| `Day 06 - Count positions and read FEN` | Proves the rules right by counting positions against published totals, then reads and writes FEN |
| `Day 07 - Play full games and score positions` | Adds game endings, SAN, two simple brains, the UCI link to the GUI, and the evaluation |
| `Day 08 - Search ahead with alpha-beta` | Looks ahead with minimax and negamax, then prunes with alpha-beta, searches captures to quiet positions, and orders moves |
| `Day 09 - Add the clock and build the stations` | Thinks on a clock with iterative deepening (Remus-WHITE), builds the ten enhancement stations, and adds a mate solver |
| `Day 10 - Aim Remus at a science problem` | Holds all ten enhancements, the hidden-peak and beam time Science AI, and the tournament |

The Day folders live inside the root `instructor/` folder. `instructor/` holds only
finished reference code that runs as it is, with no blanks to fill in, so the solution
code stays apart from the code students write and change. Every period folder is a
complete, runnable copy of Remus as it stands at the end of that period, and its
`README.md` names the period, its learning objectives with how each is measured, the
files that are new or growing, the functions the pairs write, and a paragraph on each
change and why (the text comes from `period_guides.py`). `period4` holds the finished code of the day. `make_period_folders.py`
builds `period1` to `period3` from it, so a file that grows during the day, such as
`make_move.py` on Day 5, gains castling in `period2`, en passant in `period3`, and
promotion in `period4`.

`student/` mirrors `instructor/`. In each student period folder, the functions the class
writes in that period are stubs that raise `NotImplementedError`, and the tests fail
until a pair writes them. `make_student_folders.py` builds `student/` and lists every
student function; `student/README.md` shows the same list. A student who opens
`Day 06 - Count positions and read FEN/period2` finds every file from Days 1 to 5, some of
them grown, plus `perft.py` with `perft()` left to write. Nothing in a period folder
imports from another folder.

[`file_versions.md`](file_versions.md) lists when each file first appears and what
each later day changes in it, by file and by day.

### The naming rule for newer versions

A module keeps one file name from the day it appears to Day 10. When a later lesson
makes a file smarter, the new code goes into the same file under a new function name,
next to the function it improves. The old function stays, so students can run both and
compare them.

| File | Simpler version | Smarter version beside it | Day |
| --- | --- | --- | --- |
| `attacks.py` | `is_attacked_by_scanning` (ask every enemy piece) | `is_square_attacked` (look outward from the square) | 4 |
| `search.py` | `random_move`, `greedy_move` | `minimax`, then `negamax` | 7, 8 |
| `search.py` | `negamax` | `alpha_beta`, then `alpha_beta_with_quiescence` | 8 |
| `search.py` | `alpha_beta_with_quiescence` | `upgraded_search` | 10 |
| `evaluation.py` | `material`, `placement` | adds `pawn_structure`, `mating_bonus`, `king_safety` | 7, 10 |
| `move_ordering.py` | captures by MVV-LVA | adds killer moves | 8, 10 |

Imports never break, because no file is ever renamed. A script that called `negamax` on
Day 8 still finds `negamax` on Day 10.

### Running the code

Run a script from inside its period folder, or give its path:

```bash
uv run "instructor/Day 06 - Count positions and read FEN/period4/perft.py"
```

Every script prints its own check, with the expected answer beside it. Tests sit next
to the modules. Because each period folder repeats the same module names, pytest runs
one folder at a time:

```bash
uv run pytest "instructor/Day 04 - Keep only legal moves/period3"
uv run run_all_tests.py
```

`run_all_tests.py` runs every period folder in `instructor/` in turn, then the reference-tool tests in
`tests/`.

## The puzzle box and its pieces

Think of this page as the picture on a jigsaw puzzle box. Each `.py` file is one
piece. Each piece has its own page in [`scripts/`](scripts/). A page starts with the
big picture, then shows where the piece fits, its call tree, and what each function
does.

The pieces stack up. Each file uses the ones above it in this map:

```text
board.py                     the grid of squares
game_state.py, moves.py      whose turn it is, what a move looks like
make_move.py                 play a move and take it back
move_generation.py           every move the pieces can make
attacks.py, legal_moves.py   keep only the legal moves
fen.py, notation.py          read and write positions and moves
game_end.py                  is the game over?
evaluation.py                how good is a position?
move_ordering.py, transposition_table.py, opening_book.py
search.py                    choose a move
uci_engine.py                talk to Lucas Chess
```

The pages, in the order the class builds them:

| Page | What the file does |
| --- | --- |
| [`python_setup.py`](scripts/python_setup.md) | Day 1 lab: is the laptop ready? |
| [`python_strings.py`](scripts/python_strings.md) | Day 1 lab: square names are text |
| [`python_lists.py`](scripts/python_lists.md) | Day 1 lab: a board is a list of rows |
| [`board.py`](scripts/board.md) | The chessboard |
| [`show_board.py`](scripts/show_board.md) | Draw the board and its moves as a picture |
| [`python_functions.py`](scripts/python_functions.md) | Day 2 lab: small functions and their tests |
| [`python_dicts.py`](scripts/python_dicts.md) | Day 2 lab: a dict, a copy, and a dataclass |
| [`game_state.py`](scripts/game_state.md) | Everything the board does not show |
| [`moves.py`](scripts/moves.md) | What a move looks like |
| [`make_move.py`](scripts/make_move.md) | Make a move, then take it back |
| [`python_loops.py`](scripts/python_loops.md) | Day 3 lab: walk until something stops you |
| [`move_generation.py`](scripts/move_generation.md) | Every move the pieces can make |
| [`python_modules.py`](scripts/python_modules.md) | Day 4 lab: one file uses another |
| [`attacks.py`](scripts/attacks.md) | Is this square under attack? |
| [`legal_moves.py`](scripts/legal_moves.md) | Keep only the legal moves |
| [`demo_practice_positions.py`](scripts/demo_practice_positions.md) | Day 4 demo: predict, then count the legal moves |
| [`python_sets.py`](scripts/python_sets.md) | Day 5 lab: castling rights as letters |
| [`demo_promotion.py`](scripts/demo_promotion.md) | Day 5 demo: why a pawn becomes a knight |
| [`python_recursion.py`](scripts/python_recursion.md) | Day 6 lab: a function that calls itself |
| [`perft.py`](scripts/perft.md) | Count positions to prove the rules |
| [`hunt.py`](scripts/hunt.md) | Day 6 demo: find three planted bugs |
| [`python_fen_fields.py`](scripts/python_fen_fields.md) | Day 6 lab: the six fields of FEN |
| [`fen.py`](scripts/fen.md) | A whole position in one line |
| [`notation.py`](scripts/notation.md) | Moves the way people write them |
| [`game_end.py`](scripts/game_end.md) | Is the game over? |
| [`console_game.py`](scripts/console_game.md) | Play chess in the terminal |
| [`python_input_output.py`](scripts/python_input_output.md) | Day 7 lab: read commands, answer at once |
| [`uci_engine.py`](scripts/uci_engine.md) | Talk to Lucas Chess |
| [`play_match.py`](scripts/play_match.md) | Two Remus brains play each other |
| [`evaluation.py`](scripts/evaluation.md) | How good is this position? |
| [`search.py`](scripts/search.md) | Choosing a move |
| [`python_sorting.py`](scripts/python_sorting.md) | Day 8 lab: sort, start at minus infinity, time it |
| [`compare_search.py`](scripts/compare_search.md) | Prove that alpha-beta saves work |
| [`move_ordering.py`](scripts/move_ordering.md) | Try the best moves first |
| [`python_caches.py`](scripts/python_caches.md) | Day 9 lab: remember answers in a dict |
| [`transposition_table.py`](scripts/transposition_table.md) | Remember positions already searched |
| [`opening_book.py`](scripts/opening_book.md) | Play known openings without thinking |
| [`mate_solver.py`](scripts/mate_solver.md) | Solve mate-in-two puzzles |
| [`tournament.py`](scripts/tournament.md) | The class round robin |
| [`estimate_elo.py`](scripts/estimate_elo.md) | Measures the Elo rating of Remus against Stockfish |
| [`demo_results.py`](scripts/demo_results.md) | Day 10 demo: read a match result and explain a move |
| [`station_match.py`](stations.md) | Measures one enhancement station against Remus-WHITE, the Day 9 Remus with no enhancements |
| [`station_league.py`](stations.md) | Ranks all 12 Remus versions with a round robin and one fitted Elo rating each |
| [`hidden_peak.py`](scripts/hidden_peak.md) | Science AI: find the hidden peak |
| [`beam_time.py`](scripts/beam_time.md) | Science AI: plan the beam time |
| [The test files](scripts/tests.md) | Checking that Remus works |

## The four boundaries

| Part | Files | Responsibility |
| --- | --- | --- |
| Native Python engine | `board.py` to `search.py` | Board, rules, legal moves, state, search, evaluation, move choice |
| Console driver | `console_game.py` | Prints the board and reads SAN moves typed in the terminal |
| UCI adapter | `uci_engine.py`, `remus.bat` | Speaks UCI with Lucas Chess on standard input and output |
| Teacher tools | `play_match.py`, `compare_search.py`, `tournament.py`, `estimate_elo.py`, `Stations/station_match.py`, `Stations/station_league.py`, tests | Use `python-chess` as an outside referee; the engine never imports it |

## The core data structures

**The board** is a list of 8 rows, each a list of 8 one-character strings. Row 0 is
rank 8 and column 0 is file a, so `board[6][4]` is e2, which holds `"P"` at the start.
Uppercase letters are White, lowercase letters are Black, and `"."` is an empty square.

**A square** is a `(row, col)` tuple inside the engine. Square names such as `"e2"`
appear only at the edges: printing, FEN, SAN, and UCI.

**The game state** is a dict:

```python
state = {
    "board": board,             # 8x8 list of lists
    "turn": "w",                # "w" or "b"
    "castling": "KQkq",         # Castling rights still allowed
    "en_passant": None,         # The square a pawn skipped, such as (5, 4) for e3
    "halfmove_clock": 0,        # Moves since the last capture or pawn move
    "fullmove_number": 1,       # Goes up after each Black move
    "history": [key],           # position_key of every position so far (Day 7)
}
```

**A move** is a frozen dataclass `Move(from_square, to_square, promotion)`. The move
e2-e4 is `Move((6, 4), (4, 4))`, and a pawn promoting to a queen on e8 is
`Move((1, 4), (0, 4), "Q")`.

**An undo record** is a dict that `make_move` returns. It holds the moved piece, the
captured piece, the old castling rights, the old en passant square, both old clocks,
the rook's squares for castling, and the victim's square for en passant.
`undo_move(state, undo)` puts every one of them back.

## Program flow: from a GUI command to a move

When Lucas Chess asks Remus for a move, the work runs through the modules in this
order:

1. `uci_engine.py` reads `position startpos moves e2e4 e7e5` and builds the state with
   `fen.state_from_fen` and `make_move`.
2. On `go wtime 60000 ...`, `thinking_time` turns the clock into seconds to think.
3. Out of the opening book, `search.think` runs iterative deepening: depth 1, 2, 3,
   and on, until time runs out.
4. Each depth calls `upgraded_search` (Day 10) or `alpha_beta_with_quiescence` (Day 8).
   The search calls `legal_moves`, which calls `pseudo_legal_moves`,
   `castling_moves`, `make_move`, `in_check`, and `undo_move` for every candidate.
5. At depth 0, `quiescence` keeps searching captures until the position is quiet, then
   `evaluation.evaluate` scores it.
6. Each finished depth sends an `info` line with the score and principal variation.
7. `uci_engine.py` sends `bestmove g1f3`.

The search makes and undoes moves on the one live state. A `try/finally` around every
`make_move` guarantees the undo, even when the clock stops the search in the middle.

## Rules and checks that hold on every day

1. `undo_move(state, make_move(state, move))` restores the whole state, compared as
   text by `state_snapshot`.
2. From Day 6 on, `perft` matches the published counts: 20, 400, 8,902, and 197,281
   from the start position, and the "Kiwipete" position's 97,862 at depth 3.
3. The engine imports only the Python standard library.
4. Every script prints a result next to the expected answer.

## Niram-GOLD, the Rust copy

`niram/` holds Niram-GOLD, Remus-GOLD rewritten in Rust with the same rules,
evaluation, and search. On the same positions and depth it visits exactly as many
positions as Remus-GOLD and picks the same moves, about 50 times faster: some 200,000
positions a second against about 4,000. See [`niram/README.md`](../niram/README.md).

## Where the ideas come from

Remus borrows its approach from Turbo GameWorks Chess 4.0 (Borland, 1987) without
copying its code:

| GameWorks idea | Remus |
| --- | --- |
| Piece values 256, 768, 768, 1216, 2304 | Centipawns 100, 300, 300, 500, 900 (`evaluation.py`) |
| `Attacks` asks each piece about a square | `is_attacked_by_scanning` (`attacks.py`) |
| `KillingMove` | `remember_killer` and `KILLER_SCORE` |
| `PawnStrVal`, `PassPawnRank` | `pawn_structure` |
| `Mating` mode and `DistAn` | `mating_bonus` and `CENTER_DISTANCE` |
| Zero-window search | Principal variation search in `upgraded_search` |
| `OPENING.LIB` | `opening_book.txt`, written in SAN |
| `MATE.001` to `MATE.010` | `tests/mate_puzzles.epd` and `mate_solver.py` |

## Science AI

`hidden_peak.py` reuses the engine's loop of "list the candidates, score each one,
choose the best" to choose where to measure next on a 10x10 sample. A greedy AI with an
exploration term finds the hidden peak in about 9 measurements, against about 54 for
random guessing. See [`scripts/hidden_peak.md`](scripts/hidden_peak.md).

`beam_time.py` aims the same loop at a beamline problem: 40 one-minute shots of
X-rays for 8 samples, where each sample needs a yes-or-no call. The agent looks one
shot ahead with three pretend readings and measures the sample whose next shot lowers
the chance of a wrong call the most. Over 200 sample holders it makes about 0.65 wrong
calls per holder, against 0.83 for equal time and 0.94 for random samples. See
[`scripts/beam_time.md`](scripts/beam_time.md).
