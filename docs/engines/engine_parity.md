# Engine parity: Remus and Niram

`scripts/engine_parity.py` checks that Niram-GOLD thinks exactly like Remus-GOLD. For every position below, both engines report the position key, the version's evaluation, the legal moves in generation order and in search order, the book moves, and a search with no clock: each depth's score, node count, and principal variation, and the best move. Niram picks the depth, the deepest search that visits at most 25,000 positions, and Remus repeats that search. Any difference in any field counts as a mismatch.

Last run: 2026-10-28, Remus-GOLD and Niram-GOLD, 49 positions, 49 searches, 0 mismatches, 0.5 minutes on 4 cores.

Run it again with `uv run scripts/engine_parity.py` from the repository folder.

## Versions

| Version | Positions matched | Positions searched | Deepest search | Remus time (s) |
| --- | ---: | ---: | ---: | ---: |
| GOLD | 49 of 49 | 615,806 | 12 | 78 |

## Opening book

Niram reads `Niram-GOLD/opening_book.txt`; the check compares every position and move of its book, in order, with the book Remus-GOLD loads.

| Version | Positions | Moves | Same as Niram's book | Same file |
| --- | ---: | ---: | --- | --- |
| GOLD | 285 | 328 | yes | yes |

## Positions

The depth column gives the depth each search reached.

| Position | What it tests | Depths |
| --- | --- | --- |
| start | Opening | 6 |
| after-e4 | Opening | 5 |
| italian | Opening, in book | 5 |
| najdorf | Opening, in book | 3 |
| queens-gambit | Opening, in book | 5 |
| kings-indian | Opening, in book | 4 |
| grob | Opening, out of book | 4 |
| scholars-trap | Trap line, Black defends | 5 |
| blackburne-shilling | Trap line, White defends | 5 |
| trap-attacker | Trap line, attacker's turn | 5 |
| giuoco-middlegame | Middlegame | 3 |
| kiwipete | Middlegame, castling, en passant | 4 |
| pinned-bishops | Middlegame, pins | 5 |
| wac-001 | Tactic | 4 |
| wac-002 | Tactic, Black | 7 |
| wac-003 | Tactic | 5 |
| wac-004 | Tactic, sacrifice | 3 |
| wac-005 | Tactic, Black | 3 |
| in-check | Check | 2 |
| double-check | Double check | 4 |
| castle-both | Castling | 5 |
| castle-through-check | Castling across an attacked square | 5 |
| castle-b-file | Castling with b1 attacked | 5 |
| en-passant | En passant | 4 |
| en-passant-pinned | En passant that exposes the king | 7 |
| promotion | Promotion | 5 |
| promotion-capture | Promotion by capture | 5 |
| black-promotion | Promotion, Black | 5 |
| underpromotion | Knight promotion with check | 7 |
| king-and-pawn | Endgame | 11 |
| rook-ending | Endgame | 2 |
| lucena | Endgame | 6 |
| philidor | Endgame, Black | 6 |
| queen-vs-pawns | Endgame | 6 |
| pawn-race | Endgame | 7 |
| king-queen-king | Mating with the queen | 5 |
| king-rook-king | Mating with the rook | 6 |
| bishop-knight | Mating with bishop and knight | 6 |
| back-rank | Mate in one | 2 |
| mate-001 | Mate in two | 5 |
| mate-005 | Mate in two | 5 |
| mate-007 | Mate in two | 5 |
| mate-008 | Mate in three | 3 |
| repetition | Threefold repetition one move away | 5 |
| repetition-ahead | Repetition while ahead | 12 |
| fifty-moves | Fifty-move rule near | 12 |
| knight-only | Insufficient material | 7 |
| checkmated | Checkmate on the board | 0 |
| stalemated | Stalemate on the board | 0 |
