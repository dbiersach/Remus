# Bug hunt

The Remus files in this folder are a copy of the Day 6, period 3 code, with three bugs planted in them. Each bug breaks one chess rule. Run `uv run hunt.py` from inside this folder: it uses `divide()` to count the positions under every root move of four standard positions, and prints each root move where Remus and python-chess disagree.

A root move that disagrees points at a rule that its position needs. Ask what is special about that move or about the replies to it, find the rule in the code, fix the line, and run the hunt again. The hunt is over when it prints 0 root moves that disagree.

## Answers

| File | The bug | Root moves that show it |
| --- | --- | --- |
| `make_move.py` | An en passant capture leaves the captured pawn on the board. The fix: `set_piece(board, victim, EMPTY)` | g2g4 and e2e4 in position 3: the White pawn left on rank 4 hides the Black king on h4 from the rook on b4 |
| `legal_moves.py` | Castling checks the landing square instead of the square the king crosses. The fix: `if in_check(state, color) or is_square_attacked(board, crossed, enemy):` | e5f7, e5d7, e5g6, and e5c6 in kiwipete: the knight attacks d8 or f8 |
| `move_generation.py` | A pawn cannot promote to a knight. The fix: `PROMOTION_PIECES = "QRBN"` | d7c8n in position 5, missing from Remus's list, and six moves in position 4 |
