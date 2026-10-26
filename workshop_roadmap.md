# Turning a Chess Engine into Science AI: Workshop Roadmap

## Purpose

Build a chess engine in native Python, one understandable step at a time. The workshop is a teaching project: every lesson should explain the chess idea, show the corresponding code, let the learner inspect a small example, and end with a concrete exercise. A working game comes first; stronger play comes later.

The engine should eventually play through a graphical chess interface. PyChess is a desktop chess client that can host an external engine through the Universal Chess Interface (UCI). `python-chess` is a Python chess library, not a full desktop GUI; it can help an optional interface or serve as an independent reference for testing. Neither should supply the core engine's board representation, move generator, search, or evaluation. Keep that boundary visible in the examples.

## Teaching principles

1. **Clarity over speed.** Use ordinary Python lists, dictionaries, tuples, strings, functions, and small classes only when they make the code easier to follow. Prefer a clear loop over a compact trick. Slow but understandable code is acceptable.
2. **No esoteric structures or third-party libraries inside the engine.** Do not introduce bitboards, magic numbers, specialized trees, complex caches, compiled extensions, or framework machinery merely for speed. Standard-library modules are acceptable when their use is obvious. External programs, opening books, and endgame tables are optional resources at the boundary, never hidden substitutes for lessons on how the engine works.
3. **Explain the state before changing it.** For every move, identify the squares, side to move, castling rights, en passant target, clocks, and history that may change.
4. **Make and undo the same move.** Search will rely on exact reversal. Record the old state explicitly and verify that undo restores it byte for byte in a simple serialized form.
5. **Separate chess rules from search.** A legal move generator should work before minimax, alpha-beta, books, tables, or a GUI are added.
6. **Keep one source of truth.** The engine owns its game state and rules. A GUI sends moves and displays results; it does not quietly repair illegal engine behavior.
7. **Introduce one idea at a time.** Start with a correct, small implementation. Show a faster or more advanced version only after the simple version is understood, and retain a clear explanation of why it is needed.

These principles apply especially to move generation, search-tree exploration, evaluation, game-state recording, undo, zero-width searches, background analysis, principal variation search, transposition tables, endgame-table access, and opening-book access. Advanced topics remain readable Python even when that limits playing strength.

## What we are building

The final learning project has four boundaries:

| Part | Responsibility |
| --- | --- |
| Native Python engine | Board, rules, legal moves, game state, search, evaluation, and move choice |
| Console driver | Human-readable board and commands for early lessons and debugging |
| UCI adapter | Translate GUI commands into engine calls and return best moves and optional analysis |
| Optional external interface | PyChess as a desktop GUI, or a small interface using `python-chess` for display/reference work |

The engine should run without PyChess or `python-chess`. The optional interface is an integration exercise after the core engine can complete a legal game.

## A simple starting representation

Use an 8-by-8 list of lists. A square contains a one-character piece symbol or `.` for empty. Uppercase letters are White; lowercase letters are Black. Define one coordinate convention and repeat it in comments and examples: row 0 is rank 8, column 0 is file `a`.

```python
board = [
    list("rnbqkbnr"),
    list("pppppppp"),
    list("........"),
    list("........"),
    list("........"),
    list("........"),
    list("PPPPPPPP"),
    list("RNBQKBNR"),
]
```

A plain game-state record is enough at first:

```python
state = {
    "board": board,
    "turn": "white",
    "castling": "KQkq",
    "en_passant": None,
    "halfmove_clock": 0,
    "fullmove_number": 1,
    "position_history": [],
}
```

Choose one simple move record, such as a dictionary with `from`, `to`, and `promotion`. Add flags only when they make special moves clearer. Document whether squares are `(row, column)` tuples or algebraic names. Keep conversion at the input/output boundary.

The sample representation is a starting point, not a demand for a large class hierarchy. When the state grows, a small `GameState` class or a standard-library `dataclass` is fine if it makes ownership explicit.

## Workshop roadmap

### 1. Draw the board and read coordinates

Print the board with files `a` through `h` and ranks `8` through `1`. Convert `e2` into a row and column, then back again. Reject invalid coordinates cleanly. Exercise: print a starting board and identify the piece on `b1`.

**Ready to move on when:** the displayed board, internal indices, and algebraic coordinates agree in both directions.

### 2. Describe a move and update an ordinary position

Represent a move plainly. Write a function to make a quiet move or ordinary capture and another to undo it. Save the captured piece and all prior state in a small undo record. Do not build search yet. Exercise: make `e2e4`, undo it, and compare the restored state with the original.

**Ready to move on when:** every ordinary move can be reversed exactly and the side to move changes correctly.

### 3. Generate pseudo-legal moves

For each piece belonging to the side to move, enumerate destinations allowed by its movement pattern, without yet checking whether its own king is exposed. Handle pawn direction, starting double steps, diagonal captures, and board edges. Sliding pieces stop at the first occupied square; they may capture an enemy there but cannot continue through it. The king moves one square; the knight jumps. Keep one function per piece type if that helps beginners trace the logic.

**Ready to move on when:** simple hand-built positions produce the expected candidate moves.

### 4. Detect attacks, check, and legal moves

Write `is_square_attacked(square, by_side)` independently of the final legal-move filter. A pawn's attacked squares differ from its forward moves. Determine whether a king is in check. To obtain legal moves, make each pseudo-legal move, reject it if the mover's king is attacked, and undo it. This simple approach is acceptable even if it is slow. Do not permit a move that captures the opposing king; checkmate is a state with no legal escape.

**Ready to move on when:** pinned pieces, discovered checks, king moves into attack, check escapes, checkmate, and stalemate behave correctly.

### 5. Handle special moves explicitly

Add one rule at a time, with both make and undo behavior. Use the checklist below. Do not infer castling rights from the current board alone; a rook that moved away and returned has lost the relevant right. Do not infer en passant solely from the last board shape; save its temporary target in state.

**Ready to move on when:** special moves pass the focused examples and restore exactly after undo.

### 6. Record a complete game

Update the halfmove clock, fullmove number, castling rights, en passant target, and position history. Add FEN input/output as a useful boundary format. Store enough information to identify repeated positions correctly: piece placement, side to move, castling rights, and an en passant right when it creates a legal capture. Add simple move notation for input/output; leave polished PGN writing until the game rules are stable.

**Ready to move on when:** a game can be replayed and each position can be undone to the start.

### 7. End the game correctly

Detect checkmate and stalemate. Account for threefold repetition, the fifty-move rule, and insufficient mating material; distinguish a claimable draw from an automatic termination where the rules require it. Discuss the fivefold repetition and seventy-five-move rules when extending to full FIDE behavior. Never call a position mate merely because a side has no moves: first check whether its king is attacked.

**Ready to move on when:** the console driver reports a clear result and reason.

### 8. Evaluate a position

Start with material values and a score relative to White, then convert at the search boundary if using a side-to-move convention. Add simple mobility, king safety, pawn structure, or piece placement only when each term can be explained and tested on sample positions. Checkmate scores should dominate every ordinary evaluation and include distance-to-mate information when useful.

**Ready to move on when:** the engine can explain why it prefers one quiet position over another.

### 9. Search a small game tree

Show the tree on paper first. Implement depth-limited minimax or negamax, then alpha-beta pruning. Each node must make a move, call the next depth, and undo the move even when pruning or returning early. Use a `try/finally` pattern if it prevents a missed undo. Count nodes and compare a small search with hand calculation. Define a sensible behavior when there are no legal moves.

**Ready to move on when:** the engine chooses a legal move, handles mate and stalemate at the leaf, and restores the root position after searching.

### 10. Improve search carefully

Introduce iterative deepening, move ordering, a simple capture extension or quiescence search, and a time or node limit in separate lessons. Explain the horizon effect before adding quiescence. Keep a complete principal variation as a list of moves that can be replayed. A background evaluator may run through a plain thread or process at the interface boundary, but state ownership and cancellation must be explicit; never allow background work to mutate the live game position unexpectedly.

Only after ordinary alpha-beta is correct, teach zero-width (null-window) searches and principal variation search. A zero-width search answers whether a position crosses a bound; it does not return an exact score by itself. In principal variation search, search the first move with a full window, probe later moves with a narrow window, and re-search with a full window when a probe indicates a potentially better move. Include an exercise where the re-search is required.

### 11. Cache and use optional chess resources

Add a transposition table as a normal Python dictionary. A key must identify the complete position relevant to legal play, including turn and rights. A stored entry should include search depth, score, bound type (`exact`, `lower`, or `upper`), and best move. Explain why a bound is not interchangeable with an exact result and why mate scores may need normalization by ply. Start with a straightforward position key; introduce hashing only if learners need it and can explain collisions and update rules.

Opening libraries and endgame tables are optional boundary features. First show how a small human-readable opening list can map a recorded position to candidate moves; validate every retrieved move with the native legal generator. Then explain how a tablebase probe can answer a supported endgame position, what its piece-count and rule constraints are, and how to fall back to native search when the position is unsupported. Keep file parsing or adapter code apart from engine rules. An absent book or table must never prevent the engine from playing.

### 12. Connect to a GUI

Create a small UCI command loop around the engine. Implement the subset needed to launch and play: `uci`, `isready`, `ucinewgame`, `position startpos ...`, `position fen ...`, `go`, `stop` as time control is added, and `quit`. Return moves in UCI notation, such as `e2e4` or `e7e8q`; use `bestmove 0000` only when there is no legal move. Keep protocol text on standard output and debugging information on standard error so the GUI can parse responses.

Register the Python launcher as an external UCI engine in PyChess and play short games. Alternatively, build a small display layer using `python-chess` components while the workshop engine still decides legality and moves. When testing, `python-chess` can independently check positions and moves; do not make it the engine's hidden implementation.

**Completion test:** the GUI can start a game, send moves, receive legal engine replies, display promotions correctly, and end a game without losing synchronization.

## Special-move checklist

| Case | Generation and legality | State and undo reminders |
| --- | --- | --- |
| Kingside and queenside castling | King and chosen rook have not moved; squares between them are empty; king is not in check and does not pass through or land on an attacked square. A rook's attacked square is irrelevant. | Move both pieces. Clear both rights for that king, or the appropriate right when a rook moves or is captured on its home square. Undo both pieces and the previous rights. |
| En passant | A pawn may capture only immediately after the opponent's double pawn push, from the correct adjacent file. Test the resulting king safety after removing the captured pawn. | Store the en passant target only for the next side's turn. Remove the captured pawn from its original square, not the destination square. Undo restores it there and restores the prior target. |
| Promotion and underpromotion | A pawn reaching its last rank offers queen, rook, bishop, and knight choices, for quiet moves and captures. A bare destination is ambiguous. | Replace the pawn with the selected piece and record the choice. Undo restores the pawn and any captured piece. UCI adds `q`, `r`, `b`, or `n` to the move. |
| Multiple queens or other promoted pieces | Never assume one queen per side, nor a fixed count of rooks, bishops, or knights. Iterate over board contents. | The board representation must allow every promoted piece to coexist. Captures and undo work the same way as for original pieces. |
| Double pawn push | Only from the pawn's starting rank, with both intermediate and destination squares empty. | Set the temporary en passant target; clear an old target on other moves. |
| Rook capture on its home square | The capture can remove an opponent's castling right even though that opponent did not move. | Save and restore all previous castling rights in the undo record. |
| Check, pin, and discovered attack | A special move is legal only if the mover's king is safe in the final position. | Test after the full move, including rook motion or en passant pawn removal. |

## Exact undo contract

Before changing state, save the information that cannot be reconstructed reliably from the resulting board:

- moving piece, destination's prior piece, and special captured piece if any;
- prior castling rights and en passant target;
- prior halfmove clock, fullmove number, and side to move;
- promotion choice and any rook motion during castling;
- the history entry or position count changed by this move.

After `undo_move(make_move(state, move))`, the full game state must equal its original snapshot. This includes clocks and rights, not only visible pieces. A search must leave the live position unchanged even if it stops early.

## Verification exercises

Use short, named positions rather than only playing from the standard start. For each, write the expected legal moves or game result before running the engine.

1. Starting position: 20 legal moves.
2. A king in check: only moves that remove the check.
3. A pinned piece: no move that exposes its king.
4. Castling available, blocked, through check, and after rook return.
5. En passant available, expired, and illegal because it exposes the king.
6. Quiet promotion, capture promotion, and each underpromotion choice.
7. A position with two queens on one side.
8. Checkmate versus stalemate.
9. Repetition with changed castling or en passant rights.
10. Long make/undo sequences returning to exactly the starting state.

Count legal-move tree nodes to shallow depth (`perft`) and compare with a trusted reference for a handful of standard positions. This validates move generation without mixing search strength into the diagnosis. Keep the reference outside the engine, and investigate a mismatch by dividing counts by root move.

For search lessons, record root legal moves, chosen move, score, principal variation, node count, and whether the root state is unchanged. Use tiny tactical positions whose correct answer can be checked by hand. Add a stronger engine or `python-chess` as an external cross-check only after learners can explain the native result.

## Suggested lesson rhythm

Each meeting should follow the same pattern:

1. Name the chess rule or search question in plain language.
2. Draw one minimal position or search tree.
3. Trace the relevant Python state before and after one operation.
4. Write the simplest correct code together.
5. Run focused examples, including one failure case.
6. Let learners change or extend the code and explain their result.
7. Save a short list of unanswered questions for the next meeting.

Avoid dropping in a complete optimized engine. The workshop succeeds when a learner can explain a move, trace an undo, and say why a search result is legal and preferred.

## Reference links for the optional interface

- [PyChess project and external-engine support](https://github.com/pychess/pychess)
- [python-chess documentation for UCI/XBoard communication](https://python-chess.readthedocs.io/en/latest/engine.html)
- [python-chess project and supported library features](https://github.com/niklasf/python-chess)

These links support integration and independent checking. The workshop engine remains native Python and self-contained.
