# Remus3: Remus2 with the biggest gains

Remus3 is [Remus2](../Remus2/README.md) with the eleven enhancements that buy the most
strength for the fewest lines: killer moves, pawn structure, a position key and a
transposition table, an opening book, aspiration windows, time management, null-move
pruning, the principal variation, the bishop pair, and the rook table. The student
pairs type the 193 new lines into their Remus2. It speaks UCI to Lucas Chess
through `remus.bat` and uses only the standard library.

[`remus_versions.md`](../remus_versions.md) explains each step and
why Remus3 holds it. [Remus4](../Remus4/README.md) adds every other enhancement.

## Files

| File | Code lines | What it does | New in Remus3 |
| --- | ---: | --- | --- |
| `board.py` | 23 | The piece numbers, the starting position, square names, the position key, and UCI move text | `MATE_SCORE`, `position_key()`, `move_text()` |
| `make_move.py` | 23 | Play a move on a copy of the board | |
| `attacks.py` | 34 | Is a square attacked? Is a king in check? | |
| `move_generation.py` | 65 | List the moves of the side to move, castling included | |
| `evaluation.py` | 115 | Material, five piece-square tables, the pawn structure, and the bishop pair | `ROOK_TABLE`, `pawn_terms()`, the bishop pair |
| `transposition_table.py` | 22 | Remember each searched position's score, depth, bound, and best move | New file |
| `opening_book.py` | 21 | Read `opening_book.txt` and find the book moves | New file |
| `search.py` | 173 | Move ordering with killers, quiescence, alpha-beta with the table and the null move, the principal variation, aspiration windows, and time management | Killers, table, null move, principal variation, window, time |
| `uci.py` | 59 | The UCI loop, the book, and the clock | Book, hard time limit |
| **Total** | **535** | | **+193** |

The code lines leave out blank lines, comments, and docstrings. `opening_book.txt`
holds 43 openings and 13 trap defenses in UCI moves (`e2e4 e7e5 g1f3 ...`), so Remus
needs no SAN code to read it.

## The call tree

Each box is a function, colored by its file, and each arrow runs from a function to
a function it calls. A circle arrow after a name marks a function that calls itself.

![The call tree of Remus3](call_tree.svg)

## What each enhancement does

- **Killer moves (S1).** A quiet move that causes a cutoff at one ply often causes a
  cutoff in the other positions at that ply. `alpha_beta()` keeps two such moves per
  ply in `killers`, and `ordered_moves()` tries them right after the captures.
- **Pawn structure (E1).** `pawn_terms()` subtracts 15 for each doubled or isolated
  pawn and adds a bonus for a passed pawn, from 10 on its starting rank to 120 one
  step from promotion.
- **Position key and transposition table (N1, N2).** `position_key()` turns a
  position into one number with Python's `hash()`. Before searching a position,
  `alpha_beta()` asks the table what an earlier search learned about it: a deep
  enough score ends the search at once, and the stored best move goes first.
- **Opening book (N3).** While the game follows a line of `opening_book.txt`,
  `uci.py` plays the book move at once, after checking it with the move generator.
- **Aspiration windows (S8).** From depth 4 on, `think()` searches with a window 50
  centipawns either side of the last score, and opens the window only when the score
  falls outside it.
- **Time management (M2).** `think()` spends more time when the best move changes
  between depths, and never more than `longest`, the hard limit `uci.py` sets from the
  clock.
- **Null-move pruning (S2).** `alpha_beta()` lets the opponent move twice with a search
  three plies shallower. If the side to move still stands above beta, its real moves
  will too, and the search cuts off. The null move is the same board with the other
  side to move and no en passant square, so it needs no copy. `has_pieces()` skips
  the null move in a king and pawn ending, where passing can be the only bad move.
- **Principal variation (S4).** After each depth, `principal_variation()` follows the
  table's best moves from the root, and the `info` line shows that line of best play
  after `pv`.
- **Bishop pair and rook table (E4, E6).** `evaluate()` adds 30 for a side that keeps
  both bishops, and `ROOK_TABLE` rewards rooks on the seventh rank and the central
  files.

The new search visits far fewer positions for the same depth. To depth 4 from the
starting position Remus2 visits 17,360 positions and Remus3 2,944, and both choose
`g1f3`. `verify_engines.py` checks Remus3's
perft counts against the published counts from six positions, and Remus3 finds a
forced mate in all ten of its mate puzzles (the key move in nine).

## What it leaves out

Everything Remus4 adds: draw sense, the endgame terms, late move reductions,
principal variation search, pruning margins, static exchange evaluation, and the last
evaluation terms.

## Play it

The student pair adds its own `engines/Remus3/remus.bat` to Lucas Chess, as the
[Lucas Chess guide](../../lucas_chess/lucas_chess_guide.md) shows. It names itself
`Remus3`. While a game follows a book line, it plays the book move at once; after that
it searches.
