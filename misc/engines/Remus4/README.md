# Remus4: Remus3 with every enhancement

Remus4 is [Remus3](../Remus3/README.md) with every other enhancement of
[`remus_versions.md`](../remus_versions.md): draw sense, the mating
bonus and tapered evaluation, late move reductions, principal variation search,
delta and futility pruning, rooks on open files, static exchange evaluation, mobility,
the pawn race, and king safety. The student pairs type the 159 new lines into their
Remus3. It speaks UCI to Lucas Chess through `remus.bat` and uses only the standard
library.

## Files

| File | Code lines | What it does | Steps |
| --- | ---: | --- | --- |
| `board.py` | 23 | The piece numbers, the position tuple, the starting position, the position key, and UCI move text | N1, M1 |
| `make_move.py` | 24 | Play a move on a copy of the board, and count the fifty-move clock | M1 |
| `attacks.py` | 34 | Is a square attacked? Is a king in check? | |
| `move_generation.py` | 65 | List the moves of the side to move, castling included | |
| `evaluation.py` | 195 | Material, six piece-square tables (the king's tapered), mobility, the bishop pair, rooks on open files, pawn structure, the pawn race, king safety, the mating bonus, and insufficient material | E1 to E9, M1 |
| `exchange.py` | 36 | New: static exchange evaluation | N4 |
| `transposition_table.py` | 22 | The transposition table, a plain dict | N2 |
| `opening_book.py` | 21 | Read `opening_book.txt` and find the book moves | N3 |
| `search.py` | 212 | Move ordering with killers, quiescence with delta pruning and SEE, alpha-beta with the table, null move, futility, LMR, PVS, draw sense, the principal variation, aspiration windows, and time management | S1 to S8, M1, M2 |
| `uci.py` | 62 | The UCI loop, the game's position history, the book, and the clock | M1, M2, N3 |
| **Total** | **694** | | |

The code lines leave out blank lines, comments, and docstrings. About 50 of the 195
lines of `evaluation.py` are the rows of its six tables.

## The call tree

Each box is a function, colored by its file, and each arrow runs from a function to
a function it calls. A circle arrow after a name marks a function that calls itself.

![The call tree of Remus4](call_tree.svg)

## How it keeps the code small

- **A position is one tuple**, `(board, white, castling, en_passant, halfmove)`, so
  every search function takes one `position` argument, and `make_move()` returns the
  next position. The halfmove clock counts the moves toward the fifty-move rule.
- **The position key is Python's own `hash()`** of the board, side, castling rights,
  and en passant square, so the table and the repetition check need no Zobrist
  numbers.
- **The principal variation comes from the table:** after each depth,
  `principal_variation()` follows the stored best moves from the root, so the search
  builds no move lists.
- **One pass over the board** collects everything the evaluation needs (material,
  phase, the kings, pawns, rooks, and bishops), and the terms that compare pieces,
  such as passed pawns and open files, work from those lists.
- **Remus2's shortcuts carry through.** `piece_moves()` moves every piece but the
  pawn, `is_attacked()` looks out from the square with the steps of each kind of
  piece, and `ordered_moves()` hands the search each move with
  its priority, so quiescence stops at the first move below `CAPTURE`.
- **Exchanges reuse the move generator.** `cheapest_attacker()` lists the moves of
  the attacking side with `generate_moves()` and keeps the cheapest piece whose move
  lands on the square, so `exchange.py` needs no attack loop of its own.
- **Mobility counts moves.** `evaluate()` lists each piece's moves with
  `piece_moves()` and counts them, so it needs no counting function of its own.
- **Pawn files padded by one.** The pawn counts hold ten files, the eight real ones
  and an empty file on each side, so a pawn on the a or h file needs no edge check to
  look at the files beside it.
- **The null move needs no copy:** the board stays the same, and only the side to
  move and the en passant square change.

## What the pruning costs

To depth 4 from the starting position Remus4 visits 3,005 positions, against 2,944
for Remus3 and 17,360 for Remus2, and on the Kiwipete position 6,486 against Remus3's
51,527. The pruning has a price: late move reductions search a quiet mating move one
ply shallower, so Remus4 often finds a slower mate first. In seven of the ten mate
puzzles of `verify_engines.py` it plays a
move that mates more slowly than the key move, and `think()` stops as soon as
it sees any forced mate. The slower mate still wins the game.

## Play it

The student pair adds its own `engines/Remus4/remus.bat` to Lucas Chess as "My Remus4", as the
[Lucas Chess guide](../../lucas_chess/lucas_chess_guide.md) shows. It names itself
`Remus4`. While a game follows a book line, it plays the book move at once; after that
it searches.
