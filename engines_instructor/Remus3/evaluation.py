"""evaluation.py

Score a position in centipawns (a pawn is 100): the material each
side has, a bonus or penalty for where each piece stands, and the
pawn structure (doubled, isolated, and passed pawns), and the bishop
pair. The tables show White's view with rank 8 on top; a Black piece
reads the table upside down.
"""

from board import BISHOP, EMPTY, PAWN, WHITE, Position


def mirrored_table(left_half: tuple[int, ...]) -> tuple[int, ...]:
    """
    Return a 64-square table built from files a to d of every rank.

    The tables are the same on both sides of the board: a knight earns
    the same bonus on c3 and on f3. So each table lists only files a to
    d, rank 8 first, and files e to h repeat them in reverse order:
    file e copies d, f copies c, g copies b, and h copies a.
    """
    table = []
    for row in range(8):
        # Columns a, b, c, d, then d, c, b, a again for files e to h
        for col in (0, 1, 2, 3, 3, 2, 1, 0):
            table.append(left_half[row * 4 + col])
    return tuple(table)


# Pawns gain as they advance and hold the center
PAWN_TABLE = mirrored_table((
      0,   0,   0,   0,
     50,  50,  50,  50,
     10,  10,  20,  30,
      5,   5,  10,  25,
      0,   0,   0,  20,
      5,  -5, -10,   0,
      5,  10,  10, -20,
      0,   0,   0,   0,
))  # fmt: skip

# Knights are strongest in the center
KNIGHT_TABLE = mirrored_table((
    -50, -40, -30, -30,
    -40, -20,   0,   0,
    -30,   0,  10,  15,
    -30,   5,  15,  20,
    -30,   0,  15,  20,
    -30,   5,  10,  15,
    -40, -20,   0,   5,
    -50, -40, -30, -30,
))  # fmt: skip

# Bishops avoid the corners and edges
BISHOP_TABLE = mirrored_table((
    -20, -10, -10, -10,
    -10,   0,   0,   0,
    -10,   0,   5,  10,
    -10,   5,   5,  10,
    -10,   0,  10,  10,
    -10,  10,  10,  10,
    -10,   5,   0,   0,
    -20, -10, -10, -10,
))  # fmt: skip

# The king hides behind its pawns, near a corner
KING_TABLE = mirrored_table((
    -30, -40, -40, -50,
    -30, -40, -40, -50,
    -30, -40, -40, -50,
    -30, -40, -40, -50,
    -20, -30, -30, -40,
    -10, -20, -20, -20,
     20,  20,   0,   0,
     20,  30,  10,   0,
))  # fmt: skip

# Rooks like the seventh rank and the central files
ROOK_TABLE = mirrored_table((
      0,   0,   0,   0,
      5,  10,  10,  10,
     -5,   0,   0,   0,
     -5,   0,   0,   0,
     -5,   0,   0,   0,
     -5,   0,   0,   0,
     -5,   0,   0,   0,
      0,   0,   0,   5,
))  # fmt: skip

# What each kind of piece is worth, from empty (0) to king (6). The king is never
# captured, so it counts 0.
PIECE_VALUES = (0, 100, 300, 300, 500, 900, 0)

# Queens score the same on every square
ZERO_TABLE = (0,) * 64

# The table of each kind of piece, from empty (0) to king (6)
TABLES = (
    ZERO_TABLE, PAWN_TABLE, KNIGHT_TABLE, BISHOP_TABLE,
    ROOK_TABLE, ZERO_TABLE, KING_TABLE,
)  # fmt: skip

# The bonus of a passed pawn by the moves it needs to promote
PASSED_BONUS = (0, 120, 80, 50, 30, 15, 10)
DOUBLED_PAWN = 15  # For each extra pawn on a file
ISOLATED_PAWN = 15  # No friendly pawn on a file beside it
BISHOP_PAIR = 30


def pawn_terms(pawns) -> int:
    """
    Score the doubled, isolated, and passed pawns, from White's side.

    pawns holds the squares of White's pawns, then Black's.
    """
    score = 0
    # The pawns on each file, for each side. Entry col + 1 counts file col,
    # so the a and h files have an empty file on each side.
    counts = ([0] * 10, [0] * 10)
    for side in (0, 1):
        for square in pawns[side]:
            counts[side][square % 8 + 1] += 1
    for side in (0, 1):
        sign = 1 if side == 0 else -1
        enemy = 1 - side
        for count in counts[side]:
            score -= sign * DOUBLED_PAWN * max(count - 1, 0)
        for square in pawns[side]:
            row = square // 8
            col = square % 8
            if counts[side][col] == 0 and counts[side][col + 2] == 0:
                score -= sign * ISOLATED_PAWN
            # An enemy pawn ahead on this file or a file beside it can
            # stop the pawn
            passed = True
            for other in pawns[enemy]:
                ahead = other // 8 < row if side == 0 else other // 8 > row
                if ahead and abs(other % 8 - col) <= 1:
                    passed = False
            if passed:
                steps = row if side == 0 else 7 - row  # Moves to promotion
                score += sign * PASSED_BONUS[steps]
    return score


def evaluate(position: Position) -> int:
    """Return the score for the side to move: positive when it is ahead."""
    board, white = position[0], position[1]
    score = 0  # From White's side
    pawns = ([], [])  # The squares of White's pawns, then Black's
    for square in range(64):
        piece = board[square]
        if piece == EMPTY:
            continue
        kind = piece & 7
        if kind == PAWN:
            pawns[0 if piece & WHITE else 1].append(square)
        if piece & WHITE:
            score += PIECE_VALUES[kind] + TABLES[kind][square]
        else:
            # Flip the row for Black: Black's a8 is White's a1
            score -= (
                PIECE_VALUES[kind] + TABLES[kind][(7 - square // 8) * 8 + square % 8]
            )
    if board.count(BISHOP + WHITE) >= 2:
        score += BISHOP_PAIR
    if board.count(BISHOP) >= 2:
        score -= BISHOP_PAIR
    score += pawn_terms(pawns)
    return score if white else -score
