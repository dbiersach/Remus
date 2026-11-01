# Remus-PLATINUM: Ten more enhancements

Remus-PLATINUM is Remus-GOLD plus ten more enhancements: five that change the search and five that change the evaluation. It is the course designer's engine, outside the two-week course: no student pair writes it, and no period folder copies it. Niram-PLATINUM, in `engines/Niram-PLATINUM`, is the same engine in Rust, and it picks the same move as Remus-PLATINUM at every depth.

Every rule, the opening book, and every GOLD enhancement stay as they are. The new code lives in four files:

| File | What changes |
| --- | --- |
| `exchange.py` | New: static exchange evaluation (SEE) |
| `search.py` | Delta pruning and SEE in `quiescence()`, futility pruning in `upgraded_search()`, `aspiration_search()`, and time management in `think()` |
| `evaluation.py` | Five new terms: `tapered_terms()`, `pawn_race()`, `mobility()`, `piece_terms()`, and their helpers |
| `uci_engine.py` | `longest_time()`, the hard limit on one move |
| `test_platinum.py` | New: 14 tests, one or more for each enhancement |

The steps below follow the order a reader meets them in a search: first the captures at the leaves, then the moves near the leaves, then the root, then the clock, and last the evaluation that scores every leaf.

## Step 1: Static exchange evaluation (`exchange.py`)

**The idea.** Before quiescence plays a capture, it asks what the capture wins once every recapture on that square is made. A White queen on d1 that takes a pawn on d5 defended by a knight on f6 wins 100 and then loses 900: the exchange is worth 100 - 900 = -800. Each side recaptures with its cheapest piece, and each side may stop recapturing when one more recapture would lose. No search is needed: the function only looks at the pieces that attack the square.

`attacks_square()` answers whether one piece attacks one square. A pawn attacks one step diagonally forward, a knight and a king jump, and a rook, bishop, or queen slides along a line that must be empty all the way. `step_toward()` turns the gap between two squares into one step of -1, 0, or 1.

```python
def step_toward(gap: int) -> int:
    """Return 1, -1, or 0: one step in the direction of the gap."""
    if gap > 0:
        return 1
    if gap < 0:
        return -1
    return 0
```

```python
def attacks_square(board: Board, start: Square, target: Square) -> bool:
    """
    Return True if the piece on start attacks the target square.

    Parameters
    ----------
    board : Board
        The board.
    start : Square
        The (row, col) of the attacking piece.
    target : Square
        The (row, col) of the square.

    Returns
    -------
    bool
        True if the piece could capture on target. A rook, bishop, or queen needs
        every square between the two to be empty.
    """
    piece = piece_at(board, start)
    kind = piece.upper()
    row_gap = target[0] - start[0]
    col_gap = target[1] - start[1]
    if kind == "P":
        forward = -1 if piece == "P" else 1  # White pawns move toward row 0
        return row_gap == forward and abs(col_gap) == 1
    if kind == "N":
        return (row_gap, col_gap) in KNIGHT_JUMPS
    if kind == "K":
        return max(abs(row_gap), abs(col_gap)) == 1
    straight = row_gap == 0 or col_gap == 0
    diagonal = abs(row_gap) == abs(col_gap)
    if (row_gap, col_gap) == (0, 0):
        return False
    if kind == "R" and not straight:
        return False
    if kind == "B" and not diagonal:
        return False
    if kind == "Q" and not (straight or diagonal):
        return False
    row_step = step_toward(row_gap)
    col_step = step_toward(col_gap)
    row = start[0] + row_step
    col = start[1] + col_step
    while (row, col) != target:
        if board[row][col] != EMPTY:
            return False  # A piece in between blocks the line
        row += row_step
        col += col_step
    return True
```

`least_valuable_attacker()` scans the board for the cheapest piece of one side that attacks the square. Ties go to the first piece in the scan, row 0 (rank 8) first, so Remus-PLATINUM and Niram-PLATINUM always pick the same piece.

```python
def least_valuable_attacker(board: Board, target: Square, white: bool) -> Square | None:
    """Return the square of the cheapest piece of one side attacking target, or None."""
    best = None
    best_value = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == EMPTY or piece.isupper() != white:
                continue
            value = exchange_value(piece)
            if best is not None and value >= best_value:
                continue
            if attacks_square(board, (row, col), target):
                best = (row, col)
                best_value = value
    return best
```

`static_exchange()` plays the exchange on a copy of the board. `gains[0]` is the victim. Each recapture adds the value of the piece standing on the square minus what the other side gained before. Taking a piece off the copy opens the line behind it, so a rook behind a rook (an x-ray) joins the exchange by itself. The last loop walks back from the final capture: at each step the side to move keeps the better of stopping and recapturing. The king counts KING_VALUE, 10,000, so a king can recapture only when nothing can take it back.

```python
def static_exchange(board: Board, move: Move) -> int:
    """
    Return the material a capture wins or loses once every recapture is made.

    Parameters
    ----------
    board : Board
        The board before the capture. It is unchanged when the function returns.
    move : Move
        A capture of a piece on move.to_square.

    Returns
    -------
    int
        The centipawns the moving side gains, if each side keeps recapturing with
        its cheapest piece and stops when one more recapture would lose. A queen
        taking a pawn defended by a knight returns 100 - 900 = -800.
    """
    work = []  # A copy, so pieces can leave and x-rays open
    for row in board:
        work.append(row[:])
    target = move.to_square
    gains = [exchange_value(piece_at(work, target))]
    mover = piece_at(work, move.from_square)
    on_square = exchange_value(mover)  # The value of the piece standing on target
    work[move.from_square[0]][move.from_square[1]] = EMPTY
    work[target[0]][target[1]] = mover
    white = not mover.isupper()  # The side that recaptures next
    while True:
        attacker = least_valuable_attacker(work, target, white)
        if attacker is None:
            break
        # The recapturing side wins the piece on target but gives back what it won
        gains.append(on_square - gains[-1])
        piece = piece_at(work, attacker)
        on_square = exchange_value(piece)
        work[attacker[0]][attacker[1]] = EMPTY
        work[target[0]][target[1]] = piece
        white = not white
    # Each side may stop recapturing: walk back from the last capture
    index = len(gains) - 1
    while index > 0:
        gains[index - 1] = -max(-gains[index - 1], gains[index])
        index -= 1
    return gains[0]
```

**Where it is called.** `quiescence()` in `search.py` (step 2). **What it costs.** Each call scans the 64 squares once for every recapture, so it runs only for captures that delta pruning has not already skipped.

## Step 2: Delta pruning and SEE in quiescence (`search.py`)

**The idea.** Quiescence keeps playing captures until the position is quiet. GOLD tries every capture. PLATINUM skips two kinds before it makes them:

1. **Delta pruning.** When the side to move stands so far below alpha that even winning the victim for free, plus DELTA_MARGIN (200 centipawns) for anything else the capture might bring, cannot reach alpha, the capture cannot change the result. A side that is a rook down (stand pat -500 with alpha at 0) gains nothing from grabbing a pawn: -500 + 100 + 200 = -200, still below 0.
2. **SEE.** A capture whose exchange loses material, such as the queen taking a defended pawn, is skipped. The opponent would simply recapture.

Promotions skip neither test, because a pawn that becomes a queen gains far more than the piece it takes. An en passant victim is not on the target square, so delta pruning counts it as a pawn and SEE is not asked.

```python
    for move in order_moves(capture_moves(state), board):
        victim = piece_at(board, move.to_square)
        if move.promotion is None:
            # Delta pruning: even winning the victim for free leaves the score
            # below alpha. An en passant victim is a pawn beside the target square
            gain = PIECE_VALUES["P"]
            if victim != EMPTY:
                gain = PIECE_VALUES[victim.upper()]
            if stand_pat + gain + DELTA_MARGIN <= alpha:
                continue
            # Static exchange evaluation: the recaptures lose more than the victim
            if victim != EMPTY and static_exchange(board, move) < 0:
                continue
```

**Why it is stronger.** Most of the positions a search visits are quiescence positions, and every skipped capture is a whole quiescence subtree that is never searched. **What it costs.** A skipped capture that would have worked: SEE ignores pins and checks, so it can misjudge a capture by a pinned piece. The test `test_quiescence_skips_a_losing_capture` checks that Qxd5 in the example above is never searched: quiescence visits 1 position, the root.

## Step 3: Futility pruning (`search.py`)

**The idea.** One or two plies before quiescence takes over, a quiet move (no capture, no promotion, no check) rarely changes the score by much. If the static evaluation plus a generous margin still cannot reach alpha, the quiet moves there are "futile": the side to move needs a capture or a check to catch up. FUTILITY_MARGINS gives the margin by depth: 200 centipawns one ply from quiescence, 500 two plies from it.

`upgraded_search()` decides once per position whether the position is futile. It never prunes at the root, in check, or when alpha is a mate score:

```python
    # Futility pruning: one or two plies from quiescence, a quiet move that
    # cannot lift the score above alpha even with FUTILITY_MARGINS to spare is skipped
    futile = (
        ply > 0
        and not in_check_now
        and depth < len(FUTILITY_MARGINS)
        and abs(alpha) < MATE_SCORE - 1000
        and evaluate(state) + FUTILITY_MARGINS[depth] <= alpha
    )
```

Inside the move loop, the first move is always searched in full. Every later quiet move that gives no check is taken back and skipped. The `continue` sits inside the `try` block, so the `finally` clause still runs `undo_move()`:

```python
                gives_check = in_check(state, state["turn"])
                quiet = undo["captured"] == EMPTY and move.promotion is None
                if futile and quiet and not gives_check:
                    continue  # The finally clause takes the move back
```

**Why it is stronger.** Positions near the leaves are the most numerous in the tree, so each pruned quiet move saves a full quiescence search. **What it costs.** A quiet move that would have won, such as a quiet move that traps a piece. The test `test_futility_pruning_keeps_the_answer` checks that a side a rook down still scores below alpha and that the root position is unchanged.

## Step 4: Aspiration windows (`search.py`)

**The idea.** Iterative deepening searches depth 1, then 2, then 3, and the score rarely moves far from one depth to the next. GOLD searches every depth with the widest window, -100,001 to +100,001. PLATINUM first searches the window from the last score minus ASPIRATION_WINDOW (50) to the last score plus 50. A narrow window makes alpha-beta cut off more moves. If the score lands on or outside the window, it is only a bound, not the exact score, so the root is searched again with the full window. Mate scores always get the full window.

```python
def aspiration_search(
    state: dict, depth: int, last_score: int | None, info: SearchInfo
) -> tuple[int, list[Move]]:
    """
    Search the root with a narrow window around the last depth's score first.

    Parameters
    ----------
    state : dict
        The game state. It is unchanged when the search returns.
    depth : int
        How many plies to search.
    last_score : int | None
        The score of the depth before, or None for the first depth.
    info : SearchInfo
        Counts positions and holds the deadline, table, and killers.

    Returns
    -------
    tuple[int, list[Move]]
        The score and principal variation. The score rarely moves more than
        ASPIRATION_WINDOW from one depth to the next, and a narrow window cuts
        off more moves. A score that lands on or outside the window is not exact,
        so the root is searched again with the full window.
    """
    full_alpha = -MATE_SCORE - 1
    full_beta = MATE_SCORE + 1
    if last_score is None or abs(last_score) > MATE_SCORE - 1000:
        return upgraded_search(state, depth, 0, full_alpha, full_beta, info)
    alpha = last_score - ASPIRATION_WINDOW
    beta = last_score + ASPIRATION_WINDOW
    score, pv = upgraded_search(state, depth, 0, alpha, beta, info)
    if alpha < score < beta:
        return score, pv
    return upgraded_search(state, depth, 0, full_alpha, full_beta, info)
```

**Where it is called.** `think()` calls it for every depth instead of calling `upgraded_search()` directly. **What it costs.** A second search of the same depth whenever the score jumps by more than 50, such as when the deeper search finds a tactic. The transposition table holds the first search's results, so the second search is cheaper. The test `test_aspiration_matches_the_full_window` gives a guess far from the true score (400 for a mate in 1) and checks that the re-search finds the same mate as the full window.

## Step 5: Time management (`search.py` and `uci_engine.py`)

**The idea.** GOLD thinks until its clock runs out, then throws away the depth it was in the middle of. PLATINUM plans its time:

1. `uci_engine.py` gives `think()` two times. The plan is GOLD's: a thirtieth of the clock plus half the increment. `longest_time()` adds a hard limit, LONGEST_THINK (3) times the plan, but never more than half of the spare time.
2. After each depth, `think()` sets a budget. The plan is the budget. When the best move just changed (from depth 5 on, where a change means the deeper search found something), the budget doubles (UNSTABLE_TIME). When the best move has held for STABLE_DEPTHS (4) depths in a row, as with an obvious recapture, the budget halves (STABLE_TIME).
3. A new depth takes longer than all the depths before it, so `think()` starts one only while it has spent less than NEXT_DEPTH_SHARE (half) of the budget. Remus-PLATINUM wastes less time on a depth it cannot finish.

```python
def longest_time(words: list[str], white_to_move: bool) -> float:
    """
    Return the most seconds Remus may spend on a move whose best move keeps changing.

    Parameters
    ----------
    words : list[str]
        The "go" command split into words.
    white_to_move : bool
        True if White is to move.

    Returns
    -------
    float
        The planned time for "movetime" or no clock. With a clock, LONGEST_THINK
        times the planned time, but never more than half of the spare time.
    """
    seconds = thinking_time(words, white_to_move)
    clock = "wtime" if white_to_move else "btime"
    if "movetime" in words or clock not in words:
        return seconds
    spare = int(words[words.index(clock) + 1]) / 1000 - RESERVE_SECONDS
    return max(seconds, min(seconds * LONGEST_THINK, spare / 2))
```

```python
    start = time.perf_counter()
    longest = seconds if max_seconds is None else max(seconds, max_seconds)
    info = SearchInfo(deadline=start + longest)
    moves = legal_moves(state)
    best = order_moves(moves, state["board"])[0]
    last_score = None
    stable_depths = 0  # How many depths in a row the best move has not changed
    for depth in range(1, max_depth + 1):
        try:
            score, pv = aspiration_search(state, depth, last_score, info)
        except SearchTimeout:
            break  # Keep the best move of the last depth that finished
        last_score = score
        if pv:
            if depth > 1 and pv[0] == best:
                stable_depths += 1
            else:
                stable_depths = 0
            best = pv[0]
        if report is not None:
            report(format_info(depth, score, info.nodes, pv))
        if abs(score) > MATE_SCORE - 1000 or len(moves) == 1:
            break  # A forced mate or a single legal move needs no deeper search
        budget = seconds
        if stable_depths == 0 and depth >= 5:
            budget = seconds * UNSTABLE_TIME
        elif stable_depths >= STABLE_DEPTHS:
            budget = seconds * STABLE_TIME
        if time.perf_counter() - start > budget * NEXT_DEPTH_SHARE:
            break  # The next depth would not finish in time
    return best
```

**Where it is called.** The `go` command in `uci_engine.py` passes `max_seconds=longest`. With no clock (a fixed-depth search, such as the parity check), the budget never stops a depth early, so both engines search exactly the same depths. The tests `test_think_stops_early_on_a_stable_move` and `test_longest_time_is_a_multiple_of_the_plan` check both parts: a game with 63 seconds on the clock plans 2 seconds and allows at most 6.

## Step 6: Game phase and tapered evaluation (`evaluation.py`)

**The idea.** A king should hide behind its pawns while the queens and rooks are on the board, and walk to the center once they are gone. GOLD has one king table, the hiding one. PLATINUM gives the king two tables, KING_TABLE for the middlegame and KING_ENDGAME_TABLE for the endgame, and blends them by the game phase.

`game_phase()` counts the pieces left: 1 for each knight and bishop, 2 for each rook, 4 for each queen. The starting position counts TOTAL_PHASE, 24; a pawn ending counts 0.

```python
def game_phase(board: Board) -> int:
    """
    Return how much of the middlegame is left, from TOTAL_PHASE (every piece on the
    board) down to 0 (only kings and pawns).

    Parameters
    ----------
    board : Board
        The board.

    Returns
    -------
    int
        1 for each knight and bishop, 2 for each rook, and 4 for each queen, at most
        TOTAL_PHASE (a promoted queen could push the count higher).
    """
    phase = 0
    for row in board:
        for piece in row:
            if piece != EMPTY and piece.upper() in PHASE_WEIGHTS:
                phase += PHASE_WEIGHTS[piece.upper()]
    return min(phase, TOTAL_PHASE)
```

`taper()` blends a middlegame score and an endgame score by the phase. A middlegame score of 10 and an endgame score of 50 blend to 10 at phase 24, 30 at phase 12, and 50 at phase 0. The `//` rounds down, and Niram-PLATINUM uses `div_euclid`, which rounds the same way for negative numbers.

```python
def taper(middlegame: int, endgame: int, phase: int) -> int:
    """Blend a middlegame and an endgame score by the phase: all middlegame at 24."""
    return (middlegame * phase + endgame * (TOTAL_PHASE - phase)) // TOTAL_PHASE
```

`tapered_terms()` scores both kings from both tables and blends them. It also tapers the passed pawn: a passed pawn earns its PASSED_PAWN bonus once more in the endgame, where the pieces that could stop it are gone. `is_passed()` holds the passed-pawn test that `pawn_structure()` uses, so `pawn_race()` can reuse it. `placement()` skips the king, because `tapered_terms()` scores it.

```python
def is_passed(board: Board, row: int, col: int) -> bool:
    """Return True if no enemy pawn stands ahead of this pawn on its file or a neighbor."""
    pawn = board[row][col]
    enemy = "p" if pawn == "P" else "P"
    ahead = range(row) if pawn == "P" else range(row + 1, 8)  # White moves to row 0
    for ahead_row in ahead:
        for ahead_col in (col - 1, col, col + 1):
            if 0 <= ahead_col < 8 and board[ahead_row][ahead_col] == enemy:
                return False
    return True
```

```python
def tapered_terms(board: Board) -> int:
    """
    Score the king's square and the passed pawns by the game phase, positive when
    it favors White.

    Parameters
    ----------
    board : Board
        The board.

    Returns
    -------
    int
        The king reads KING_TABLE in the middlegame and KING_ENDGAME_TABLE in the
        endgame, and taper() blends the two. A passed pawn earns its PASSED_PAWN
        bonus once more in the endgame, so a pawn on the sixth rank is worth an
        extra 60 with only kings and pawns left and nothing extra with every piece
        on the board.
    """
    middlegame = 0
    endgame = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == "K":
                middlegame += KING_TABLE[row][col]
                endgame += KING_ENDGAME_TABLE[row][col]
            elif piece == "k":
                # Black reads the tables upside down
                middlegame -= KING_TABLE[7 - row][col]
                endgame -= KING_ENDGAME_TABLE[7 - row][col]
            elif piece == "P" and is_passed(board, row, col):
                endgame += PASSED_PAWN[6 - row]
            elif piece == "p" and is_passed(board, row, col):
                endgame -= PASSED_PAWN[row - 1]
    return taper(middlegame, endgame, game_phase(board))
```

**Why it is stronger.** In an endgame the king is a strong piece, and GOLD keeps it in the corner. The test `test_endgame_king_prefers_the_center` checks that a king on e4 outscores a king on a1 with only kings on the board.

## Step 7: The pawn race (`evaluation.py`)

**The idea.** The rule of the square: in a pawn ending, a passed pawn promotes unless the defending king can reach the promotion square in time. A White pawn on e5 needs 3 moves to reach e8. A Black king on a5 is 4 king steps from e8 (Chebyshev distance: the larger of the row and column gaps), so with White to move the king is one step too slow and the pawn queens. With Black to move, the king moves first and gains a step: 3 against 3, and the king catches the pawn.

`pawn_race()` gives UNSTOPPABLE_PAWN (400 centipawns) to a side with such a pawn, but only when the defending side has no knight, bishop, rook, or queen, which could stop the pawn. A pawn on its starting square moves two squares at once, so it needs 5 moves, not 6.

```python
def pawn_race(board: Board, turn: str) -> int:
    """
    Score passed pawns that the defending king cannot catch, positive when it
    favors White.

    Parameters
    ----------
    board : Board
        The board.
    turn : str
        The side to move, "w" or "b". A defending king that moves first gains a step.

    Returns
    -------
    int
        UNSTOPPABLE_PAWN for each side with a passed pawn outside the square of the
        defending king, counted only when the defending side has no knight, bishop,
        rook, or queen to stop the pawn. A White pawn on e5 needs 3 moves to reach
        e8, so a Black king on a5, 4 steps from e8, cannot catch it with White to move.
    """
    kings = {}
    for row in range(8):
        for col in range(8):
            if board[row][col] in "Kk":
                kings[board[row][col]] = (row, col)
    score = 0
    for pawn, defender, defender_color, sign in (
        ("P", "k", "b", 1),
        ("p", "K", "w", -1),
    ):
        if defender not in kings:
            continue
        defender_pieces = "nbrq" if defender_color == "b" else "NBRQ"
        has_defender_piece = False
        for row in board:
            for piece in row:
                if piece in defender_pieces:
                    has_defender_piece = True
        if has_defender_piece:
            continue
        king_row, king_col = kings[defender]
        unstoppable = False
        for row in range(8):
            for col in range(8):
                if board[row][col] != pawn or not is_passed(board, row, col):
                    continue
                # Moves to promote; a pawn on its first square moves two at once
                if pawn == "P":
                    promote_row = 0
                    moves_to_go = 5 if row == 6 else row
                else:
                    promote_row = 7
                    moves_to_go = 5 if row == 1 else 7 - row
                king_steps = max(abs(king_row - promote_row), abs(king_col - col))
                if turn == defender_color:
                    king_steps -= 1  # The defending king moves first
                if king_steps > moves_to_go:
                    unstoppable = True
        if unstoppable:
            score += sign * UNSTOPPABLE_PAWN
    return score
```

**Why it is stronger.** A search of 6 to 10 plies cannot always see a pawn promote, but the rule of the square sees it at once, so Remus-PLATINUM goes for a won pawn race and avoids a lost one. The tests `test_pawn_race_rule_of_the_square` and `test_pawn_race_needs_a_pawn_ending` check the e5 example with each side to move, and with a Black knight that turns the term off.

## Step 8: Mobility (`evaluation.py`)

**The idea.** A piece that can move to many squares does more work than a piece boxed in. `reachable_squares()` counts the squares a knight, bishop, rook, or queen can move to: an empty square, or an enemy piece it could capture. A slide stops at the first piece in its way. Pins are not checked, to keep the count simple. `mobility()` multiplies each count by MOBILITY_WEIGHTS: 4 per square for a knight or bishop, 2 for a rook, 1 for a queen. The queen counts least because it reaches many squares anywhere. A knight on e4 of an empty board reaches 8 squares and earns 32.

```python
def reachable_squares(board: Board, row: int, col: int) -> int:
    """Return how many squares a knight, bishop, rook, or queen can move to."""
    piece = board[row][col]
    kind = piece.upper()
    count = 0
    if kind == "N":
        for row_step, col_step in KNIGHT_JUMPS:
            to_row = row + row_step
            to_col = col + col_step
            if 0 <= to_row < 8 and 0 <= to_col < 8:
                target = board[to_row][to_col]
                if target == EMPTY or target.isupper() != piece.isupper():
                    count += 1
        return count
    directions = []
    if kind in "RQ":
        directions += ROOK_DIRECTIONS
    if kind in "BQ":
        directions += BISHOP_DIRECTIONS
    for row_step, col_step in directions:
        to_row = row + row_step
        to_col = col + col_step
        while 0 <= to_row < 8 and 0 <= to_col < 8:
            target = board[to_row][to_col]
            if target != EMPTY:
                if target.isupper() != piece.isupper():
                    count += 1  # A capture counts; the slide stops at any piece
                break
            count += 1
            to_row += row_step
            to_col += col_step
    return count
```

```python
def mobility(board: Board) -> int:
    """
    Score how freely the pieces move, positive when it favors White.

    Parameters
    ----------
    board : Board
        The board.

    Returns
    -------
    int
        For each knight, bishop, rook, and queen, MOBILITY_WEIGHTS of its kind for
        every empty square or enemy piece it can move to (pins are not checked). A
        knight on e4 of an empty board reaches 8 squares and earns 32.
    """
    score = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == EMPTY or piece.upper() not in MOBILITY_WEIGHTS:
                continue
            bonus = MOBILITY_WEIGHTS[piece.upper()] * reachable_squares(board, row, col)
            if piece.isupper():
                score += bonus
            else:
                score -= bonus
    return score
```

**Why it is stronger.** The piece-square tables only know which squares are good in general; mobility sees which squares are open in this position, such as a bishop shut in by its own pawns. **What it costs.** Mobility is the most expensive term: it walks every line of every piece in every position the search scores.

## Step 9: The bishop pair and rooks on open files (`evaluation.py`)

**The idea.** Two bishops together cover both colors of square, so a side that keeps both earns BISHOP_PAIR (30). A rook belongs on an open file, a file with no pawns, where it reaches the far end of the board: ROOK_OPEN_FILE (20). A half-open file, with no friendly pawn but an enemy pawn to attack, earns ROOK_HALF_OPEN_FILE (10). `piece_terms()` counts the pawns on each file first, then scores each rook.

```python
def piece_terms(board: Board) -> int:
    """
    Score the bishop pair and rooks on open files, positive when it favors White.

    Parameters
    ----------
    board : Board
        The board.

    Returns
    -------
    int
        BISHOP_PAIR for a side with two or more bishops, ROOK_OPEN_FILE for each
        rook on a file with no pawns, and ROOK_HALF_OPEN_FILE for each rook on a
        file with only enemy pawns.
    """
    white_pawns = [0] * 8
    black_pawns = [0] * 8
    white_bishops = 0
    black_bishops = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == "P":
                white_pawns[col] += 1
            elif piece == "p":
                black_pawns[col] += 1
            elif piece == "B":
                white_bishops += 1
            elif piece == "b":
                black_bishops += 1
    score = 0
    if white_bishops >= 2:
        score += BISHOP_PAIR
    if black_bishops >= 2:
        score -= BISHOP_PAIR
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == "R":
                own, enemy, sign = white_pawns[col], black_pawns[col], 1
            elif piece == "r":
                own, enemy, sign = black_pawns[col], white_pawns[col], -1
            else:
                continue
            if own == 0 and enemy == 0:
                score += sign * ROOK_OPEN_FILE
            elif own == 0:
                score += sign * ROOK_HALF_OPEN_FILE
    return score
```

The test `test_bishop_pair_and_open_files` checks all three bonuses on small positions.

## Step 10: Adding the terms to `evaluate()` (`evaluation.py`)

`evaluate()` adds the four new functions to GOLD's five terms. `pawn_race()` needs the side to move, so it takes `state["turn"]` as well as the board. `explain_evaluation()` prints every term, and `main()` adds the e5 pawn race as a worked example.

```python
def evaluate(state: dict) -> int:
    """
    Score the position for the side to move.

    Parameters
    ----------
    state : dict
        The game state.

    Returns
    -------
    int
        Material, placement, pawn structure, the mating bonus, king safety, the
        tapered king and passed pawn terms, the pawn race, mobility, and the piece
        terms in centipawns, positive when the side to move stands better. Negamax
        search needs the score from the mover's side.
    """
    board = state["board"]
    white_score = (
        material(board)
        + placement(board)
        + pawn_structure(board)
        + mating_bonus(board)
        + king_safety(board)
        + tapered_terms(board)
        + pawn_race(board, state["turn"])
        + mobility(board)
        + piece_terms(board)
    )
    return white_score if state["turn"] == "w" else -white_score
```

## Measured against Remus-GOLD

The designer's benchmark, `misc/designer/remus_benchmark.py`, searched its ten positions one depth at a time up to depth 4 with each engine, on one computer:

| Version | Positions to finish depth 4 | Share of Remus-GOLD's | Positions per second | Total time |
| --- | ---: | ---: | ---: | ---: |
| Remus-GOLD | 84,812 | 100% | 5,750 | 14.7 s |
| Remus-PLATINUM | 38,041 | 45% | 4,573 | 8.3 s |

The Rust copies, with `cargo run --release -- bench 7` on the same ten positions:

| Version | Positions to finish depth 7 | Positions per second (cloud) | Time (cloud) | Time (designer's PC) |
| --- | ---: | ---: | ---: | ---: |
| Niram-GOLD | 2,043,889 | 361,806 | 5.65 s | 4.95 s |
| Niram-PLATINUM | 666,350 | 211,810 | 3.15 s | 2.91 s |

PLATINUM visits less than half as many positions as GOLD for the same depth, because the three pruning steps remove subtrees and the aspiration windows cut off more moves. Each position costs about 20 percent more in Python and about 40 percent more in Rust, because mobility and SEE scan the board. The two effects together still finish each depth sooner.

## The tournament: Niram-PLATINUM against Niram-GOLD

Python plays too slowly for a long match, so the two Rust copies played it. Each one chooses the same moves as its Python engine at every depth, as the parity check below shows.

| Setting | Value |
| --- | --- |
| Players | Niram-PLATINUM (then called Niram-Diamond) against Niram-GOLD |
| Games | 20, 4 at once on 4 cores |
| Clock | 10 minutes a side, no increment |
| Openings | The first 10 of `version_match.py`'s OPENINGS, three moves for each side, each played once with each piece color; both engines then play their opening book |

**Niram-PLATINUM scored 18 of 20: 16 wins, 4 draws, and no losses, an Elo gap of about +382.** It won all 10 games with Black and scored 8 of 10 with White. No game ended on time or with an engine error.

| Game | White | Black | Result | Plies |
| ---: | --- | --- | --- | ---: |
| 1 | Niram-PLATINUM | Niram-GOLD | 1/2-1/2 | 106 |
| 2 | Niram-GOLD | Niram-PLATINUM | 0-1 | 140 |
| 3 | Niram-PLATINUM | Niram-GOLD | 1-0 | 127 |
| 4 | Niram-GOLD | Niram-PLATINUM | 0-1 | 162 |
| 5 | Niram-PLATINUM | Niram-GOLD | 1-0 | 105 |
| 6 | Niram-GOLD | Niram-PLATINUM | 0-1 | 150 |
| 7 | Niram-PLATINUM | Niram-GOLD | 1/2-1/2 | 29 |
| 8 | Niram-GOLD | Niram-PLATINUM | 0-1 | 120 |
| 9 | Niram-PLATINUM | Niram-GOLD | 1-0 | 155 |
| 10 | Niram-GOLD | Niram-PLATINUM | 0-1 | 144 |
| 11 | Niram-PLATINUM | Niram-GOLD | 1-0 | 107 |
| 12 | Niram-GOLD | Niram-PLATINUM | 0-1 | 130 |
| 13 | Niram-PLATINUM | Niram-GOLD | 1/2-1/2 | 183 |
| 14 | Niram-GOLD | Niram-PLATINUM | 0-1 | 128 |
| 15 | Niram-PLATINUM | Niram-GOLD | 1/2-1/2 | 30 |
| 16 | Niram-GOLD | Niram-PLATINUM | 0-1 | 108 |
| 17 | Niram-PLATINUM | Niram-GOLD | 1-0 | 145 |
| 18 | Niram-GOLD | Niram-PLATINUM | 0-1 | 102 |
| 19 | Niram-PLATINUM | Niram-GOLD | 1-0 | 129 |
| 20 | Niram-GOLD | Niram-PLATINUM | 0-1 | 192 |

Twenty games give a wide margin: measured from how far each game's score landed from the average, the 95 percent interval for 18 of 20 runs from about +250 to about +770 Elo. All four draws ended by threefold repetition, two of them early, after 29 and 30 plies (games 7 and 15). The games were not added to `misc/games/remus_games.pgn`. [`engines_elo.md`](../../../misc/designer/engines_elo.md) rates Niram-PLATINUM against Stockfish.

## The same algorithms in Rust

`uv run misc/designer/engine_parity.py --version PLATINUM` gives Remus-PLATINUM and Niram-PLATINUM the same 49 positions with no clock and compares the evaluation, the legal moves, the book moves, and every depth's score, node count, and principal variation. All 49 match, with searches of up to 150,000 positions each: [`remus-niram_platinum_same_algorithms.md`](../../../misc/designer/remus-niram_platinum_same_algorithms.md). `cargo test --release` inside `engines/Niram-PLATINUM` checks that Niram-PLATINUM visits 10,038 positions on the bench positions at depth 3, the same as Remus-PLATINUM.

## Check it

Open `run_tests.py` in this folder and click Run Python File. GOLD's 91 tests and the 14 tests in `test_platinum.py` all pass. `estimate_elo.py` rates Remus-PLATINUM against Stockfish the same way it rates Remus-GOLD. To play Remus-PLATINUM in Lucas Chess, add this folder's `remus.bat` as an external engine; for Niram-PLATINUM, build it with `cargo build --release` inside `engines/Niram-PLATINUM` and add `target/release/niram-platinum.exe`.
