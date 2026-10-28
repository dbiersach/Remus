# Engine parity: Remus and Niram

`scripts/engine_parity.py` checks that each Niram engine thinks exactly like the Remus version of the same color. For every position below, both engines report the position key, the version's evaluation, the legal moves in generation order and in search order, the book moves, and a search with no clock: each depth's score, node count, and principal variation, and the best move. Niram picks the depth, the deepest search that visits at most 100,000 positions, and Remus repeats that search. Any difference in any field counts as a mismatch.

Last run: 2026-10-28, 12 versions, 49 positions, 588 searches, 0 mismatches, 16.4 minutes on 4 cores.

Run it again with `uv run scripts/engine_parity.py --nodes 100000` from the repository folder.

## Versions

| Version | Positions matched | Positions searched | Deepest search | Remus time (s) |
| --- | ---: | ---: | ---: | ---: |
| WHITE | 49 of 49 | 1,666,799 | 7 | 194 |
| YELLOW | 49 of 49 | 1,640,811 | 12 | 192 |
| ORANGE | 49 of 49 | 1,673,889 | 7 | 183 |
| BROWN | 49 of 49 | 1,847,889 | 8 | 240 |
| BLUE | 49 of 49 | 1,703,716 | 8 | 180 |
| PINK | 49 of 49 | 1,550,094 | 8 | 170 |
| RED | 49 of 49 | 2,095,092 | 10 | 208 |
| PURPLE | 49 of 49 | 1,756,864 | 8 | 225 |
| GRAY | 49 of 49 | 1,668,693 | 7 | 198 |
| CYAN | 49 of 49 | 1,663,131 | 7 | 197 |
| GREEN | 49 of 49 | 1,666,799 | 7 | 194 |
| GOLD | 49 of 49 | 2,232,898 | 12 | 281 |

## Opening book

Niram reads `Niram/opening_book.txt`; the check compares every position and move of its book, in order, with the book each Remus version loads.

| Version | Positions | Moves | Same as Niram's book | Same file |
| --- | ---: | ---: | --- | --- |
| GREEN | 285 | 328 | yes | yes |
| GOLD | 285 | 328 | yes | yes |

## Positions

The depth column gives the depth each version searched, WHITE first.

| Position | What it tests | Depths |
| --- | --- | --- |
| start | Opening | 5 5 5 6 5 5 5 5 5 5 5 8 |
| after-e4 | Opening | 4 4 4 5 5 4 5 4 4 4 4 7 |
| italian | Opening, in book | 4 4 4 4 4 4 4 4 4 4 4 5 |
| najdorf | Opening, in book | 4 4 4 5 4 4 4 4 4 4 4 6 |
| queens-gambit | Opening, in book | 4 4 4 4 4 4 4 4 4 4 4 6 |
| kings-indian | Opening, in book | 4 4 4 4 4 4 4 4 4 4 4 5 |
| grob | Opening, out of book | 4 4 4 5 4 4 4 4 4 4 4 6 |
| scholars-trap | Trap line, Black defends | 4 4 4 5 4 4 5 4 4 4 4 6 |
| blackburne-shilling | Trap line, White defends | 4 4 5 5 4 4 5 4 4 4 4 6 |
| trap-attacker | Trap line, attacker's turn | 4 4 4 4 4 4 4 4 4 4 4 5 |
| giuoco-middlegame | Middlegame | 3 3 4 4 3 4 4 3 3 3 3 5 |
| kiwipete | Middlegame, castling, en passant | 4 4 4 4 4 4 4 4 4 4 4 4 |
| pinned-bishops | Middlegame, pins | 4 4 4 5 4 4 4 4 4 4 4 6 |
| wac-001 | Tactic | 4 4 4 5 4 4 4 4 4 4 4 5 |
| wac-002 | Tactic, Black | 5 5 6 6 5 5 6 5 5 5 5 7 |
| wac-003 | Tactic | 4 4 5 5 4 4 4 4 4 4 4 6 |
| wac-004 | Tactic, sacrifice | 3 3 3 3 3 3 3 3 3 3 3 3 |
| wac-005 | Tactic, Black | 3 3 3 3 3 3 3 3 3 3 3 3 |
| in-check | Check | 2 2 2 2 2 2 2 2 2 2 2 2 |
| double-check | Double check | 4 4 4 4 4 4 4 4 4 3 4 6 |
| castle-both | Castling | 5 5 5 6 5 5 6 5 5 5 5 7 |
| castle-through-check | Castling across an attacked square | 5 5 5 5 5 5 6 5 5 5 5 6 |
| castle-b-file | Castling with b1 attacked | 5 5 5 5 5 5 6 5 5 5 5 6 |
| en-passant | En passant | 4 4 4 4 4 4 4 4 4 4 4 5 |
| en-passant-pinned | En passant that exposes the king | 6 6 6 7 7 6 7 6 6 6 6 8 |
| promotion | Promotion | 4 4 4 5 5 4 6 4 4 5 4 6 |
| promotion-capture | Promotion by capture | 4 4 4 4 5 4 6 4 4 4 4 7 |
| black-promotion | Promotion, Black | 4 4 4 4 5 4 6 4 4 4 4 7 |
| underpromotion | Knight promotion with check | 5 5 5 5 5 5 7 5 5 5 5 10 |
| king-and-pawn | Endgame | 7 7 7 8 8 8 10 7 7 7 7 12 |
| rook-ending | Endgame | 2 2 2 2 2 2 2 2 2 2 2 2 |
| lucena | Endgame | 5 5 6 6 5 5 6 5 5 5 5 9 |
| philidor | Endgame, Black | 5 5 5 6 5 5 6 5 5 5 5 7 |
| queen-vs-pawns | Endgame | 4 4 4 5 5 5 6 4 4 4 4 7 |
| pawn-race | Endgame | 7 7 7 7 7 7 9 8 7 7 7 10 |
| king-queen-king | Mating with the queen | 4 4 4 5 4 4 5 4 4 4 4 6 |
| king-rook-king | Mating with the rook | 5 5 5 6 5 5 6 5 5 5 5 8 |
| bishop-knight | Mating with bishop and knight | 5 5 5 6 6 5 6 5 5 5 5 8 |
| back-rank | Mate in one | 2 2 2 2 2 2 2 2 2 2 2 2 |
| mate-001 | Mate in two | 4 4 4 5 4 4 4 4 4 4 4 5 |
| mate-005 | Mate in two | 4 4 4 5 4 4 4 4 4 4 4 5 |
| mate-007 | Mate in two | 4 4 4 5 4 4 4 4 4 4 4 5 |
| mate-008 | Mate in three | 3 3 3 3 3 3 5 3 3 3 3 5 |
| repetition | Threefold repetition one move away | 4 4 4 5 5 4 5 4 4 4 4 7 |
| repetition-ahead | Repetition while ahead | 4 9 4 5 5 4 5 4 4 4 4 12 |
| fifty-moves | Fifty-move rule near | 5 12 5 6 5 5 6 5 5 5 5 12 |
| knight-only | Insufficient material | 5 5 6 7 6 5 6 5 5 5 5 10 |
| checkmated | Checkmate on the board | 0 0 0 0 0 0 0 0 0 0 0 0 |
| stalemated | Stalemate on the board | 0 0 0 0 0 0 0 0 0 0 0 0 |
